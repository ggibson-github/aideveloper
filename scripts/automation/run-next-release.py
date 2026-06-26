#!/usr/bin/env python3
"""Process next pending release-queue item (template evolution only).

For consumer project pipeline autopilot, use run-local-pipeline.py instead.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
QUEUE = ROOT / "docs" / "automation" / "release-queue.json"


def main() -> int:
    if not QUEUE.is_file():
        print(f"Missing {QUEUE}", file=sys.stderr)
        return 1

    queue = json.loads(QUEUE.read_text(encoding="utf-8"))
    pending = [r for r in queue.get("releases", []) if r.get("status") == "pending"]
    if not pending:
        print("No pending releases in release-queue.json")
        return 0

    release = pending[0]
    print(
        json.dumps(
            {
                "action": "implement_release_queue_item",
                "release": release,
                "prompt_file": "docs/automation/unattended-prompt.md",
                "local_pipeline": "python scripts/automation/run-local-pipeline.py",
                "note": "For template queue: implement one release manually or via SDK. "
                "For SDLC pipeline autopilot use run-local-pipeline.py (local runtime).",
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
