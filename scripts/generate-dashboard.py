#!/usr/bin/env python3
"""Generate docs/operator/dashboard.md and refresh STATUS.md from state.json."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / "journal" / "state.json"
STALE = ROOT / "docs" / "manifest" / "staleness.json"
DASH = ROOT / "docs" / "operator" / "dashboard.md"
STATUS = ROOT / "STATUS.md"


def main() -> int:
    state = {}
    if STATE.is_file():
        state = json.loads(STATE.read_text(encoding="utf-8"))

    stale_lines = []
    if STALE.is_file():
        data = json.loads(STALE.read_text(encoding="utf-8"))
        for node_id, info in (data.get("stale") or {}).items():
            if info.get("stale"):
                stale_lines.append(f"- **{node_id}:** {info.get('reason', 'stale')}")

    lines = [
        "# Operator dashboard",
        "",
        f"_Generated {date.today().isoformat()}_",
        "",
        "## Pipeline",
        f"- **next_action:** {state.get('next_action')}",
        f"- **phase:** {state.get('phase')}",
        f"- **mode:** {state.get('mode')}",
        f"- **completion_status:** {state.get('completion_status')}",
        "",
        "## Gates and blockers",
        f"- **gates_pending:** {state.get('gates_pending')}",
        f"- **blocking_questions:** {state.get('blocking_questions')}",
        f"- **blockers:** {state.get('blockers')}",
        "",
        "## Verify",
        f"- **last_verify:** {state.get('last_verify')}",
        f"- **evidence_required:** {state.get('evidence_required')}",
        f"- **evidence_files:** {state.get('evidence_files')}",
        "",
        "## Stale artifacts",
    ]
    lines.extend(stale_lines or ["- (none)"])
    lines.extend(["", "## Allowed reads", f"- {state.get('allowed_reads')}", ""])

    DASH.parent.mkdir(parents=True, exist_ok=True)
    DASH.write_text("\n".join(lines), encoding="utf-8")

    summary = state.get("last_session_summary") or (
        f"Next: {state.get('next_action')}. See dashboard for gates/blockers."
    )
    STATUS.write_text(summary + "\n", encoding="utf-8")
    print(f"Wrote {DASH.relative_to(ROOT)} and {STATUS.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
