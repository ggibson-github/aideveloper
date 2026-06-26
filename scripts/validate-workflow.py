#!/usr/bin/env python3
"""Validate workflow artifacts and journal/state consistency (v2 conformance)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / "journal" / "state.json"
JOURNAL = ROOT / "journal" / "progress.md"
ERRORS: list[str] = []


def check(path: Path, label: str) -> None:
    if not path.is_file():
        ERRORS.append(f"Missing {label}: {path.relative_to(ROOT)}")


def main() -> int:
    check(STATE, "state.json")
    check(JOURNAL, "progress.md")
    check(ROOT / "docs" / "facts" / "INDEX.md", "facts INDEX")
    check(ROOT / "docs" / "manifest" / "staleness.json", "staleness manifest")

    if STATE.is_file():
        state = json.loads(STATE.read_text(encoding="utf-8"))
        if state.get("version") != 2:
            ERRORS.append("state.json version should be 2")
        bq = state.get("blocking_questions") or []
        phase = state.get("phase", "")
        if bq and phase not in ("not_started", "parsed"):
            ERRORS.append(f"blocking_questions non-empty during phase {phase}")
        if state.get("evidence_required") and not state.get("evidence_files"):
            ERRORS.append("evidence_required but no evidence_files")

    if JOURNAL.is_file() and STATE.is_file():
        journal = JOURNAL.read_text(encoding="utf-8")
        state = json.loads(STATE.read_text(encoding="utf-8"))
        na = state.get("next_action")
        if na and na not in journal:
            ERRORS.append("next_action in state.json not reflected in progress.md")

    if ERRORS:
        for e in ERRORS:
            print(f"ERROR: {e}", file=sys.stderr)
        return 1
    print("validate-workflow: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
