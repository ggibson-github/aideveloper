#!/usr/bin/env python3
"""Repair or validate journal/progress.md vs journal/state.json (stdlib only)."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE_PATH = ROOT / "journal" / "state.json"
JOURNAL_PATH = ROOT / "journal" / "progress.md"

FIELD_MAP = {
    "Spec file": "spec_file",
    "Mode": "mode",
    "Current phase": "phase",
    "Current feature id": "feature_id",
    "Repo URL": "repo_url",
    "Current branch": "current_branch",
    "Last completed": "last_completed",
    "Next action": "next_action",
    "Blockers": "blockers",
    "Pause reason / Delay": "pause_reason",
    "Last failure / Retry state": "last_failure",
    "Completion status": "completion_status",
    "Last session summary": "last_session_summary",
}


def parse_journal_field(text: str, field: str) -> str | None:
    pattern = re.compile(rf"^\s*-\s*\*\*{re.escape(field)}:\*\*\s*(.*)$", re.MULTILINE)
    m = pattern.search(text)
    if not m:
        return None
    value = m.group(1).strip()
    if value.startswith("(") and "optional" in value.lower():
        return None
    if value.lower() in ("none", "(none)", "(none — must be empty to proceed past spec/hld)"):
        return None
    return value


def main() -> int:
    if not JOURNAL_PATH.is_file():
        print("No journal/progress.md", file=sys.stderr)
        return 1

    journal_text = JOURNAL_PATH.read_text(encoding="utf-8")
    state: dict = {}
    if STATE_PATH.is_file():
        state = json.loads(STATE_PATH.read_text(encoding="utf-8"))

    for md_field, json_key in FIELD_MAP.items():
        val = parse_journal_field(journal_text, md_field)
        if val is not None:
            if json_key == "feature_id" and val.startswith("("):
                continue
            state[json_key] = val

    ctx = parse_journal_field(journal_text, "Context files")
    if ctx and not ctx.startswith("("):
        paths = [p.strip() for p in re.split(r"[,;]", ctx) if p.strip() and "/" in p]
        if paths:
            state["context_files"] = paths

    state["version"] = 2
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    print(f"Synced {STATE_PATH.relative_to(ROOT)} from journal")
    return 0


if __name__ == "__main__":
    sys.exit(main())
