"""Autopilot state and validate-workflow acceptance."""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STATE = ROOT / "journal" / "state.json"
VALIDATE = ROOT / "scripts" / "validate-workflow.py"


def test_state_has_autopilot_block():
    state = json.loads(STATE.read_text(encoding="utf-8"))
    ap = state.get("autopilot")
    assert ap is not None
    assert "active" in ap
    assert "max_steps_per_session" in ap


def test_validate_workflow_ok_with_autopilot():
    result = subprocess.run(
        [sys.executable, str(VALIDATE)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
