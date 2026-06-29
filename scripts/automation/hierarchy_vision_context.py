#!/usr/bin/env python3
"""Extract hierarchy tree lines from vision markdown for doc enrichment."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
VISION = ROOT / "documents" / "full-automation-vision-and-hierarchy.md"


def load_vision_lines() -> list[str]:
    if not VISION.is_file():
        return []
    return VISION.read_text(encoding="utf-8").splitlines()


def find_tree_context(item_id: str, lines: list[str]) -> str:
    """Find ASCII tree lines mentioning item_id (e.g. A2.4, D2.1.1)."""
    hits: list[str] = []
    for line in lines:
        if item_id in line and ("├──" in line or "└──" in line or "│" in line):
            hits.append(line.strip())
    return "\n".join(hits) if hits else ""


def section_for_branch(item_id: str) -> str:
    m = re.match(r"^([A-J])", item_id)
    if m:
        return {"A": "§3", "B": "§4", "C": "§5", "D": "§6", "E": "§7",
                "F": "§8", "G": "§9", "H": "§10", "I": "§11", "J": "§12"}.get(m.group(1), "")
    if item_id.startswith("INTRO"):
        return "§0–§1"
    if item_id.startswith("MASTER"):
        return "§2"
    if item_id.startswith("SEC-13"):
        return "§13"
    if item_id.startswith("SEC-14"):
        return "§14"
    if item_id.startswith("SEC-15"):
        return "§15"
    if item_id.startswith("SEC-17"):
        return "§17"
    if item_id.startswith("APP"):
        return "§18–§19"
    return ""
