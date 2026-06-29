#!/usr/bin/env python3
"""Audit published HTML timeline steps for generic boilerplate and doc-work leaks."""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from hierarchy_completeness import list_leaf_paths  # noqa: E402
from hierarchy_html_parse import load_all_nodes  # noqa: E402
from hierarchy_html_rules import is_conceptual_capability, public_behavior_steps  # noqa: E402
from hierarchy_prose_editor import is_timeline_agent_authored  # noqa: E402
from hierarchy_reader_narrative import humanize_timeline_step  # noqa: E402

HTML_DIR = ROOT / "documents/plans/full-automation/html-site"
PLAN_DIR = ROOT / "documents/plans/full-automation"

BAD_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("generic_establish", re.compile(r"establish .+ in pursuit and state records", re.I)),
    ("define_implement", re.compile(r"define and implement", re.I)),
    ("doc_work", re.compile(r"map `.+` to v2\.|sec-15-index|sec-15 release row", re.I)),
    ("empty_timeline", re.compile(r"^see diagram above\.?$", re.I)),
)


def audit_plan_md(plan_dir: Path) -> dict[str, list[str]]:
    issues: dict[str, list[str]] = defaultdict(list)
    for path in list_leaf_paths(plan_dir):
        text = path.read_text(encoding="utf-8")
        if not is_timeline_agent_authored(text):
            issues["missing_agent_timeline"].append(path.stem)
    return issues


def audit_html(html_dir: Path, nodes) -> dict[str, list[str]]:
    by_id = {n.id: n for n in nodes}
    issues: dict[str, list[str]] = defaultdict(list)

    for f in sorted(html_dir.rglob("capabilities/*.html")):
        rel = str(f.relative_to(html_dir)).replace("\\", "/")
        text = f.read_text(encoding="utf-8")
        m = re.search(r'capabilities/([A-Z0-9.-]+)\.html', rel)
        if not m:
            continue
        # find node by slug
        slug = m.group(1)
        node = next((n for n in nodes if n.slug == slug or slug in n.slug), None)
        if not node:
            continue
        steps = public_behavior_steps(node.behavior_steps, item_id=node.id, branch=node.branch)
        if not steps:
            issues["empty_steps"].append(node.id)
            continue
        for i, step in enumerate(steps[:8], 1):
            rendered = humanize_timeline_step(step, node)
            for name, pat in BAD_PATTERNS:
                if pat.search(rendered):
                    issues[name].append(f"{node.id} step {i}")
    return issues


def main() -> int:
    html_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else HTML_DIR
    plan_dir = PLAN_DIR
    nodes = load_all_nodes(plan_dir)
    md_issues = audit_plan_md(plan_dir)
    html_issues = audit_html(html_dir, nodes) if html_dir.is_dir() else {}

    total = sum(len(v) for v in md_issues.values()) + sum(len(v) for v in html_issues.values())
    print(f"TIMELINE AUDIT — {len(nodes)} capabilities")
    for kind, pages in sorted({**md_issues, **html_issues}.items()):
        print(f"  {kind}: {len(pages)}")
        for p in pages[:5]:
            print(f"    - {p}")
        if len(pages) > 5:
            print(f"    ... +{len(pages) - 5} more")

    if total:
        print("\nTIMELINE AUDIT FAILED")
        return 1
    print("\nTIMELINE AUDIT PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
