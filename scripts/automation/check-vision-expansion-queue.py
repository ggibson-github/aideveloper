#!/usr/bin/env python3
"""Backward-compatible wrapper for vision expansion queue."""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
CHECK = ROOT / "scripts" / "automation" / "check-hierarchy-queue.py"

if __name__ == "__main__":
    sys.exit(
        subprocess.call(
            [sys.executable, str(CHECK), "--queue", "docs/automation/vision-expansion-queue.json"],
            cwd=ROOT,
        )
    )
