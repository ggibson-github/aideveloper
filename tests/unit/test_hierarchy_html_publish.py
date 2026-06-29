#!/usr/bin/env python3
"""Unit tests for hierarchy HTML publish paths and chapter prose."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts/automation"))

from hierarchy_html_parse import ParsedNode  # noqa: E402
from hierarchy_reader_narrative import build_chapter_story_md  # noqa: E402


def rel_href(from_dir_depth: int, target: str) -> str:
    return ("../" * from_dir_depth if from_dir_depth else "") + target


CHAPTER_DEPTH = 1


def test_chapter_depth_is_one() -> None:
    assert CHAPTER_DEPTH == 1
    assert rel_href(CHAPTER_DEPTH, "assets/css/site.css") == "../assets/css/site.css"


def test_chapter_story_uses_single_leaf_reader_narrative() -> None:
    node = ParsedNode(
        id="INTRO-0",
        slug="INTRO-0-executive-summary---0",
        title="Executive summary",
        branch="meta",
        reader_narrative=(
            "<!-- prose-source: agent meta 2026-06-28 -->\n\n"
            "Today's harness is a verified delivery system with conductor, state machine, "
            "evidence paths, and autopilot-until-blocked semantics across the full SDLC pipeline. "
            "The target architecture replaces burst-and-wait Continue loops with goal-directed "
            "pursuit that runs until verification succeeds or a defined stop reason fires."
        ),
    )
    story = build_chapter_story_md("INTRO-0", [node], "Front matter", branch_id="meta")
    assert "verified delivery system" in story
    assert "contains 1 sections" not in story


def test_chapter_story_meta_multi_leaf_uses_intro_not_blob() -> None:
    nodes = [
        ParsedNode(
            id=f"SEC-15-v2.{i}",
            slug=f"s{i}",
            title=f"r{i}",
            branch="meta",
            reader_narrative=" ".join([f"Release v2.{i} adds goal model and verify hooks."] * 6),
        )
        for i in range(14, 17)
    ]
    story = build_chapter_story_md("SEC-15", nodes, "Roadmap", branch_id="meta")
    assert "additive releases" in story.lower()
    assert "contains 3 sections" not in story
