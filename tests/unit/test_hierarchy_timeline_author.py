#!/usr/bin/env python3
"""Unit tests for timeline step authoring from reader narratives."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts/automation"))

from hierarchy_timeline_author import steps_from_narrative  # noqa: E402


A1_1_NARRATIVE = """\
Every pursuit in the expert system begins with a goal record that can be found again after restarts, nested under the right parent, and classified by type. This capability defines the three identity fields that make that possible: a unique goal_id, an optional parent_goal for tree structure, and goal_type (app, feature, milestone, or company_ops).

The type enum is not cosmetic. It tells preflight, routing, and verification which contracts apply—a milestone goal may require manifest approval while a feature goal binds to task cards and evidence paths. Nesting via parent_goal lets a program decompose into parallel streams without losing roll-up status at H3.

Operators set these fields at H1 when approving a plan; afterward the conductor and S0 scripts maintain them through dual-write to journal and state.json. If identity drifts (duplicate ids, wrong parent), pursuit turns attach evidence to the wrong scope and goal_verify cannot succeed. See Vision §3 for how the goal model anchors Plane A."""


def test_steps_from_narrative_a1_1_not_generic() -> None:
    steps = steps_from_narrative(
        A1_1_NARRATIVE,
        item_id="A1.1",
        title="goal_id parent_goal goal_type",
        branch="A",
    )
    assert len(steps) >= 3
    joined = " ".join(steps).lower()
    assert "define and implement" not in joined
    assert "pursuit and state records" not in joined
    assert any("goal" in s.lower() or "h1" in s.lower() for s in steps)


def test_steps_from_intro_conceptual() -> None:
    intro = """\
At H1, the operator supplies a spec or charter; the approved plan reflects this summary—north star, scope, and minimal HITL (H1/H2/H3).
All pursuit and plane specs assume three structural shifts: always-on pursuit until goals verify, parallel product and self-improvement work, and template-packs at company scale."""
    steps = steps_from_narrative(
        intro,
        item_id="INTRO-0",
        title="Executive summary (§0)",
        branch="meta",
    )
    assert len(steps) >= 2
    assert "sec-15" not in " ".join(steps).lower()
