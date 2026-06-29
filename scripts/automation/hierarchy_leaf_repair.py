#!/usr/bin/env python3
"""Repair hierarchy leaves truncated by bad behavior-section cleanup."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from hierarchy_completeness import item_id_from_path, list_leaf_paths, title_from_path  # noqa: E402
from hierarchy_leaf_builder import build_complete_leaf  # noqa: E402
from hierarchy_prose_editor import BEHAVIOR_HEADING, READER_HEADING, SECTION_END  # noqa: E402
from hierarchy_vision_context import load_vision_lines  # noqa: E402


def _section_text(text: str, heading: re.Pattern[str]) -> str:
    bounds = _bounds(text, heading)
    if not bounds:
        return ""
    start, end = bounds
    return text[start:end].strip()


def _bounds(text: str, heading: re.Pattern[str]) -> tuple[int, int] | None:
    m = heading.search(text)
    if not m:
        return None
    start = m.end()
    rest = text[start:]
    end_m = SECTION_END.search(rest)
    end = start + end_m.start() if end_m else len(text)
    return start, end


def _extract_after_hierarchy(full: str) -> str:
    """Return full markdown from end of hierarchy context through EOF."""
    m = re.search(r"## Hierarchy context\s*\n\n```[\s\S]*?```\s*\n", full)
    if not m:
        m = re.search(r"## Behavior / step logic", full)
        if not m:
            return ""
        return full[m.start() :]
    after_hier = full[m.end() :]
    beh = re.search(r"## Behavior / step logic\s*\n[\s\S]*?(?=\n```mermaid|\n## JSON|\n## Repo|\Z)", after_hier)
    if beh:
        after_hier = after_hier[: beh.start()] + after_hier[beh.end() :]
    return after_hier.lstrip("\n")


def repair_leaf(path: Path, vision_lines: list[str]) -> bool:
    text = path.read_text(encoding="utf-8")
    if "## Verification" in text and "```mermaid" in text:
        return False

    item_id = item_id_from_path(path, text)
    title = title_from_path(path, item_id)
    full = build_complete_leaf(item_id, title, vision_lines, pass_num=3)

    header_m = re.match(r"^([\s\S]*?)(?=## Reader narrative|## Purpose)", text)
    header = header_m.group(1).strip() + "\n\n" if header_m else ""

    reader = _section_text(text, READER_HEADING)
    reader_block = f"## Reader narrative\n{reader}\n\n" if reader else ""

    behavior = _section_text(text, BEHAVIOR_HEADING)
    if not behavior:
        behavior = _section_text(full, BEHAVIOR_HEADING)
    behavior_block = f"## Behavior / step logic\n{behavior}\n\n" if behavior else ""

    purpose_m = re.search(r"## Purpose[\s\S]*", full)
    if not purpose_m:
        return False
    purpose_through_hier = full[purpose_m.start() :]
    hier_m = re.search(
        r"(## Purpose[\s\S]*?## Hierarchy context\s*\n\n```[\s\S]*?```)\s*\n",
        purpose_through_hier,
    )
    if not hier_m:
        return False
    middle = hier_m.group(1) + "\n\n"
    tail = _extract_after_hierarchy(full)

    new_text = header + reader_block + middle + behavior_block + tail
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
        return True
    return False


def main() -> int:
    vision = load_vision_lines()
    repaired = 0
    for path in list_leaf_paths(ROOT / "documents/plans/full-automation"):
        if repair_leaf(path, vision):
            repaired += 1
    print(f"Repaired {repaired} truncated leaves")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
