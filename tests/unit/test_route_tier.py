"""Tests for route-tier.py."""

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
ROUTE = ROOT / "scripts" / "route-tier.py"
POLICY = ROOT / "docs" / "operator" / "model-policy.json"


def _load_route_module():
    import importlib.util

    spec = importlib.util.spec_from_file_location("route_tier", ROUTE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_route_spec_parser_is_s3_genius():
    mod = _load_route_module()
    policy = json.loads(POLICY.read_text(encoding="utf-8"))
    routed = mod.route("run spec-parser", policy, {})
    assert routed["capability_class"] == "S3"
    assert routed["model_tier"] == "genius"
    assert routed["spawn_workers"] is False


def test_route_implement_spawns_workers():
    mod = _load_route_module()
    policy = json.loads(POLICY.read_text(encoding="utf-8"))
    routed = mod.route("implement-feature (task 1/3)", policy, {})
    assert routed["capability_class"] == "S1"
    assert routed["spawn_workers"] is True


def test_route_escalation_on_failure():
    mod = _load_route_module()
    policy = json.loads(POLICY.read_text(encoding="utf-8"))
    routed = mod.route("implement-feature (task 1/3)", policy, {"model_escalation": True})
    assert routed["capability_class"] == "S4"
    assert routed["model_tier"] == "genius"
