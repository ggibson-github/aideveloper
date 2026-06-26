#!/usr/bin/env python3
"""Validate evidence for lane task and release lease."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    parser = argparse.ArgumentParser(description="Complete lane work order")
    parser.add_argument("workstream", help="Workstream id")
    parser.add_argument("--evidence", required=True, help="Evidence log path relative to root")
    parser.add_argument("--status", default="done", choices=["done", "verify", "failed"])
    args = parser.parse_args()

    lane_path = ROOT / "program" / "workstreams" / args.workstream / "lane.json"
    if not lane_path.is_file():
        print(f"Missing lane {lane_path}", file=sys.stderr)
        return 1

    evidence_path = ROOT / args.evidence
    if not evidence_path.is_file():
        print(f"Missing evidence {evidence_path}", file=sys.stderr)
        return 1

    lane = json.loads(lane_path.read_text(encoding="utf-8"))
    lane["lease"] = {"holder": None, "expires_at": None, "work_order_path": None}
    lane["status"] = args.status
    if args.status == "done":
        done = lane.get("done") or []
        task = lane.get("current_task")
        if task and task not in done:
            done.append(task)
        lane["done"] = done
        lane["current_task"] = None

    lane_path.write_text(json.dumps(lane, indent=2) + "\n", encoding="utf-8")
    print(f"Updated {lane_path.relative_to(ROOT)} status={args.status}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
