#!/usr/bin/env python3
"""Run multi-pass audit/rebuild until strict completeness (delegates to full pipeline)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-passes", type=int, default=0, help="0 = unlimited")
    parser.add_argument("--threshold", type=int, default=90)
    args = parser.parse_args()
    cmd = [
        sys.executable,
        str(ROOT / "scripts/automation/run-hierarchy-full-pipeline.py"),
        "--threshold", str(args.threshold),
        "--max-passes", str(args.max_passes),
    ]
    return subprocess.call(cmd, cwd=ROOT)


if __name__ == "__main__":
    sys.exit(main())
