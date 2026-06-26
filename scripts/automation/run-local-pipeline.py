#!/usr/bin/env python3
"""Local pipeline driver: loop until blocked using Cursor SDK (local runtime).

Requires: pip install cursor-sdk, CURSOR_API_KEY in environment.
Runs on your PC against project cwd — not Cloud Agents.

Usage:
  python scripts/automation/run-local-pipeline.py
  python scripts/automation/run-local-pipeline.py --dry-run
  python scripts/automation/run-local-pipeline.py --max-iterations 10
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
STATE = ROOT / "journal" / "state.json"
POLICY = ROOT / "docs" / "operator" / "model-policy.json"
PROMPT_FILE = ROOT / "docs" / "automation" / "local-autopilot-prompt.md"
CHECK = ROOT / "scripts" / "automation" / "check-pipeline-blocked.py"
ROUTE = ROOT / "scripts" / "route-tier.py"
GEN_DASH = ROOT / "scripts" / "generate-dashboard.py"


def load_state() -> dict:
    return json.loads(STATE.read_text(encoding="utf-8"))


def save_state(state: dict) -> None:
    STATE.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")


def default_model() -> str:
    env = os.environ.get("AUTOPILOT_MODEL")
    if env:
        return env
    if POLICY.is_file():
        policy = json.loads(POLICY.read_text(encoding="utf-8"))
        models = (policy.get("tiers") or {}).get("genius", {}).get("cursor_models") or []
        if models:
            return models[0]
    return "composer-2.5"


def default_max_steps() -> int:
    if POLICY.is_file():
        policy = json.loads(POLICY.read_text(encoding="utf-8"))
        ap = policy.get("autopilot") or {}
        return int(ap.get("default_max_steps") or 25)
    return 25


def run_check() -> tuple[bool, str]:
    result = subprocess.run(
        [sys.executable, str(CHECK)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    out = (result.stdout or "") + (result.stderr or "")
    if result.returncode != 0:
        line = out.strip().splitlines()[-1] if out.strip() else "blocked"
        return True, line
    return False, out.strip()


def build_prompt(state: dict) -> str:
    base = PROMPT_FILE.read_text(encoding="utf-8") if PROMPT_FILE.is_file() else ""
    return (
        base
        + "\n\n---\n\n"
        + f"Current next_action: {state.get('next_action')}\n"
        + f"mode: {state.get('mode')}\n"
        + "Execute ONE pipeline step (continue skill). Spawn subagents when spawn_workers is true. "
        + "Dual-write journal + state. Increment autopilot.steps_this_session."
    )


def sdk_iteration(prompt: str, model: str) -> int:
    try:
        from cursor_sdk import Agent, AgentOptions, LocalAgentOptions
    except ImportError:
        print(
            "cursor-sdk not installed. Run: pip install cursor-sdk\n"
            "Or use /autopilot in Cursor Agents Window (local, no SDK).",
            file=sys.stderr,
        )
        return 2

    api_key = os.environ.get("CURSOR_API_KEY")
    if not api_key:
        print("Set CURSOR_API_KEY for SDK local runs.", file=sys.stderr)
        return 2

    result = Agent.prompt(
        prompt,
        AgentOptions(
            api_key=api_key,
            model=model,
            local=LocalAgentOptions(cwd=str(ROOT)),
        ),
    )
    print(f"SDK status: {result.status}")
    if result.result:
        text = result.result
        print(text[:2000] + ("..." if len(text) > 2000 else ""))
    return 0 if result.status == "completed" else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Local autopilot SDK loop")
    parser.add_argument("--dry-run", action="store_true", help="Only check blocked/ready")
    parser.add_argument("--max-iterations", type=int, default=None)
    parser.add_argument("--model", default=None, help="Parent model id (default: policy genius tier)")
    args = parser.parse_args()

    if not STATE.is_file():
        print("Missing journal/state.json", file=sys.stderr)
        return 1

    max_iter = args.max_iterations or default_max_steps()
    model = args.model or default_model()

    state = load_state()
    autopilot = state.get("autopilot") or {}
    autopilot["active"] = True
    autopilot["max_steps_per_session"] = max_iter
    autopilot["steps_this_session"] = 0
    autopilot["stopped_reason"] = None
    state["autopilot"] = autopilot
    save_state(state)

    iterations = 0
    while iterations < max_iter:
        blocked, reason = run_check()
        if blocked:
            print(reason)
            state = load_state()
            ap = state.setdefault("autopilot", {})
            ap["active"] = False
            ap["stopped_reason"] = reason.replace("BLOCKED: ", "")
            save_state(state)
            if GEN_DASH.is_file():
                subprocess.run([sys.executable, str(GEN_DASH)], cwd=ROOT)
            return 0

        if args.dry_run:
            print("READY (dry-run)")
            return 0

        state = load_state()
        prompt = build_prompt(state)
        code = sdk_iteration(prompt, model)
        if code == 2:
            state = load_state()
            state.setdefault("autopilot", {})["active"] = False
            save_state(state)
            return 2
        if code != 0:
            print("SDK iteration failed", file=sys.stderr)
            state = load_state()
            state.setdefault("autopilot", {})["active"] = False
            state["autopilot"]["stopped_reason"] = "sdk_iteration_failed"
            save_state(state)
            return 1

        subprocess.run([sys.executable, str(ROUTE), "--apply"], cwd=ROOT)
        state = load_state()
        ap = state.setdefault("autopilot", {})
        ap["steps_this_session"] = int(ap.get("steps_this_session") or 0) + 1
        save_state(state)
        iterations += 1
        print(f"Completed iteration {iterations}/{max_iter}")

    state = load_state()
    state.setdefault("autopilot", {})["active"] = False
    state["autopilot"]["stopped_reason"] = "max_iterations reached"
    save_state(state)
    subprocess.run([sys.executable, str(GEN_DASH)], cwd=ROOT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
