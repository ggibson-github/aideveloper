#!/usr/bin/env python3
"""Apply agent-authored timeline steps to hierarchy leaf Behavior sections.

Modes:
  apply-all (default) — deterministic extract from agent reader narrative (S0, no API)
  queue             — JSON work queue for Cursor CLI / SDK batch
  run-cli           — Cursor CLI headless: agent -p --trust (needs CURSOR_API_KEY)
  run-sdk           — cursor-sdk Agent.prompt batch (needs pip install cursor-sdk)
  apply-text        — apply numbered steps from a file for one leaf
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from hierarchy_agent_prose import build_brief, _vision_excerpt  # noqa: E402
from hierarchy_book_structure import capability_group_id, group_title  # noqa: E402
from hierarchy_completeness import item_id_from_path, list_leaf_paths, title_from_path  # noqa: E402
from hierarchy_html_parse import parse_markdown  # noqa: E402
from hierarchy_prose import ProseContext, build_prose_context  # noqa: E402
from hierarchy_prose_editor import (  # noqa: E402
    BEHAVIOR_HEADING,
    READER_HEADING,
    SECTION_END,
    is_timeline_agent_authored,
)
from hierarchy_timeline_author import steps_from_narrative  # noqa: E402

PROMPT_TEMPLATE = ROOT / "docs/automation/templates/hierarchy-agent-timeline-prompt.md"
GENERIC_STEP = re.compile(
    r"define and implement|map `.+` to v2\.|sec-15-index|establish .+ in pursuit and state records",
    re.I,
)


def _section_bounds(text: str, heading_pat: re.Pattern[str]) -> tuple[int, int] | None:
    m = heading_pat.search(text)
    if not m:
        return None
    start = m.end()
    rest = text[start:]
    end_m = SECTION_END.search(rest)
    end = start + end_m.start() if end_m else len(text)
    return start, end


def _reader_section(text: str) -> str:
    bounds = _section_bounds(text, READER_HEADING)
    if not bounds:
        return ""
    start, end = bounds
    return text[start:end].strip()


def render_timeline_prompt(brief: dict) -> str:
    tpl = PROMPT_TEMPLATE.read_text(encoding="utf-8")
    body = (
        tpl.replace("{item_id}", brief["item_id"])
        .replace("{title}", brief["title"])
        .replace("{vision_excerpt}", brief.get("vision_excerpt", ""))
        .replace("{group_id}", brief["group_id"])
        .replace("{group_title}", brief["group_title"])
        .replace("{branch}", brief["branch"])
        .replace("{branch_title}", brief["branch_title"])
        .replace("{siblings}", ", ".join(brief["siblings"]) or "(none)")
    )
    reader = brief.get("reader_excerpt", "")
    return (
        body
        + "\n\n---\n\n## Leaf file\n\nRead: "
        + brief["path"]
        + "\n\n## Reader narrative (authoritative context)\n\n"
        + reader
    )


def build_timeline_brief(path: Path, ctx: ProseContext, out_dir: Path) -> dict:
    brief = build_brief(path, ctx, out_dir)
    text = path.read_text(encoding="utf-8")
    reader = _reader_section(text)
    brief["reader_excerpt"] = re.sub(r"<!--.*?-->", "", reader, flags=re.S).strip()[:2000]
    brief["vision_excerpt"] = _vision_excerpt(ctx, brief["item_id"])
    brief["group_id"] = capability_group_id(brief["item_id"])
    brief["group_title"] = group_title(brief["group_id"])
    return brief


def parse_steps_from_agent_output(text: str) -> list[str]:
    steps: list[str] = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        m = re.match(r"^(\d+)[.)]\s+(.+)$", line)
        if m:
            steps.append(m.group(2).strip())
    return [s for s in steps if len(s) > 15][:5]


def critique_steps(steps: list[str]) -> list[str]:
    issues: list[str] = []
    if len(steps) < 3:
        issues.append(f"short timeline ({len(steps)} steps)")
    for s in steps:
        if GENERIC_STEP.search(s):
            issues.append("generic/doc-work step")
            break
    return issues


def cleanup_behavior_sections(text: str) -> str:
    """Fix corrupted headings and remove duplicate Behavior sections (keep agent timeline)."""
    from hierarchy_prose_editor import TIMELINE_MARKER

    # Close an open hierarchy fence before Behavior if CLI merged sections
    text = re.sub(
        r"(## Hierarchy context\s*\n\n```[^\n]*\n[\s\S]*?)\n(## Behavior / step logic)",
        r"\1\n```\n\n\2",
        text,
        count=1,
    )
    text = re.sub(r"([^\n`])## Behavior / step logic", r"\1\n\n## Behavior / step logic", text)
    text = re.sub(r"```[^\n]*## Behavior / step logic", "## Behavior / step logic", text)

    matches = list(BEHAVIOR_HEADING.finditer(text))
    if len(matches) <= 1:
        return text

    keep_idx = 0
    for i, m in enumerate(matches):
        start = m.end()
        rest = text[start:]
        end_m = SECTION_END.search(rest)
        end = start + end_m.start() if end_m else len(text)
        if TIMELINE_MARKER.search(text[start:end]):
            keep_idx = i
            break

    for i in reversed(range(len(matches))):
        if i == keep_idx:
            continue
        m = matches[i]
        start = m.start()
        rest = text[m.end() :]
        end_m = SECTION_END.search(rest)
        end = m.end() + end_m.start() if end_m else len(text)
        text = text[:start] + text[end:]

    return text


def apply_timeline_text(
    text: str,
    steps: list[str],
    *,
    version: str = "narrative-v1",
) -> tuple[str, list[str]]:
    issues = critique_steps(steps)
    if not steps:
        issues.append("empty timeline")
        return text, issues

    marker = f"<!-- timeline-source: agent {version} {date.today().isoformat()} -->\n\n"
    numbered = "\n".join(f"{i}. {s.strip()}" for i, s in enumerate(steps, 1) if s.strip())
    block = marker + numbered + "\n"

    bounds = _section_bounds(text, BEHAVIOR_HEADING)
    if bounds:
        start, end = bounds
        text = text[:start] + "\n" + block + text[end:]
    else:
        purpose = re.search(r"^## Purpose\s*$", text, re.M)
        insert_at = purpose.start() if purpose else 0
        text = text[:insert_at] + "## Behavior / step logic\n" + block + "\n" + text[insert_at:]
    return text, issues


def write_timeline(path: Path, steps: list[str], *, version: str = "narrative-v1", dry_run: bool = False) -> list[str]:
    text = path.read_text(encoding="utf-8")
    new_text, issues = apply_timeline_text(text, steps, version=version)
    new_text = cleanup_behavior_sections(new_text)
    if not dry_run:
        path.write_text(new_text, encoding="utf-8")
    return issues


def apply_file(path: Path, *, dry_run: bool = False, force: bool = False) -> list[str]:
    text = path.read_text(encoding="utf-8")
    if not force and is_timeline_agent_authored(text):
        return []

    item_id = item_id_from_path(path, text)
    node = parse_markdown(path, text)
    reader = _reader_section(text)
    steps = steps_from_narrative(
        reader,
        item_id=item_id,
        title=node.title,
        branch=node.branch,
    )
    return write_timeline(path, steps, version="narrative-v1", dry_run=dry_run)


def queue_leaves(
    out_dir: Path,
    ctx: ProseContext,
    *,
    group: str | None = None,
    ids: list[str] | None = None,
    skip_done: bool = True,
) -> list[dict]:
    items: list[dict] = []
    for p in list_leaf_paths(out_dir):
        text = p.read_text(encoding="utf-8")
        iid = item_id_from_path(p, text)
        if ids and iid not in ids:
            continue
        if group and capability_group_id(iid) != group:
            continue
        if skip_done and is_timeline_agent_authored(text):
            continue
        brief = build_timeline_brief(p, ctx, out_dir)
        brief["prompt"] = render_timeline_prompt(brief)
        items.append(brief)
    return items


def resolve_agent_cli() -> list[str]:
    """Return argv prefix to invoke Cursor headless CLI (Windows: agent.cmd, not bare 'agent')."""
    if sys.platform == "win32":
        local = Path(os.environ.get("LOCALAPPDATA", "")) / "cursor-agent"
        cmd = local / "agent.cmd"
        if cmd.is_file():
            return [str(cmd)]
        ps1 = local / "agent.ps1"
        if ps1.is_file():
            return [
                "powershell",
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-File",
                str(ps1),
            ]
    exe = shutil.which("agent")
    if exe:
        return [exe]
    if shutil.which("cursor"):
        return ["cursor", "agent"]
    return ["agent"]


def run_cli_prompt(prompt: str, *, model: str, cwd: Path) -> tuple[int, str]:
    if not os.environ.get("CURSOR_API_KEY"):
        print("Set CURSOR_API_KEY for headless Cursor CLI", file=sys.stderr)
        return 2, ""
    cmd = resolve_agent_cli() + [
        "-p",
        "--trust",
        "--output-format",
        "text",
        "--model",
        model,
        prompt,
    ]
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=900,
        )
    except FileNotFoundError:
        print(
            "Cursor CLI not found. Install: https://cursor.com/docs/cli/headless "
            "(Windows: irm 'https://cursor.com/install?win32=true' | iex)",
            file=sys.stderr,
        )
        return 127, ""
    except subprocess.TimeoutExpired:
        return 124, ""
    out = (proc.stdout or "") + (proc.stderr or "")
    return proc.returncode, out.strip()


PROGRESS_FILE = ROOT / "docs/automation/hierarchy-timeline-cli-progress.json"


def load_cli_progress(progress_file: Path | None = None) -> dict:
    p = progress_file or PROGRESS_FILE
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return {"done": {}, "failed": {}}


def save_cli_progress(progress: dict, progress_file: Path | None = None) -> None:
    p = progress_file or PROGRESS_FILE
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(progress, indent=2) + "\n", encoding="utf-8")


def run_cli_batch(
    items: list[dict],
    model: str,
    *,
    force: bool = False,
    progress_file: Path | None = None,
) -> int:
    failed = 0
    progress = load_cli_progress(progress_file)
    version_tag = f"cli-{model}"
    for brief in items:
        iid = brief["item_id"]
        if not force and iid in progress.get("done", {}):
            print(f"CLI timeline: {iid} (skip, done)")
            continue
        path = ROOT / brief["path"]
        print(f"CLI timeline: {iid} …", flush=True)
        rc, out = run_cli_prompt(brief["prompt"], model=model, cwd=ROOT)
        if rc != 0:
            print(f"  FAILED rc={rc}", file=sys.stderr)
            progress.setdefault("failed", {})[iid] = {"rc": rc, "snippet": out[:500]}
            save_cli_progress(progress, progress_file)
            failed += 1
            continue
        steps = parse_steps_from_agent_output(out)
        if len(steps) < 3:
            print("  WARN: parse failed; narrative fallback", file=sys.stderr)
            node = parse_markdown(path)
            steps = steps_from_narrative(
                _reader_section(path.read_text(encoding="utf-8")),
                item_id=iid,
                title=node.title,
                branch=node.branch,
            )
        issues = write_timeline(path, steps, version=version_tag, dry_run=False)
        progress.setdefault("done", {})[iid] = {"version": version_tag, "issues": issues}
        progress.get("failed", {}).pop(iid, None)
        save_cli_progress(progress, progress_file)
        if issues:
            print(f"  critique: {', '.join(issues)}")
    print(f"CLI batch complete: {len(progress.get('done', {}))} done, {failed} failed this run")
    return 1 if failed else 0


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
        print(f"SDK timeline: {brief['item_id']} …")
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
        steps = parse_steps_from_agent_output(result.result)
        if len(steps) < 3:
            node = parse_markdown(path)
            steps = steps_from_narrative(
                _reader_section(path.read_text(encoding="utf-8")),
                item_id=brief["item_id"],
                title=node.title,
                branch=node.branch,
            )
        issues = write_timeline(path, steps, version=f"sdk-{model}", dry_run=False)
        if issues:
            print(f"  critique: {', '.join(issues)}")
    return 1 if failed else 0


def cleanup_all(out_dir: Path | None = None, *, dry_run: bool = False) -> int:
    base = out_dir or ROOT / "documents/plans/full-automation"
    cleaned = 0
    for path in list_leaf_paths(base):
        old = path.read_text(encoding="utf-8")
        new = cleanup_behavior_sections(old)
        if new != old:
            cleaned += 1
            if not dry_run:
                path.write_text(new, encoding="utf-8")
    print(f"Cleaned duplicate/corrupt behavior sections in {cleaned} leaves")
    return 0


def apply_all(out_dir: Path | None = None, *, dry_run: bool = False, force: bool = False) -> int:
    base = out_dir or ROOT / "documents/plans/full-automation"
    applied = 0
    skipped = 0
    flagged: list[str] = []
    for path in list_leaf_paths(base):
        text = path.read_text(encoding="utf-8")
        if not force and is_timeline_agent_authored(text):
            skipped += 1
            continue
        issues = apply_file(path, dry_run=dry_run, force=force)
        applied += 1
        if issues:
            iid = item_id_from_path(path, path.read_text(encoding="utf-8"))
            flagged.append(f"{iid}: {', '.join(issues)}")
    print(f"Applied agent timeline to {applied} leaves ({skipped} skipped, already agent-authored)")
    for line in flagged[:20]:
        print(line)
    if len(flagged) > 20:
        print(f"... +{len(flagged) - 20} more flags")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Agent timeline steps for hierarchy leaves")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_apply = sub.add_parser("apply-all", help="Deterministic timeline from reader narrative (S0)")
    p_apply.add_argument("--output-dir", default="documents/plans/full-automation")
    p_apply.add_argument("--dry-run", action="store_true")
    p_apply.add_argument("--force", action="store_true")

    p_queue = sub.add_parser("queue", help="Write CLI/SDK work queue JSON")
    p_queue.add_argument("--output-dir", default="documents/plans/full-automation")
    p_queue.add_argument("--group", default=None)
    p_queue.add_argument("--ids", default=None, help="Comma-separated ids")
    p_queue.add_argument("--out", default="docs/automation/hierarchy-timeline-agent-queue.json")
    p_queue.add_argument("--all", action="store_true", help="Include leaves that already have agent timeline")

    p_cli = sub.add_parser("run-cli", help="Batch via Cursor CLI: agent -p --trust")
    p_cli.add_argument("--output-dir", default="documents/plans/full-automation")
    p_cli.add_argument("--group", default=None)
    p_cli.add_argument("--ids", default=None)
    p_cli.add_argument("--model", default="composer-2.5")
    p_cli.add_argument("--limit", type=int, default=0)
    p_cli.add_argument("--queue", default=None, help="Use existing queue JSON")
    p_cli.add_argument("--all", action="store_true", help="Include leaves with existing agent timeline")
    p_cli.add_argument("--force", action="store_true", help="Re-run even if progress file marks done")
    p_cli.add_argument(
        "--progress-file",
        default=None,
        help="Progress JSON path (default docs/automation/hierarchy-timeline-cli-progress.json)",
    )

    p_sdk = sub.add_parser("run-sdk", help="Batch via cursor-sdk Agent.prompt")
    p_sdk.add_argument("--output-dir", default="documents/plans/full-automation")
    p_sdk.add_argument("--group", default=None)
    p_sdk.add_argument("--ids", default=None)
    p_sdk.add_argument("--model", default="composer-2.5")
    p_sdk.add_argument("--limit", type=int, default=0)
    p_sdk.add_argument("--queue", default=None)

    p_text = sub.add_parser("apply-text", help="Apply numbered steps from file")
    p_text.add_argument("--id", required=True)
    p_text.add_argument("--text-file", required=True)
    p_text.add_argument("--output-dir", default="documents/plans/full-automation")
    p_text.add_argument("--version", default="cli-manual")

    p_clean = sub.add_parser("cleanup", help="Remove duplicate behavior sections")
    p_clean.add_argument("--output-dir", default="documents/plans/full-automation")
    p_clean.add_argument("--dry-run", action="store_true")

    args = parser.parse_args()
    out_dir = ROOT / args.output_dir
    vision = ROOT / "documents/full-automation-vision-and-hierarchy.md"
    ctx = build_prose_context(out_dir, vision)

    if args.cmd == "apply-all":
        return apply_all(out_dir, dry_run=args.dry_run, force=args.force)
    if args.cmd == "cleanup":
        return cleanup_all(out_dir, dry_run=args.dry_run)
    if args.cmd == "apply-text":
        ids = {args.id}
        for p in list_leaf_paths(out_dir):
            if item_id_from_path(p, p.read_text(encoding="utf-8")) == args.id:
                steps = parse_steps_from_agent_output(Path(args.text_file).read_text(encoding="utf-8"))
                issues = write_timeline(p, steps, version=args.version)
                if issues:
                    print(f"critique: {', '.join(issues)}")
                return 0
        print(f"Not found: {args.id}", file=sys.stderr)
        return 1
    if args.cmd == "queue":
        ids = [x.strip() for x in args.ids.split(",")] if args.ids else None
        items = queue_leaves(out_dir, ctx, group=args.group, ids=ids, skip_done=not args.all)
        out_path = ROOT / args.out
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(
            json.dumps({"generated": date.today().isoformat(), "items": items}, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"Queued {len(items)} leaves -> {out_path.relative_to(ROOT)}")
        return 0

    if args.cmd in ("run-cli", "run-sdk"):
        if args.queue:
            items = json.loads(Path(args.queue).read_text(encoding="utf-8"))["items"]
        else:
            ids = [x.strip() for x in args.ids.split(",")] if args.ids else None
            skip = not getattr(args, "all", False)
            items = queue_leaves(out_dir, ctx, group=args.group, ids=ids, skip_done=skip)
        if args.limit:
            items = items[: args.limit]
        if not items:
            print("No leaves to process")
            return 0
        if args.cmd == "run-cli":
            pf = Path(args.progress_file) if args.progress_file else None
            if pf and not pf.is_absolute():
                pf = ROOT / pf
            return run_cli_batch(items, args.model, force=getattr(args, "force", False), progress_file=pf)
        return run_sdk_batch(items, args.model)

    return 1


if __name__ == "__main__":
    # Back-compat: bare --force without subcommand
    if len(sys.argv) > 1 and sys.argv[1].startswith("-"):
        legacy = argparse.ArgumentParser()
        legacy.add_argument("--output-dir", default="documents/plans/full-automation")
        legacy.add_argument("--dry-run", action="store_true")
        legacy.add_argument("--force", action="store_true")
        legacy.add_argument("--cleanup-only", action="store_true")
        a = legacy.parse_args()
        if a.cleanup_only:
            raise SystemExit(cleanup_all(ROOT / a.output_dir, dry_run=a.dry_run))
        raise SystemExit(apply_all(ROOT / a.output_dir, dry_run=a.dry_run, force=a.force))
    raise SystemExit(main())
