#!/usr/bin/env python3
"""Verify HTML book site meets minimum completeness for print/export."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from hierarchy_completeness import list_leaf_paths  # noqa: E402
from hierarchy_html_parse import parse_markdown  # noqa: E402

MIN_READER_WORDS = 40
FORBIDDEN = ("[[Vision", ".cursor/rules/", "In practice, the system define")


def word_count(text: str) -> int:
    return len(re.findall(r"\w+", text))


def verify_html_dir(html_dir: Path) -> list[str]:
    errors: list[str] = []
    cap_dir = html_dir / "capabilities"
    if not cap_dir.is_dir():
        return [f"missing capabilities dir: {cap_dir}"]
    for html in cap_dir.glob("*.html"):
        text = html.read_text(encoding="utf-8")
        if "story-block" not in text:
            errors.append(f"{html.name}: missing story-block")
        for phrase in FORBIDDEN:
            if phrase.lower() in text.lower():
                errors.append(f"{html.name}: forbidden phrase {phrase!r}")
        story = re.search(r'class="story-block"[^>]*>(.*?)</div>', text, re.S)
        if story:
            plain = re.sub(r"<[^>]+>", " ", story.group(1))
            if word_count(plain) < MIN_READER_WORDS:
                errors.append(f"{html.name}: story too short ({word_count(plain)} words)")
    branch_dir = html_dir / "branches"
    for html in branch_dir.glob("*.html"):
        text = html.read_text(encoding="utf-8")
        if html.name != "index.html" and "cap-group" not in text and html.stem in "ABCDEFGHIJmeta":
            errors.append(f"branches/{html.name}: missing grouped sections (cap-group)")
        from hierarchy_html_rules import validate_no_reference_blob  # noqa: WPS433

        for msg in validate_no_reference_blob(text):
            errors.append(f"branches/{html.name}: {msg}")
    meta_path = branch_dir / "meta.html"
    if meta_path.is_file() and "reading-order-list" not in meta_path.read_text(encoding="utf-8"):
        errors.append("branches/meta.html: missing reading-order-list")
    chapters = html_dir / "chapters"
    chapter_count = len(list(chapters.glob("*.html"))) if chapters.is_dir() else 0
    if chapter_count < 60:
        errors.append(f"chapters/: expected group chapter pages, found {chapter_count}")
    return errors


def verify_markdown(out_dir: Path) -> list[str]:
    errors: list[str] = []
    for p in list_leaf_paths(out_dir):
        raw = p.read_text(encoding="utf-8")
        if "## Reader narrative" not in raw:
            errors.append(f"{p.name}: missing Reader narrative section")
            continue
        node = parse_markdown(p, raw)
        if word_count(node.reader_narrative) < MIN_READER_WORDS:
            errors.append(f"{p.name}: reader narrative too short")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--html-dir", default="documents/plans/full-automation/html-site")
    parser.add_argument("--output-dir", default="documents/plans/full-automation")
    args = parser.parse_args()
    html_dir = ROOT / args.html_dir
    out_dir = ROOT / args.output_dir
    errors = verify_html_dir(html_dir) + verify_markdown(out_dir)
    if errors:
        print(f"BOOK VERIFY FAILED ({len(errors)} issues):", file=sys.stderr)
        for e in errors[:30]:
            print(f"  - {e}", file=sys.stderr)
        if len(errors) > 30:
            print(f"  ... and {len(errors) - 30} more", file=sys.stderr)
        return 1

    audit_script = ROOT / "scripts/automation/audit-book-readiness.py"
    if audit_script.is_file():
        import subprocess

        rc = subprocess.call([sys.executable, str(audit_script), str(html_dir)])
        if rc != 0:
            print("BOOK VERIFY FAILED: readiness audit blockers (see above)", file=sys.stderr)
            return 1

    timeline_script = ROOT / "scripts/automation/audit-timeline-steps.py"
    if timeline_script.is_file():
        import subprocess

        rc = subprocess.call([sys.executable, str(timeline_script), str(html_dir)])
        if rc != 0:
            print("BOOK VERIFY FAILED: timeline audit (see above)", file=sys.stderr)
            return 1

    print("BOOK VERIFY PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
