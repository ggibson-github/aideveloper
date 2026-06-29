#!/usr/bin/env python3
"""Check hierarchy expansion queue (S0). Exit 0 = pending, 1 = empty/blocked."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent


def main() -> int:
    parser = argparse.ArgumentParser(description="Check hierarchy expansion queue")
    parser.add_argument(
        "--queue",
        default="docs/automation/vision-expansion-queue.json",
        help="Path to queue JSON (relative to repo root)",
    )
    args = parser.parse_args()
    queue_path = ROOT / args.queue
    if not queue_path.is_file():
        print(f"Missing {queue_path}", file=sys.stderr)
        return 1
    data = json.loads(queue_path.read_text(encoding="utf-8"))
    pending = [i for i in data.get("items", []) if i.get("status") == "pending"]
    blocked = [i for i in data.get("items", []) if i.get("status") == "blocked"]
    if pending:
        first = pending[0]
        print(
            f"READY: pending={len(pending)} next={first.get('id')} action={first.get('action')}"
        )
        return 0
    if blocked:
        print(f"BLOCKED: {len(blocked)} item(s) need user input")
        for b in blocked:
            print(f"  - {b.get('id')}: {b.get('blocker', 'unknown')}")
        return 1
    print("EMPTY: hierarchy expansion queue complete")
    return 1


if __name__ == "__main__":
    sys.exit(main())
