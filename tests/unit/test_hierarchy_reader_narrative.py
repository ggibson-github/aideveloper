#!/usr/bin/env python3
"""Tests for human reader narrative generation."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts/automation"))

from hierarchy_html_parse import ParsedNode  # noqa: E402
from hierarchy_prose import ProseContext, load_vision_sections  # noqa: E402
from hierarchy_reader_narrative import build_reader_story_md, humanize_timeline_step  # noqa: E402


def test_a11_story_is_teaching_prose() -> None:
    ctx = ProseContext(vision_sections=load_vision_sections())
    node = ParsedNode(
        id="A1.1",
        slug="A1.1-test",
        title="goal_id parent_goal goal_type",
        branch="A",
        purpose="A1.1 defines goal_id parent_goal goal_type for the agent-driven expert system.",
    )
    story = build_reader_story_md(node, ctx, "Branch A — Pursuit & control plane")
    assert "Goal id" in story or "goal" in story.lower()
    assert "In practice, the system" not in story
    assert "[Vision §3" in story


def test_humanize_step_avoids_spec_jargon() -> None:
    node = ParsedNode(id="A1.1", slug="x", title="goal_id parent_goal goal_type", branch="A")
    step = "Define and implement goal_id per [Vision §3 — Branch A](branch.md)."
    out = humanize_timeline_step(step, node)
    assert "[[Vision" not in out
    assert "goal identity" in out.lower() or "goal id" in out.lower() or "Establish" in out
