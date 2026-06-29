#!/usr/bin/env python3
"""Strict reader-readiness audit for published hierarchy HTML book."""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

import importlib.util

_scan_spec = importlib.util.spec_from_file_location(
    "scan_html_reader_issues",
    Path(__file__).resolve().parent / "scan-html-reader-issues.py",
)
_scan = importlib.util.module_from_spec(_scan_spec)
assert _scan_spec and _scan_spec.loader
_scan_spec.loader.exec_module(_scan)
PATTERNS = _scan.PATTERNS
story_plain = _scan.story_plain
story_word_count = _scan.story_word_count

from hierarchy_html_rules import validate_no_reference_blob, validate_visible_copy  # noqa: E402

HTML_DIR = ROOT / "documents/plans/full-automation/html-site"

MOJIBAKE = re.compile(r"â€|â†|Â§|Ã|ï¿½")
RAW_MARKDOWN = re.compile(r"<li>\*\*[^*]+\*\*|<li>\[ \]|`python scripts/automation/audit")
BROKEN_TABLE = re.compile(r"\|------\||\| Link \| Why \|")
SPEC_LEAK = re.compile(
    r"## Concrete implementation|## Cross-links|Adversarial review|"
    r"Scope bleed:|Silent stop:|False complete:",
    re.I,
)
MIN_STORY = {
    "capabilities": 40,
    "chapters": 35,
    "branches": 25,
    "index": 20,
}


@dataclass
class AuditResult:
    blockers: dict[str, list[str]] = field(default_factory=lambda: defaultdict(list))
    warnings: dict[str, list[str]] = field(default_factory=lambda: defaultdict(list))

    def add(self, severity: str, kind: str, page: str) -> None:
        bucket = self.blockers if severity == "blocker" else self.warnings
        bucket[kind].append(page)

    @property
    def blocker_count(self) -> int:
        return sum(len(v) for v in self.blockers.values())

    @property
    def warning_count(self) -> int:
        return sum(len(v) for v in self.warnings.values())


def page_kind(rel: str) -> str:
    if rel == "index.html" or rel == "glossary.html":
        return "index"
    if rel.startswith("capabilities/"):
        return "capabilities"
    if rel.startswith("chapters/"):
        return "chapters"
    if rel.startswith("branches/"):
        return "branches"
    return "other"


def resolve_href(html_path: Path, href: str) -> Path | None:
    if not href or href.startswith(("http://", "https://", "mailto:", "#")):
        return None
    if href.startswith("/"):
        return HTML_DIR / href.lstrip("/")
    return (html_path.parent / href).resolve()


def audit(html_dir: Path) -> AuditResult:
    res = AuditResult()
    html_files = sorted(html_dir.rglob("*.html"))

    for f in html_files:
        rel = str(f.relative_to(html_dir)).replace("\\", "/")
        text = f.read_text(encoding="utf-8")
        kind = page_kind(rel)

        # Layout / assets
        if 'rel="stylesheet"' in text:
            m = re.search(r'href="([^"]+site\.css)"', text)
            if m:
                css = resolve_href(f, m.group(1))
                if css is None or not css.is_file():
                    res.add("blocker", "broken_css_path", rel)

        if "<main" not in text:
            res.add("blocker", "missing_main", rel)
        if "site-header" not in text:
            res.add("blocker", "missing_header", rel)

        # Index / glossary pages use different layout
        exempt_story = rel in ("index.html", "glossary.html", "branches/index.html")

        # Internal links
        for href in re.findall(r'href="([^"]+\.html[^"]*)"', text):
            target = resolve_href(f, href.split("#")[0])
            if target is not None and not target.is_file():
                res.add("blocker", "broken_link", f"{rel} -> {href}")
        for href in re.findall(r'href="([^"]+\.md[^"]*)"', text):
            target = resolve_href(f, href.split("#")[0])
            if target is not None and not target.is_file():
                res.add("blocker", "broken_link", f"{rel} -> {href}")

        # Story block
        if kind in MIN_STORY and not exempt_story and "story-block" not in text:
            res.add("blocker", "missing_story_block", rel)
        elif "story-block" in text:
            words = story_word_count(text)
            min_w = MIN_STORY.get(kind, 20)
            if words < min_w:
                res.add("blocker" if kind == "capabilities" else "warning", f"short_story_{words}w", rel)
            sp = story_plain(text)
            for name, pat in PATTERNS.items():
                if pat.search(sp):
                    res.add("blocker", name, rel)
            if '<span class="vision-ref">' in text:
                res.add("blocker", "unlinked_vision_ref", rel)

        # Publication rules
        for msg in validate_no_reference_blob(text):
            res.add("blocker", f"ref_blob:{msg[:40]}", rel)
        for msg in validate_visible_copy(text):
            if not msg.startswith("reference blob"):
                res.add("blocker", f"pub_meta:{msg[:40]}", rel)

        if kind == "capabilities":
            body_after_story = text.split("</div>", 1)[-1] if "story-block" in text else text
            detail = re.sub(r"<div class=\"story-block\".*?</div>", "", text, count=1, flags=re.S)
            if MOJIBAKE.search(detail):
                res.add("warning", "mojibake_encoding", rel)
            if RAW_MARKDOWN.search(detail):
                res.add("warning", "raw_markdown", rel)
            if BROKEN_TABLE.search(detail):
                res.add("warning", "broken_table", rel)
            if SPEC_LEAK.search(detail):
                res.add("warning", "spec_junk_in_body", rel)

        # Chapters: should not use wrong asset depth
        if kind == "chapters" and '../../assets/' in text:
            res.add("blocker", "chapter_wrong_css_depth", rel)

    return res


def print_report(res: AuditResult, total: int) -> None:
    print(f"READINESS AUDIT — {total} HTML pages")
    print(f"  BLOCKERS: {res.blocker_count} (must fix before 'ready to read')")
    print(f"  WARNINGS: {res.warning_count} (quality debt; reader can skim story)")
    print()

    if res.blockers:
        print("=== BLOCKERS ===")
        for kind, pages in sorted(res.blockers.items(), key=lambda x: -len(x[1])):
            print(f"  {kind}: {len(pages)}")
            for p in pages[:5]:
                print(f"    - {p}")
            if len(pages) > 5:
                print(f"    ... +{len(pages) - 5} more")
        print()

    if res.warnings:
        print("=== WARNINGS (detail sections) ===")
        for kind, pages in sorted(res.warnings.items(), key=lambda x: -len(x[1])):
            print(f"  {kind}: {len(pages)}")
            for p in pages[:3]:
                print(f"    - {p}")
            if len(pages) > 3:
                print(f"    ... +{len(pages) - 3} more")
        print()

    if res.blocker_count == 0:
        print("BLOCKERS: none — layout, links, and reader stories pass.")
    else:
        print("NOT READY: fix blockers above before calling the book reader-ready.")


def main() -> int:
    html_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else HTML_DIR
    if not html_dir.is_dir():
        print(f"Missing {html_dir}", file=sys.stderr)
        return 2
    total = len(list(html_dir.rglob("*.html")))
    res = audit(html_dir)
    print_report(res, total)
    return 1 if res.blocker_count else 0


if __name__ == "__main__":
    sys.exit(main())
