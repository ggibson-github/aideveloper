#!/usr/bin/env python3
"""Unit tests for hierarchy HTML publication rules."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts/automation"))

from hierarchy_html_rules import (  # noqa: E402
    PublishRuleViolation,
    enforce_publish_rules,
    validate_no_publication_meta,
    validate_no_reference_blob,
    validate_site_config,
    validate_subject_only,
    validate_visible_copy,
)


def test_subject_only_rejects_certification_meta() -> None:
    text = "Certified for review at 99.6 quality score / 100."
    assert validate_subject_only(text)


def test_no_publication_meta_rejects_layout_commentary() -> None:
    text = "Diagrams and narratives lead; structured specifications live in linked data pages."
    hits = validate_no_publication_meta(text)
    assert len(hits) >= 2


def test_no_publication_meta_rejects_data_footnote_html() -> None:
    html = '<div class="footnotes"><p>Structured specifications: <a href="data/manifest.json">manifest.json</a></p></div>'
    assert validate_no_publication_meta(html)


def test_clean_subject_copy_passes() -> None:
    text = "From pursuit and routing through verification and governance — each plane owns a coherent slice."
    assert validate_visible_copy(text) == []


def test_site_config_rejects_publication_meta_in_explore_sub() -> None:
    site = {
        "explore_branches_sub": "Each plane is a chapter of the design. Diagrams and narratives lead; structured specifications live in linked data pages.",
    }
    violations = validate_site_config(site)
    assert any("explore_branches_sub" in loc for loc, _ in violations)


def test_site_config_accepts_subject_only_overlay() -> None:
    site = {
        "explore_branches_sub": "From pursuit and routing through verification and governance — each plane owns a coherent slice of autonomous operation.",
        "hero_lead": "A ten-plane expert system that pursues goals autonomously.",
    }
    assert validate_site_config(site) == []


def test_reference_blob_rejects_inline_reading_order() -> None:
    html = (
        '<div class="story-block"><p>Read in this order: INTRO-0 (§0), INTRO-1 (§1), MASTER (§2).</p></div>'
    )
    hits = validate_no_reference_blob(html)
    assert any("reading-order" in h for h in hits)


def test_reference_blob_passes_with_list() -> None:
    html = (
        '<div class="story-block"><p>Short intro.</p></div>'
        '<nav class="reading-order"><ol class="reading-order-list"><li><a href="x">INTRO-0</a></li></ol></nav>'
    )
    assert validate_no_reference_blob(html) == []


def test_enforce_publish_rules_raises() -> None:
    with pytest.raises(PublishRuleViolation):
        enforce_publish_rules([("index.html", "html layout commentary: contains 'linked data pages'")])


def test_public_behavior_steps_filters_doc_work_for_conceptual_nodes() -> None:
    from hierarchy_html_rules import is_conceptual_capability, public_behavior_steps

    assert is_conceptual_capability("INTRO-0", "meta")
    steps = [
        "Define and implement Executive summary per Vision §0.",
        "At H1, the operator supplies a spec or charter.",
        "Map `INTRO-0` to v2.14–v2.23 release row in SEC-15-index.md.",
        "Create or extend S0 script if behavior is file-derived.",
    ]
    out = public_behavior_steps(steps, item_id="INTRO-0", branch="meta")
    assert "Define and implement" not in " ".join(out)
    assert "SEC-15-index" not in " ".join(out)
    assert any("H1" in s for s in out)


def test_humanize_conceptual_step_avoids_pursuit_state_boilerplate() -> None:
    from hierarchy_html_parse import ParsedNode
    from hierarchy_reader_narrative import humanize_timeline_step

    node = ParsedNode(
        id="INTRO-0",
        slug="intro",
        title="Executive summary (§0)",
        branch="meta",
    )
    text = humanize_timeline_step(
        "Define and implement Executive summary (§0) per Vision §0.",
        node,
    )
    assert "pursuit and state records" not in text
    assert "Defines" in text or "expert system" in text
