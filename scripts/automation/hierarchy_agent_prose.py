#!/usr/bin/env python3
"""
Agent-driven Reader narrative writer for hierarchy leaves.

Template prose (hierarchy_reader_narrative.py) is deterministic and fast but not
book-quality. This module builds research briefs and applies agent-authored prose
that is preserved across subsequent prose-editor runs.

Usage:
  python scripts/automation/hierarchy_agent_prose.py brief --id A1.1
  python scripts/automation/hierarchy_agent_prose.py queue --group A1
  python scripts/automation/hierarchy_agent_prose.py apply --id A1.1 --text-file narrative.md
  python scripts/automation/hierarchy_agent_prose.py run-sdk --group A1   # needs cursor-sdk + CURSOR_API_KEY
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from hierarchy_book_structure import GROUP_CATALOG, capability_group_id, group_title  # noqa: E402
from hierarchy_completeness import item_id_from_path, list_leaf_paths, title_from_path  # noqa: E402
from hierarchy_html_parse import parse_markdown  # noqa: E402
from hierarchy_prose import ProseContext, build_prose_context, critique_prose  # noqa: E402
from hierarchy_prose_editor import READER_HEADING, is_agent_authored, _section_bounds  # noqa: E402
from hierarchy_vision_context import section_for_branch  # noqa: E402

PROMPT_TEMPLATE = ROOT / "docs/automation/templates/hierarchy-agent-prose-prompt.md"
AGENT_MARKER = re.compile(r"<!--\s*prose-source:\s*agent\b", re.I)
MIN_AGENT_WORDS = 35


def _vision_excerpt(ctx: ProseContext, item_id: str, max_chars: int = 1200) -> str:
    key = section_for_branch(item_id) or "§3"
    sec = ctx.vision_sections.get(key, {})
    body = sec.get("body", "") or sec.get("title", "")
    return body[:max_chars].strip()


def _siblings(out_dir: Path, item_id: str) -> list[str]:
    gid = capability_group_id(item_id)
    sibs: list[str] = []
    for p in list_leaf_paths(out_dir):
        iid = item_id_from_path(p, p.read_text(encoding="utf-8"))
        if capability_group_id(iid) == gid and iid != item_id:
            sibs.append(iid)
    return sorted(sibs)


def build_brief(path: Path, ctx: ProseContext, out_dir: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    item_id = item_id_from_path(path, text)
    node = parse_markdown(path, text)
    gid = capability_group_id(item_id)
    branch = node.branch
    branch_title = ctx.vision_sections.get(section_for_branch(item_id) or "§3", {}).get("title", branch)
    return {
        "item_id": item_id,
        "title": title_from_path(path, item_id),
        "path": str(path.relative_to(ROOT)).replace("\\", "/"),
        "branch": branch,
        "branch_title": branch_title,
        "group_id": gid,
        "group_title": group_title(gid),
        "siblings": _siblings(out_dir, item_id),
        "purpose": node.purpose[:500],
        "behavior_steps": node.behavior_steps[:6],
        "edge_cases": node.edge_cases[:4],
        "vision_excerpt": _vision_excerpt(ctx, item_id),
    }


def render_prompt(brief: dict) -> str:
    tpl = PROMPT_TEMPLATE.read_text(encoding="utf-8")
    return (
        tpl.replace("{item_id}", brief["item_id"])
        .replace("{title}", brief["title"])
        .replace("{vision_excerpt}", brief["vision_excerpt"])
        .replace("{group_id}", brief["group_id"])
        .replace("{group_title}", brief["group_title"])
        .replace("{branch}", brief["branch"])
        .replace("{branch_title}", brief["branch_title"])
        .replace("{siblings}", ", ".join(brief["siblings"]) or "(none)")
        + "\n\n---\n\n## Leaf file\n\nRead: "
        + brief["path"]
        + "\n\nPurpose: "
        + brief["purpose"]
        + "\n\nBehavior steps:\n"
        + "\n".join(f"- {s}" for s in brief["behavior_steps"])
    )


def apply_narrative(path: Path, narrative: str, *, version: str = "v1") -> tuple[str, list[str]]:
    """Upsert agent narrative; return (new_text, critique_issues)."""
    text = path.read_text(encoding="utf-8")
    narrative = narrative.strip()
    if narrative.startswith("## Reader narrative"):
        narrative = re.sub(r"^## Reader narrative\s*", "", narrative).strip()
    marker = f"<!-- prose-source: agent {version} {date.today().isoformat()} -->\n\n"
    block = marker + narrative + "\n"
    bounds = _section_bounds(text, READER_HEADING)
    if bounds:
        start, end = bounds
        text = text[:start] + "\n" + block + text[end:]
    else:
        purpose = re.search(r"^## Purpose\s*$", text, re.M)
        insert = f"## Reader narrative\n{block}\n"
        if purpose:
            text = text[: purpose.start()] + insert + text[purpose.start() :]
        else:
            text = insert + text
    issues = critique_prose(narrative)
    word_count = len(re.findall(r"\w+", narrative))
    if word_count < MIN_AGENT_WORDS:
        issues.append(f"too short ({word_count} words, need >={MIN_AGENT_WORDS})")
    return text, issues


def write_narrative(path: Path, narrative: str, *, dry_run: bool = False) -> list[str]:
    new_text, issues = apply_narrative(path, narrative)
    if not dry_run:
        path.write_text(new_text, encoding="utf-8")
    return issues


def find_paths_for_item_ids(out_dir: Path, item_ids: set[str]) -> dict[str, Path]:
    """Map item_id -> markdown path; prefer leaf files over *-index.md names."""
    buckets: dict[str, list[Path]] = {iid: [] for iid in item_ids}
    for p in sorted(out_dir.glob("*.md")):
        if p.name == "INDEX.md":
            continue
        iid = item_id_from_path(p, p.read_text(encoding="utf-8"))
        if iid in buckets:
            buckets[iid].append(p)
    out: dict[str, Path] = {}
    for iid, paths in buckets.items():
        if not paths:
            continue
        paths.sort(key=lambda x: (x.name.endswith("-index.md"), x.name))
        out[iid] = paths[0]
    return out


def queue_leaves(
    out_dir: Path,
    ctx: ProseContext,
    *,
    group: str | None = None,
    ids: list[str] | None = None,
    skip_agent: bool = True,
) -> list[dict]:
    items: list[dict] = []
    for p in list_leaf_paths(out_dir):
        text = p.read_text(encoding="utf-8")
        iid = item_id_from_path(p, text)
        if ids and iid not in ids:
            continue
        if group and capability_group_id(iid) != group:
            continue
        if skip_agent and is_agent_authored(text):
            continue
        brief = build_brief(p, ctx, out_dir)
        brief["prompt"] = render_prompt(brief)
        items.append(brief)
    return items


def run_sdk_batch(items: list[dict], model: str) -> int:
    try:
        from cursor_sdk import Agent, AgentOptions, LocalAgentOptions
    except ImportError:
        print("Install cursor-sdk: pip install cursor-sdk", file=sys.stderr)
        return 2
    api_key = os.environ.get("CURSOR_API_KEY")
    if not api_key:
        print("Set CURSOR_API_KEY", file=sys.stderr)
        return 2
    failed = 0
    for brief in items:
        path = ROOT / brief["path"]
        print(f"Agent prose: {brief['item_id']} …")
        result = Agent.prompt(
            brief["prompt"],
            AgentOptions(
                api_key=api_key,
                model=model,
                local=LocalAgentOptions(cwd=str(ROOT)),
            ),
        )
        if result.status != "completed" or not result.result:
            print(f"  FAILED: {result.status}", file=sys.stderr)
            failed += 1
            continue
        issues = write_narrative(path, result.result.strip())
        if issues:
            print(f"  critique: {', '.join(issues)}")
    return 1 if failed else 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Agent prose writer for hierarchy leaves")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_brief = sub.add_parser("brief", help="Print research brief JSON for one leaf")
    p_brief.add_argument("--id", required=True)
    p_brief.add_argument("--output-dir", default="documents/plans/full-automation")

    p_queue = sub.add_parser("queue", help="Write agent work queue JSON")
    p_queue.add_argument("--output-dir", default="documents/plans/full-automation")
    p_queue.add_argument("--group", default=None)
    p_queue.add_argument("--ids", default=None, help="Comma-separated ids")
    p_queue.add_argument("--out", default="docs/automation/hierarchy-prose-agent-queue.json")

    p_apply = sub.add_parser("apply", help="Apply narrative from file or stdin")
    p_apply.add_argument("--id", required=True)
    p_apply.add_argument("--text-file", default=None)
    p_apply.add_argument("--output-dir", default="documents/plans/full-automation")
    p_apply.add_argument("--dry-run", action="store_true")

    p_sdk = sub.add_parser("run-sdk", help="Run Cursor SDK agent per queued leaf")
    p_sdk.add_argument("--output-dir", default="documents/plans/full-automation")
    p_sdk.add_argument("--group", default=None)
    p_sdk.add_argument("--ids", default=None)
    p_sdk.add_argument("--model", default="composer-2.5")
    p_sdk.add_argument("--limit", type=int, default=0)

    args = parser.parse_args()
    out_dir = ROOT / args.output_dir
    vision = ROOT / "documents/full-automation-vision-and-hierarchy.md"
    ctx = build_prose_context(out_dir, vision)

    if args.cmd == "brief":
        for p in list_leaf_paths(out_dir):
            if item_id_from_path(p, p.read_text(encoding="utf-8")) == args.id:
                print(json.dumps(build_brief(p, ctx, out_dir), indent=2))
                return 0
        print(f"Not found: {args.id}", file=sys.stderr)
        return 1

    if args.cmd == "queue":
        ids = [x.strip() for x in args.ids.split(",")] if args.ids else None
        items = queue_leaves(out_dir, ctx, group=args.group, ids=ids)
        out_path = ROOT / args.out
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps({"generated": date.today().isoformat(), "items": items}, indent=2) + "\n", encoding="utf-8")
        print(f"Queued {len(items)} leaves -> {out_path.relative_to(ROOT)}")
        return 0

    if args.cmd == "apply":
        for p in list_leaf_paths(out_dir):
            if item_id_from_path(p, p.read_text(encoding="utf-8")) == args.id:
                narrative = Path(args.text_file).read_text(encoding="utf-8") if args.text_file else sys.stdin.read()
                issues = write_narrative(p, narrative, dry_run=args.dry_run)
                if issues:
                    print("Critique:", ", ".join(issues))
                print(f"Applied to {p.name}" + (" (dry-run)" if args.dry_run else ""))
                return 0
        return 1

    if args.cmd == "run-sdk":
        ids = [x.strip() for x in args.ids.split(",")] if args.ids else None
        items = queue_leaves(out_dir, ctx, group=args.group, ids=ids)
        if args.limit:
            items = items[: args.limit]
        if not items:
            print("Nothing to process (all agent-authored or no matches)")
            return 0
        return run_sdk_batch(items, args.model)

    return 1


if __name__ == "__main__":
    sys.exit(main())
