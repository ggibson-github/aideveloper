#!/usr/bin/env python3
"""Check whether pipeline can advance (S0). Exit 0 = run, 1 = blocked."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
STATE = ROOT / "journal" / "state.json"


def is_blocked(state: dict) -> tuple[bool, str]:
    if state.get("completion_status") == "done":
        return True, "completion_status is done"
    na = str(state.get("next_action") or "").strip()
    if not na or na.lower() == "done":
        return True, "next_action empty or done"
    if na.startswith("wait for"):
        return True, f"gate or wait: {na}"
    bq = state.get("blocking_questions") or []
    if bq:
        return True, f"blocking_questions: {bq}"
    gates = state.get("gates_pending") or []
    if gates:
        return True, f"gates_pending: {gates}"
    program = state.get("program") or {}
    pg = program.get("gates_pending_program") or []
    if pg:
        return True, f"gates_pending_program: {pg}"
    blockers = str(state.get("blockers") or "none").strip().lower()
    if blockers and blockers != "none":
        return True, f"blockers: {state.get('blockers')}"
    if state.get("pause_reason"):
        return True, f"pause_reason: {state.get('pause_reason')}"
    if state.get("evidence_required") and state.get("last_verify") != "passed":
        return True, "evidence_required but not verified"
    autopilot = state.get("autopilot") or {}
    max_steps = int(autopilot.get("max_steps_per_session") or 25)
    steps = int(autopilot.get("steps_this_session") or 0)
    if autopilot.get("active") and steps >= max_steps:
        return True, f"autopilot max_steps_per_session ({max_steps}) reached"
    return False, ""


def main() -> int:
    if not STATE.is_file():
        print("No state.json", file=sys.stderr)
        return 1
    state = json.loads(STATE.read_text(encoding="utf-8"))
    blocked, reason = is_blocked(state)
    if blocked:
        print(f"BLOCKED: {reason}")
        return 1
    print(f"READY: next_action={state.get('next_action')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
