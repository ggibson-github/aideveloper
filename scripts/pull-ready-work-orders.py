#!/usr/bin/env python3
"""List leasable work orders from program workstream lanes."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROGRAM_WS = ROOT / "program" / "workstreams"


def lane_ready(lane: dict) -> bool:
    lease = lane.get("lease") or {}
    if lease.get("holder"):
        expires = lease.get("expires_at")
        if expires:
            try:
                exp = datetime.fromisoformat(expires.replace("Z", "+00:00"))
                if exp > datetime.now(timezone.utc):
                    return False
            except ValueError:
                return False
        else:
            return False
    if lane.get("blocked_on"):
        return False
    return lane.get("status") in ("in_progress", "verify", "backlog")


def main() -> int:
    ready = []
    if not PROGRAM_WS.is_dir():
        print(json.dumps({"ready": []}))
        return 0

    for ws_dir in sorted(PROGRAM_WS.iterdir()):
        if not ws_dir.is_dir():
            continue
        lane_path = ws_dir / "lane.json"
        if not lane_path.is_file():
            continue
        lane = json.loads(lane_path.read_text(encoding="utf-8"))
        if not lane_ready(lane):
            continue
        task = lane.get("current_task")
        work_order = lane.get("lease", {}).get("work_order_path")
        if not task and not work_order:
            continue
        ready.append(
            {
                "workstream": ws_dir.name,
                "lane_path": str(lane_path.relative_to(ROOT)).replace("\\", "/"),
                "current_task": task,
                "work_order_path": work_order,
                "status": lane.get("status"),
            }
        )

    print(json.dumps({"ready": ready}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
