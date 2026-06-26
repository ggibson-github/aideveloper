"""Tests for lane work order scripts."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_pull_ready_lists_character_lane():
    path = ROOT / "program" / "workstreams" / "character" / "lane.json"
    lane = json.loads(path.read_text(encoding="utf-8"))
    assert lane["status"] == "backlog"
    assert lane["lease"]["holder"] is None
