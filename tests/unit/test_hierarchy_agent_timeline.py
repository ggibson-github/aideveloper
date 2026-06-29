#!/usr/bin/env python3
"""Unit tests for hierarchy_agent_timeline CLI helpers."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts/automation"))

from hierarchy_agent_timeline import (  # noqa: E402
    critique_steps,
    parse_steps_from_agent_output,
    render_timeline_prompt,
)


def test_parse_steps_from_numbered_output() -> None:
    text = """1. Preflight loads goal_id and parent_goal from state.json before routing.
2. Conductor dual-writes identity fields to journal and state on H1 approval.
3. Workers inherit goal_type so verification contracts match pursuit scope.
4. On duplicate goal_id, H2 blocks the turn until identity is reconciled."""
    steps = parse_steps_from_agent_output(text)
    assert len(steps) == 4
    assert steps[0].startswith("Preflight")


def test_parse_steps_ignores_markdown_noise() -> None:
    text = """Here are the steps:

1. First step with enough characters to pass the filter.
2. Second step with enough characters to pass the filter.
3. Third step with enough characters to pass the filter.
"""
    assert len(parse_steps_from_agent_output(text)) == 3


def test_critique_flags_generic() -> None:
    issues = critique_steps(
        [
            "Define and implement goal identity in the hierarchy leaf.",
            "Second operational step with sufficient length here.",
            "Third operational step with sufficient length here.",
        ]
    )
    assert any("generic" in i for i in issues)


def test_render_timeline_prompt_includes_reader() -> None:
    brief = {
        "item_id": "A1.1",
        "title": "goal identity",
        "vision_excerpt": "Goals anchor pursuit.",
        "group_id": "A1",
        "group_title": "Goal model",
        "branch": "A",
        "branch_title": "Pursuit core",
        "siblings": ["A1.2"],
        "path": "documents/plans/full-automation/A1.1-foo.md",
        "reader_excerpt": "Every pursuit begins with goal_id.",
    }
    prompt = render_timeline_prompt(brief)
    assert "A1.1" in prompt
    assert "Every pursuit begins" in prompt
    assert "numbered steps" in prompt.lower()
