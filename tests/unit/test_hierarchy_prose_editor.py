#!/usr/bin/env python3
"""Unit tests for prose editor reader-narrative preservation."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts/automation"))

from hierarchy_prose import build_prose_context  # noqa: E402
from hierarchy_prose_editor import edit_leaf_markdown  # noqa: E402
from hierarchy_reader_narrative import (  # noqa: E402
    MIN_READER_NARRATIVE_WORDS,
    should_preserve_reader_narrative,
)


def test_should_preserve_agent_marked_prose() -> None:
    text = "<!-- prose-source: agent meta 2026-06-28 -->\n\nShort but protected."
    assert should_preserve_reader_narrative(text)


def test_should_preserve_long_narrative_without_marker() -> None:
    text = " ".join(["substantive"] * MIN_READER_NARRATIVE_WORDS)
    assert should_preserve_reader_narrative(text)


def test_should_not_preserve_empty_or_tiny() -> None:
    assert not should_preserve_reader_narrative("")
    assert not should_preserve_reader_narrative("Too short.")


def test_prose_editor_does_not_clobber_substantive_reader_narrative() -> None:
    original_body = (
        "The transistor manifest schema is the contract that makes generator workflows "
        "machine-checkable instead of prose-only. Every block under docs/platform/transistors/ "
        "declares id, version, capability_id, class, inputs, outputs, preconditions, executor, "
        "verify, and promotion provenance back to the platform queue."
    )
    md = f"""# E6.2: test

## Reader narrative

{original_body}

## Purpose

E6.2 defines test for the agent-driven expert system.
"""
    tmp_dir = ROOT / "documents/plans/full-automation/tmp/prose-editor-test"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    path = tmp_dir / "E6.2-test.md"
    try:
        path.write_text(md, encoding="utf-8")
        ctx = build_prose_context(ROOT / "documents/plans/full-automation")
        new_text, _changes, _ = edit_leaf_markdown(path, ctx, allow_reader_overwrite=True)
        assert original_body in new_text
        reader_block = new_text.split("## Reader narrative")[1].split("## Purpose")[0]
        assert "This section is part of" not in reader_block
    finally:
        if path.exists():
            path.unlink()


def test_prose_editor_skips_reader_overwrite_when_disabled() -> None:
    md = """# X1.1: test

## Reader narrative

One line only.

## Purpose

X1.1 defines test.
"""
    tmp_dir = ROOT / "documents/plans/full-automation/tmp/prose-editor-test"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    path = tmp_dir / "X1.1-test.md"
    try:
        path.write_text(md, encoding="utf-8")
        ctx = build_prose_context(ROOT / "documents/plans/full-automation")
        new_text, _changes, _ = edit_leaf_markdown(path, ctx, allow_reader_overwrite=False)
        assert "One line only." in new_text
        assert "specifies one contract in the expert system" not in new_text
    finally:
        if path.exists():
            path.unlink()
