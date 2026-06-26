#!/usr/bin/env python3
"""Run Test command or Tool command from a task card; write evidence/."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EVIDENCE = ROOT / "evidence"


def extract_section(card_text: str, heading: str) -> str | None:
    lines = card_text.splitlines()
    target = heading.lower().strip()
    in_section = False
    collected: list[str] = []
    for line in lines:
        if line.strip().startswith("##"):
            h = line.strip().lower()
            if in_section:
                break
            if h == f"## {target}" or h.startswith(f"## {target}"):
                in_section = True
            continue
        if in_section:
            collected.append(line)
    text = "\n".join(collected).strip()
    return text or None


def extract_command(section_text: str) -> str | None:
    for line in section_text.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("`") and line.endswith("`"):
            return line.strip("`")
        if "`" in line:
            m = re.search(r"`([^`]+)`", line)
            if m:
                return m.group(1)
    return None


def find_task_card_from_state(state: dict) -> Path | None:
    na = str(state.get("next_action", ""))
    m = re.search(r"task\s+(\d+)", na, re.I)
    if not m:
        return None
    num = m.group(1).zfill(3)
    candidates = [
        ROOT / "docs" / "tasks" / f"task-{num}.md",
    ]
    program = state.get("program") or {}
    for ws in program.get("workstreams", []) or []:
        candidates.append(
            ROOT / "program" / "workstreams" / ws / "tasks" / f"task-{num}.md"
        )
    for path in candidates:
        if path.is_file():
            return path
    return None


def main() -> int:
    card_path: Path | None = None
    if len(sys.argv) > 1:
        card_path = Path(sys.argv[1])
        if not card_path.is_absolute():
            card_path = ROOT / card_path
    else:
        state_path = ROOT / "journal" / "state.json"
        if state_path.is_file():
            state = json.loads(state_path.read_text(encoding="utf-8"))
            card_path = find_task_card_from_state(state)

    if not card_path or not card_path.is_file():
        print("No task card found", file=sys.stderr)
        return 1

    card_text = card_path.read_text(encoding="utf-8")
    tool_section = extract_section(card_text, "tool command")
    test_section = extract_section(card_text, "test command")
    cmd = None
    if tool_section:
        cmd = extract_command(tool_section)
    if not cmd and test_section:
        cmd = extract_command(test_section)

    num = card_path.stem.split("-")[-1]
    log_name = f"task-{num}-test.log"

    EVIDENCE.mkdir(parents=True, exist_ok=True)
    log_path = EVIDENCE / log_name

    if not cmd or cmd.startswith("(none"):
        log_path.write_text("SKIP: no test/tool command\n", encoding="utf-8")
        print(f"SKIP {log_path.relative_to(ROOT)}")
        return 0

    result = subprocess.run(cmd, shell=True, cwd=ROOT, capture_output=True, text=True)
    log_path.write_text(
        f"COMMAND: {cmd}\nEXIT: {result.returncode}\n\n"
        + result.stdout
        + "\n"
        + result.stderr,
        encoding="utf-8",
    )
    print(f"Wrote {log_path.relative_to(ROOT)} exit={result.returncode}")
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
