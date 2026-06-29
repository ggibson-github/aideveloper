#!/usr/bin/env python3
"""Unit tests for hierarchy reader prose normalization."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts/automation"))

from hierarchy_prose import (  # noqa: E402
    ProseContext,
    build_prose_context,
    compose_reader_narrative,
    critique_prose,
    load_vision_sections,
    normalize_step_md,
    render_prose_html,
)


def _ctx() -> ProseContext:
    return ProseContext(
        slug_by_id={"B1.1": "B1.1-s0-deterministic-mandatory-first"},
        slug_by_file={"B1.1-s0-deterministic-mandatory-first.md": "B1.1-s0-deterministic-mandatory-first"},
        vision_sections=load_vision_sections(ROOT / "documents/full-automation-vision-and-hierarchy.md"),
    )


def test_critique_flags_bare_vision_and_cursor_rules() -> None:
    text = "Implement as specified in vision §3. See ([deterministic-first](../../../.cursor/rules/deterministic-first.mdc))."
    issues = critique_prose(text)
    assert "bare vision § reference without link" in issues
    assert "cursor rule path link" in issues


def test_normalize_step_links_vision_and_s0() -> None:
    ctx = _ctx()
    step = "Implement **goal_id** as specified in vision §3."
    out = normalize_step_md(step, ctx, item_id="A1.1", title="goal_id")
    assert "§3" not in out or "[Vision" in out
    assert "**" not in out


def test_normalize_step_replaces_cursor_rule() -> None:
    ctx = _ctx()
    step = "Prefer S0 script ([deterministic-first](../../../.cursor/rules/deterministic-first.mdc))."
    out = normalize_step_md(step, ctx, item_id="A1.1", title="x")
    assert ".cursor/rules/" not in out
    assert "B1.1" in out or "Deterministic-first" in out


def test_render_prose_html_vision_link() -> None:
    ctx = _ctx()

    def noop(s: str, _d: int, **_kw) -> str:
        return s

    html_out = render_prose_html("Defined in vision §3.", ctx, 1, noop)
    assert "branches/A.html" in html_out
    assert "§3" in html_out


def test_render_prose_html_vision_section_zero_links_to_source() -> None:
    ctx = _ctx()

    def noop(s: str, _d: int, **_kw) -> str:
        return s

    md = (
        "See [Vision §0 — Executive summary]"
        "(../../full-automation-vision-and-hierarchy.md#0-executive-summary)."
    )
    html_out = render_prose_html(md, ctx, 1, noop)
    assert 'class="spec-link"' in html_out
    assert "full-automation-vision-and-hierarchy.md" in html_out
    assert "0-executive-summary" in html_out
    assert "vision-ref" not in html_out


def test_compose_reader_narrative_from_markdown() -> None:
    ctx = _ctx()

    def link(s: str, _d: int, **_kw) -> str:
        return s

    md = (
        "Every pursuit begins with a goal record.\n\n"
        "See [Vision §3 — Branch A — Pursuit & control plane]"
        "(../../full-automation-vision-and-hierarchy.md#3-branch-a-pursuit-control-plane)."
    )
    html_out = compose_reader_narrative(md, ctx, 1, link)
    assert "branches/A.html" in html_out
    assert "](.." not in html_out


def test_build_prose_context_from_plan_dir() -> None:
    out_dir = ROOT / "documents/plans/full-automation"
    if not out_dir.is_dir():
        return
    ctx = build_prose_context(out_dir)
    assert "A1.1" in ctx.slug_by_id
    assert "§3" in ctx.vision_sections
