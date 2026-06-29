#!/usr/bin/env python3
"""
Critic / writer editor pass for hierarchy leaf markdown.

Runs after each leaf rebuild in the 3-pass pipeline to fix reader-facing prose:
- Link vision §N references
- Replace .cursor/rules links with capability spec links
- Link S0 and other tier terms
- Strip raw markdown bold and meta process steps from Behavior
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from hierarchy_completeness import item_id_from_path, list_leaf_paths, title_from_path  # noqa: E402
from hierarchy_prose import (  # noqa: E402
    ProseContext,
    build_prose_context,
    critique_prose,
    is_meta_step,
    normalize_prose_md,
    normalize_step_md,
    repair_corrupted_links,
)
from hierarchy_html_parse import parse_markdown  # noqa: E402
from hierarchy_vision_context import section_for_branch  # noqa: E402
from hierarchy_reader_narrative import build_reader_story_md, should_preserve_reader_narrative  # noqa: E402

READER_HEADING = re.compile(r"^## Reader narrative\s*$", re.M)
AGENT_PROSE_MARKER = re.compile(r"<!--\s*prose-source:\s*agent\b", re.I)
TIMELINE_MARKER = re.compile(r"<!--\s*timeline-source:\s*agent\b", re.I)

BEHAVIOR_HEADING = re.compile(r"^(## Behavior / step logic|## Behavior)\s*$", re.M)
SECTION_END = re.compile(r"^## ", re.M)


def is_timeline_agent_authored(text: str) -> bool:
    bounds = _section_bounds(text, BEHAVIOR_HEADING)
    if not bounds:
        return False
    return bool(TIMELINE_MARKER.search(text[bounds[0] : bounds[1]]))


def is_agent_authored(text: str) -> bool:
    bounds = _section_bounds(text, READER_HEADING)
    if not bounds:
        return False
    return bool(AGENT_PROSE_MARKER.search(text[bounds[0] : bounds[1]]))


def _section_bounds(text: str, heading_pat: re.Pattern[str]) -> tuple[int, int] | None:
    m = heading_pat.search(text)
    if not m:
        return None
    start = m.end()
    rest = text[start:]
    end_m = SECTION_END.search(rest)
    end = start + end_m.start() if end_m else len(text)
    return start, end


def _rewrite_behavior_section(text: str, ctx: ProseContext, item_id: str, title: str) -> tuple[str, int]:
    if is_timeline_agent_authored(text):
        return text, 0
    bounds = _section_bounds(text, BEHAVIOR_HEADING)
    if not bounds:
        return text, 0
    start, end = bounds
    block = text[start:end]
    lines = block.splitlines()
    new_lines: list[str] = []
    changes = 0
    step_num = 0
    for line in lines:
        m = re.match(r"^(\d+)\.\s+(.*)$", line.strip())
        if not m:
            new_lines.append(line)
            continue
        raw = m.group(2)
        if is_meta_step(raw):
            changes += 1
            continue
        normalized = normalize_step_md(raw, ctx, item_id=item_id, title=title)
        if not normalized:
            changes += 1
            continue
        if normalized != raw:
            changes += 1
        step_num += 1
        new_lines.append(f"{step_num}. {normalized}")
    new_block = "\n".join(new_lines)
    if new_block != block:
        return text[:start] + new_block + text[end:], changes
    return text, changes


def _rewrite_purpose(text: str, ctx: ProseContext, item_id: str, title: str) -> tuple[str, int]:
    bounds = _section_bounds(text, re.compile(r"^## Purpose\s*$", re.M))
    if not bounds:
        return text, 0
    start, end = bounds
    block = text[start:end].strip()
    if not block:
        return text, 0
    normalized = normalize_prose_md(block, ctx, item_id=item_id, title=title)
    if normalized == block:
        return text, 0
    return text[:start] + "\n" + normalized + "\n" + text[end:], 1


def _branch_title(item_id: str, ctx: ProseContext) -> str:
    m = re.match(r"^([A-J])", item_id)
    if m:
        sec = ctx.vision_sections.get(f"§{ord(m.group(1)) - ord('A') + 3}", {})
        return sec.get("title", f"Branch {m.group(1)}")
    return "Architecture"


def _upsert_reader_narrative(text: str, story: str) -> tuple[str, int]:
    bounds = _section_bounds(text, READER_HEADING)
    block = f"\n{story.strip()}\n"
    if bounds:
        start, end = bounds
        old = text[start:end].strip()
        if old == story.strip():
            return text, 0
        return text[:start] + block + text[end:], 1
    purpose = re.search(r"^## Purpose\s*$", text, re.M)
    if purpose:
        insert_at = purpose.start()
        section = f"## Reader narrative\n{story.strip()}\n\n"
        return text[:insert_at] + section + text[insert_at:], 1
    return text, 0


def _rewrite_scope_bullets(text: str, ctx: ProseContext, item_id: str, title: str) -> tuple[str, int]:
    bounds = _section_bounds(text, re.compile(r"^## Scope\s*$", re.M))
    if not bounds:
        return text, 0
    start, end = bounds
    block = text[start:end]
    changes = 0
    new_lines: list[str] = []
    for line in block.splitlines():
        if line.strip().startswith("- "):
            raw = line.strip()[2:]
            if raw.startswith("Conflicts resolve"):
                key = section_for_branch(item_id) or "§3"
                norm = f"Conflicts resolve in favor of {ctx.vision_md_link(key)}."
                if norm != raw:
                    changes += 1
                    new_lines.append(f"- {norm}")
                    continue
            if "[[Vision" in raw or ("vision" in raw.lower() and "§" in raw) or ".cursor/rules/" in raw:
                norm = normalize_prose_md(raw, ctx, item_id=item_id, title=title)
                if norm != raw:
                    changes += 1
                    new_lines.append(f"- {norm}")
                    continue
        new_lines.append(line)
    if changes:
        return text[:start] + "\n".join(new_lines) + text[end:], changes
    return text, 0


def edit_leaf_markdown(path: Path, ctx: ProseContext, *, allow_reader_overwrite: bool = True) -> tuple[str, int, list[str]]:
    """Return (new_text, change_count, remaining_critique_issues)."""
    text = path.read_text(encoding="utf-8")
    item_id = item_id_from_path(path, text)
    title = title_from_path(path, item_id)
    total = 0

    repaired = repair_corrupted_links(text, ctx)
    if repaired != text:
        text = repaired
        total += 1

    branch_title = _branch_title(item_id, ctx)
    node = parse_markdown(path, text)
    bounds = _section_bounds(text, READER_HEADING)
    existing_reader = text[bounds[0] : bounds[1]].strip() if bounds else ""

    if allow_reader_overwrite and not (
        is_agent_authored(text) or should_preserve_reader_narrative(existing_reader)
    ):
        story = build_reader_story_md(node, ctx, branch_title)
        text, n = _upsert_reader_narrative(text, story)
        total += n
        existing_reader = story.strip()
    else:
        existing_reader = existing_reader or node.reader_narrative

    story = existing_reader

    text, n = _rewrite_purpose(text, ctx, item_id, title)
    total += n
    text, n = _rewrite_scope_bullets(text, ctx, item_id, title)
    total += n
    text, n = _rewrite_behavior_section(text, ctx, item_id, title)
    total += n
    issues = critique_prose(story + "\n" + text)
    return text, total, issues


def edit_leaf_for_readers(path: Path, ctx: ProseContext, *, dry_run: bool = False, allow_reader_overwrite: bool = True) -> bool:
    new_text, changes, _issues = edit_leaf_markdown(path, ctx, allow_reader_overwrite=allow_reader_overwrite)
    if changes and not dry_run:
        path.write_text(new_text, encoding="utf-8")
    return changes > 0


def run_prose_editor_pass(
    out_dir: Path,
    *,
    vision_path: Path | None = None,
    dry_run: bool = False,
    allow_reader_overwrite: bool = True,
) -> dict:
    ctx = build_prose_context(out_dir, vision_path)
    edited = 0
    issues_by_id: dict[str, list[str]] = {}
    for p in list_leaf_paths(out_dir):
        new_text, changes, issues = edit_leaf_markdown(
            p, ctx, allow_reader_overwrite=allow_reader_overwrite
        )
        iid = item_id_from_path(p, new_text)
        if issues:
            issues_by_id[iid] = issues
        if changes and not dry_run:
            p.write_text(new_text, encoding="utf-8")
            edited += 1
        elif changes:
            edited += 1
    return {"edited": edited, "total": len(list_leaf_paths(out_dir)), "issues": issues_by_id}


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Writer/critic prose editor pass on hierarchy leaves")
    parser.add_argument("--output-dir", default="documents/plans/full-automation")
    parser.add_argument("--vision", default="documents/full-automation-vision-and-hierarchy.md")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    out_dir = ROOT / args.output_dir
    result = run_prose_editor_pass(out_dir, vision_path=ROOT / args.vision, dry_run=args.dry_run)
    print(f"Edited {result['edited']} / {result['total']} leaves")
    if result["issues"]:
        print(f"Remaining critique issues: {len(result['issues'])} nodes")
        for iid, issues in list(result["issues"].items())[:10]:
            print(f"  {iid}: {', '.join(issues)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
