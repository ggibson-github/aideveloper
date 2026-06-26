#!/usr/bin/env python3
"""Headless verify: delegate to verify-router.py."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ROUTER = ROOT / "scripts" / "verify-router.py"


def main() -> int:
    if not ROUTER.is_file():
        print("Missing verify-router.py", file=sys.stderr)
        return 1
    result = subprocess.run([sys.executable, str(ROUTER)], cwd=ROOT)
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
