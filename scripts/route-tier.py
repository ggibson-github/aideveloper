#!/usr/bin/env python3
"""Map next_action to capability class, model tier, and spawn_workers from model-policy.json."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / "journal" / "state.json"
POLICY = ROOT / "docs" / "operator" / "model-policy.json"

IMPLEMENT_PREFIX = "implement-feature"
ORCHESTRATE_PROGRAM = "orchestrate-program"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def match_routing(next_action: str, routing: dict) -> dict | None:
    na = next_action or ""
    if na in routing:
        return routing[na]
    for key, val in routing.items():
        if key == "wait for":
            if na.startswith("wait for"):
                return val
        elif na.startswith(key):
            return val
    if IMPLEMENT_PREFIX in na:
        return routing.get(IMPLEMENT_PREFIX)
    if ORCHESTRATE_PROGRAM in na:
        return routing.get(ORCHESTRATE_PROGRAM)
    return None


def route(next_action: str, policy: dict, state: dict) -> dict:
    routing = policy.get("routing_by_next_action", {})
    matched = match_routing(next_action, routing)
    if not matched:
        matched = {"class": "S3", "tier": "genius", "spawn_workers": False}

    tier = matched.get("tier")
    genius_recommended = tier == "genius" or matched.get("class") in ("S3", "S4")

    if state.get("model_escalation"):
        matched = dict(matched)
        matched["class"] = policy.get("escalation", {}).get("on_verify_failure", {}).get(
            "set_class", "S4"
        )
        matched["tier"] = "genius"
        matched["spawn_workers"] = False
        genius_recommended = True

    subagent_roles = policy.get("subagent_roles", {})
    subagent_models = {}
    for role, cfg in subagent_roles.items():
        subagent_models[role] = cfg.get("tier") or "economy"

    return {
        "capability_class": matched.get("class"),
        "model_tier": matched.get("tier"),
        "spawn_workers": bool(matched.get("spawn_workers")),
        "genius_session_recommended": genius_recommended,
        "subagent_models": subagent_models,
    }


def apply_to_state(state: dict, routed: dict) -> dict:
    state = dict(state)
    for key in (
        "capability_class",
        "model_tier",
        "spawn_workers",
        "genius_session_recommended",
        "subagent_models",
    ):
        if key in routed:
            state[key] = routed[key]
    return state


def check_state(state: dict, routed: dict) -> list[str]:
    errors = []
    for key in ("capability_class", "model_tier", "spawn_workers"):
        if state.get(key) != routed.get(key):
            errors.append(
                f"state.{key}={state.get(key)!r} expected {routed.get(key)!r} for next_action"
            )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Route model tier from next_action")
    parser.add_argument("--apply", action="store_true", help="Write routed fields to state.json")
    parser.add_argument("--check", action="store_true", help="Validate state matches routing")
    parser.add_argument("--json", action="store_true", help="Print routed JSON")
    args = parser.parse_args()

    if not POLICY.is_file():
        print(f"Missing {POLICY}", file=sys.stderr)
        return 1

    policy = load_json(POLICY)
    state = load_json(STATE) if STATE.is_file() else {}
    next_action = state.get("next_action", "")
    routed = route(next_action, policy, state)

    if args.json or (not args.apply and not args.check):
        print(json.dumps(routed, indent=2))

    if args.check:
        errors = check_state(state, routed)
        if errors:
            for e in errors:
                print(f"ERROR: {e}", file=sys.stderr)
            return 1
        print("route-tier --check: OK")
        return 0

    if args.apply:
        if not STATE.is_file():
            print("No state.json", file=sys.stderr)
            return 1
        new_state = apply_to_state(state, routed)
        STATE.write_text(json.dumps(new_state, indent=2) + "\n", encoding="utf-8")
        print(f"Updated {STATE.relative_to(ROOT)}")
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
