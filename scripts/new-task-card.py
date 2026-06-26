#!/usr/bin/env python3
"""Create a task card markdown file from title and optional fields."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TASKS = ROOT / "docs" / "tasks"


def next_task_num() -> str:
    nums = []
    for p in TASKS.glob("task-*.md"):
        m = re.match(r"task-(\d+)", p.stem)
        if m:
            nums.append(int(m.group(1)))
    for p in ROOT.glob("program/workstreams/*/tasks/task-*.md"):
        m = re.match(r"task-(\d+)", p.stem)
        if m:
            nums.append(int(m.group(1)))
    return str(max(nums or [0]) + 1).zfill(3)


def main() -> int:
    parser = argparse.ArgumentParser(description="Create task-NNN.md")
    parser.add_argument("title", help="Task title")
    parser.add_argument("--workstream", default=None, help="Workstream id for program tasks")
    parser.add_argument("--test-cmd", default="(none — document manual verify)")
    parser.add_argument("--tool-cmd", default=None)
    parser.add_argument("--acceptance", default="- (add criteria)")
    args = parser.parse_args()

    num = next_task_num()
    if args.workstream:
        out_dir = ROOT / "program" / "workstreams" / args.workstream / "tasks"
    else:
        out_dir = TASKS

    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"task-{num}.md"

    lines = [
        f"# Task {num}: {args.title}",
        "",
        "## Workstream",
        "",
        args.workstream or "(none — main pipeline)",
        "",
        "## Acceptance criteria",
        "",
        args.acceptance,
        "",
        "## Design pointers",
        "",
        "- (optional)",
        "",
        "## Files to touch",
        "",
        "- (optional)",
        "",
        "## Facts topics",
        "",
        "- (optional)",
        "",
        "## Test command",
        "",
        f"`{args.test_cmd}`",
        "",
    ]
    if args.tool_cmd:
        lines.extend(["## Tool command", "", f"`{args.tool_cmd}`", ""])
    lines.extend(
        [
            "## Evidence",
            "",
            f"- Log: `evidence/task-{num}-test.log`",
            "",
        ]
    )

    path.write_text("\n".join(lines), encoding="utf-8")
    print(path.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
