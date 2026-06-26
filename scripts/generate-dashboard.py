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
PROGRAM_WS = ROOT / "program" / "workstreams"


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
        f"- **pipeline_id:** {state.get('pipeline_id')}",
        f"- **completion_status:** {state.get('completion_status')}",
        "",
        "## Model routing",
        f"- **capability_class:** {state.get('capability_class')}",
        f"- **model_tier:** {state.get('model_tier')}",
        f"- **spawn_workers:** {state.get('spawn_workers')}",
        f"- **genius_session_recommended:** {state.get('genius_session_recommended')}",
        f"- **model_escalation:** {state.get('model_escalation')}",
        "",
        "## Autopilot",
    ]
    ap = state.get("autopilot") or {}
    lines.extend(
        [
            f"- **active:** {ap.get('active')}",
            f"- **steps_this_session:** {ap.get('steps_this_session')}",
            f"- **max_steps_per_session:** {ap.get('max_steps_per_session')}",
            f"- **stopped_reason:** {ap.get('stopped_reason')}",
            "",
            "## Gates and blockers",
        ]
    )
    lines.extend(
        [
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
    )
    lines.extend(stale_lines or ["- (none)"])
    lines.extend(["", "## Allowed reads", f"- {state.get('allowed_reads')}", ""])

    program = state.get("program")
    if program:
        lines.extend(
            [
                "## Program",
                f"- **program_id:** {program.get('program_id')}",
                f"- **milestone:** {program.get('milestone')}",
                f"- **integration_manifest:** {program.get('integration_manifest')}",
                f"- **gates_pending_program:** {program.get('gates_pending_program')}",
                f"- **workstreams:** {program.get('workstreams')}",
                "",
            ]
        )
        for ws in program.get("workstreams", []) or []:
            lane_path = PROGRAM_WS / ws / "lane.json"
            if lane_path.is_file():
                lane = json.loads(lane_path.read_text(encoding="utf-8"))
                lines.append(
                    f"- **lane {ws}:** status={lane.get('status')} "
                    f"task={lane.get('current_task')} blocked={lane.get('blocked_on')}"
                )
        lines.append("")

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
