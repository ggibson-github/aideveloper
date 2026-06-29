#!/usr/bin/env python3
"""Legacy wrapper — use init-hierarchy-queue.py for unified all-branch queue."""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
INIT = ROOT / "scripts" / "automation" / "init-hierarchy-queue.py"

if __name__ == "__main__":
    print("seed-vision-expansion-leaves.py is deprecated.", file=sys.stderr)
    print("Use: python scripts/automation/init-hierarchy-queue.py --mode full", file=sys.stderr)
    sys.exit(subprocess.call([sys.executable, str(INIT), "--mode", "full"], cwd=ROOT))
