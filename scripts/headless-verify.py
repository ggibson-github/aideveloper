#!/usr/bin/env python3
"""Headless verify stub: read state.json, run verify command if configured, write evidence."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / "journal" / "state.json"
EVIDENCE = ROOT / "evidence"


def find_task_card(state: dict) -> Path | None:
    na = str(state.get("next_action", ""))
    import re

    m = re.search(r"task\s+(\d+)", na, re.I)
    if not m:
        return None
    num = m.group(1).zfill(3)
    path = ROOT / "docs" / "tasks" / f"task-{num}.md"
    return path if path.is_file() else None


def extract_test_command(card_text: str) -> str | None:
    for line in card_text.splitlines():
        if line.strip().lower().startswith("## test command"):
            continue
        if "`" in line and ("pytest" in line or "npm" in line or "python" in line):
            return line.strip().strip("`")
    return None


def main() -> int:
    if not STATE.is_file():
        print("No state.json", file=sys.stderr)
        return 1

    state = json.loads(STATE.read_text(encoding="utf-8"))
    card = find_task_card(state)
    cmd = None
    log_name = "headless-verify.log"

    if card:
        cmd = extract_test_command(card.read_text(encoding="utf-8"))
        log_name = f"task-{card.stem.split('-')[-1]}-test.log"

    if not cmd:
        print("No test command found; writing skip log")
        EVIDENCE.mkdir(parents=True, exist_ok=True)
        (EVIDENCE / log_name).write_text("SKIP: no test command\n", encoding="utf-8")
        return 0

    EVIDENCE.mkdir(parents=True, exist_ok=True)
    log_path = EVIDENCE / log_name
    result = subprocess.run(cmd, shell=True, cwd=ROOT, capture_output=True, text=True)
    log_path.write_text(result.stdout + "\n" + result.stderr, encoding="utf-8")
    print(f"Wrote {log_path.relative_to(ROOT)} exit={result.returncode}")
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
