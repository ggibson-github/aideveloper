"""Tests for check-pipeline-blocked.py."""

import json
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CHECK = ROOT / "scripts" / "automation" / "check-pipeline-blocked.py"


def _load_mod():
    spec = importlib.util.spec_from_file_location("check_blocked", CHECK)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _base_state() -> dict:
    return json.loads((ROOT / "journal" / "state.json").read_text(encoding="utf-8"))


def test_ready_on_default_state():
    mod = _load_mod()
    blocked, _ = mod.is_blocked(_base_state())
    assert not blocked


def test_blocked_on_gates_pending():
    mod = _load_mod()
    state = _base_state()
    state["gates_pending"] = ["hld_approved"]
    blocked, reason = mod.is_blocked(state)
    assert blocked
    assert "gates_pending" in reason


def test_blocked_on_wait_for():
    mod = _load_mod()
    state = _base_state()
    state["next_action"] = "wait for HLD approval"
    blocked, reason = mod.is_blocked(state)
    assert blocked
    assert "wait for" in reason


def test_blocked_on_blocking_questions():
    mod = _load_mod()
    state = _base_state()
    state["blocking_questions"] = ["What database?"]
    blocked, _ = mod.is_blocked(state)
    assert blocked


def test_blocked_on_max_steps():
    mod = _load_mod()
    state = _base_state()
    state["autopilot"] = {
        "active": True,
        "max_steps_per_session": 5,
        "steps_this_session": 5,
        "stopped_reason": None,
    }
    blocked, reason = mod.is_blocked(state)
    assert blocked
    assert "max_steps" in reason
