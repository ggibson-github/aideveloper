#!/usr/bin/env python3
"""Validate workflow artifacts and journal/state consistency (v2 conformance)."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / "journal" / "state.json"
JOURNAL = ROOT / "journal" / "progress.md"
ERRORS: list[str] = []


def check(path: Path, label: str) -> None:
    if not path.is_file():
        ERRORS.append(f"Missing {label}: {path.relative_to(ROOT)}")


def validate_program(state: dict) -> None:
    program = state.get("program")
    if not program:
        return
    if state.get("mode") != "program":
        ERRORS.append("program object set but mode is not 'program'")
    manifest = program.get("integration_manifest")
    if manifest:
        check(ROOT / manifest, "integration manifest")
    graph = program.get("artifact_graph")
    if graph:
        check(ROOT / graph, "artifact graph")
    for ws in program.get("workstreams", []) or []:
        ws_dir = ROOT / "program" / "workstreams" / ws
        check(ws_dir / "lane.json", f"lane {ws}")
        check(ws_dir / "workstream.md", f"workstream {ws}")


def validate_task_card(path: Path) -> None:
    if not path.is_file():
        return
    text = path.read_text(encoding="utf-8")
    for section in ("## Acceptance criteria", "## Test command", "## Evidence"):
        if section.lower() not in text.lower():
            ERRORS.append(f"Task card missing {section}: {path.relative_to(ROOT)}")


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
        if state.get("last_verify") == "failed" and not state.get("model_escalation"):
            ERRORS.append("last_verify failed but model_escalation not set")
        validate_program(state)

        autopilot = state.get("autopilot") or {}
        if autopilot.get("active"):
            max_s = int(autopilot.get("max_steps_per_session") or 25)
            steps = int(autopilot.get("steps_this_session") or 0)
            if steps > max_s:
                ERRORS.append(
                    f"autopilot steps_this_session ({steps}) > max_steps_per_session ({max_s})"
                )

        na = str(state.get("next_action", ""))
        m = re.search(r"task\s+(\d+)", na, re.I)
        if m:
            num = m.group(1).zfill(3)
            validate_task_card(ROOT / "docs" / "tasks" / f"task-{num}.md")

    if JOURNAL.is_file() and STATE.is_file():
        journal = JOURNAL.read_text(encoding="utf-8")
        state = json.loads(STATE.read_text(encoding="utf-8"))
        na = state.get("next_action")
        if na and na not in journal:
            ERRORS.append("next_action in state.json not reflected in progress.md")

    route_script = ROOT / "scripts" / "route-tier.py"
    if route_script.is_file() and STATE.is_file():
        result = subprocess.run(
            [sys.executable, str(route_script), "--check"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            ERRORS.append("route-tier --check failed")
            if result.stderr:
                ERRORS.append(result.stderr.strip())

    if ERRORS:
        for e in ERRORS:
            print(f"ERROR: {e}", file=sys.stderr)
        return 1
    print("validate-workflow: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
