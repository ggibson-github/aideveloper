#!/usr/bin/env python3
"""Scan published HTML for reader-facing content quality issues."""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from hierarchy_html_rules import validate_no_reference_blob, validate_visible_copy  # noqa: E402

HTML_DIR = ROOT / "documents/plans/full-automation/html-site"

PATTERNS: dict[str, re.Pattern[str]] = {
    "template_section_part_of": re.compile(r"This section is part of|This section belongs to", re.I),
    "template_designers_friction": re.compile(r"Designers should plan for real-world friction", re.I),
    "template_acceptance_boiler": re.compile(r"Acceptance criteria define when this capability", re.I),
    "template_success_not_assumed": re.compile(r"Success is not assumed: explicit verification", re.I),
    "template_hitl_duplicate": re.compile(r"The design keeps human involvement minimal", re.I),
    "comma_and_N_more": re.compile(r", and \d+ more", re.I),
    "inline_capability_list": re.compile(r"capabilities:\s*.+,", re.I),
    "covers_N_capabilities": re.compile(r"covers \d+ capabilities:", re.I),
}


def story_plain(html: str) -> str:
    m = re.search(r'class="story-block"[^>]*>(.*?)</div>', html, re.S)
    if not m:
        return ""
    return re.sub(r"<[^>]+>", " ", m.group(1))


def story_word_count(html: str) -> int:
    return len(re.findall(r"\w+", story_plain(html)))


def scan(html_dir: Path) -> dict[str, list[tuple[str, str]]]:
    pages: dict[str, list[tuple[str, str]]] = {}
    for f in sorted(html_dir.rglob("*.html")):
        rel = str(f.relative_to(html_dir)).replace("\\", "/")
        text = f.read_text(encoding="utf-8")
        issues: list[tuple[str, str]] = []
        for msg in validate_no_reference_blob(text):
            issues.append(("reference_blob", msg))
        for msg in validate_visible_copy(text):
            if not msg.startswith("reference blob"):
                issues.append(("publication", msg))
        sp = story_plain(text)
        if "story-block" in text:
            if not sp.strip():
                issues.append(("quality", "empty story-block"))
            elif "capabilities/" in rel and story_word_count(text) < 40:
                issues.append(("quality", f"short story ({story_word_count(text)} words)"))
            for name, pat in PATTERNS.items():
                if pat.search(sp):
                    issues.append(("quality", name))
        if issues:
            pages[rel] = issues
    return pages


def main() -> int:
    html_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else HTML_DIR
    pages = scan(html_dir)
    by_issue: dict[str, list[str]] = defaultdict(list)
    for rel, issues in pages.items():
        for _, detail in issues:
            by_issue[detail].append(rel)

    total = len(list(html_dir.rglob("*.html")))
    print(f"Scanned {total} HTML files under {html_dir.relative_to(ROOT)}")
    print(f"Pages with at least one issue: {len(pages)}")
    print()

    hard = {k: v for k, v in by_issue.items() if k.startswith("reference") or "publication" in k}
    print("=== Hard failures (publish should block) ===")
    if not hard:
        print("None")
    else:
        for detail, rels in sorted(hard.items(), key=lambda x: -len(x[1])):
            print(f"  {detail}: {len(rels)}")
    print()

    quality = {k: v for k, v in by_issue.items() if k not in hard}
    print("=== Similar quality issues (template / boilerplate) ===")
    for detail, rels in sorted(quality.items(), key=lambda x: -len(x[1])):
        print(f"  {detail}: {len(rels)} pages")
        for r in rels[:3]:
            print(f"    - {r}")
        if len(rels) > 3:
            print(f"    ... +{len(rels) - 3} more")

    cap_dir = html_dir / "capabilities"
    template_caps = 0
    agent_caps = 0
    if cap_dir.is_dir():
        for f in cap_dir.glob("*.html"):
            sp = story_plain(f.read_text(encoding="utf-8"))
            if PATTERNS["template_section_part_of"].search(sp):
                template_caps += 1
            elif len(sp) > 200 and not PATTERNS["template_designers_friction"].search(sp):
                agent_caps += 1
        print()
        print(f"Capability pages: {len(list(cap_dir.glob('*.html')))}")
        print(f"  Template boilerplate story (section is part of...): {template_caps}")
        print(f"  Richer agent-style story (heuristic): {agent_caps}")

    return 1 if hard else 0


if __name__ == "__main__":
    sys.exit(main())
