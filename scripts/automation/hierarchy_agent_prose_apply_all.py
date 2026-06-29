#!/usr/bin/env python3
"""Apply all agent prose batch modules (pilot, meta, planes A–J)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
PY = sys.executable

MODULES = [
    "hierarchy_agent_prose_pilot.py",
    "hierarchy_agent_prose_meta.py",
    "hierarchy_agent_prose_plane_a_rest.py",
    "hierarchy_agent_prose_plane_b.py",
    "hierarchy_agent_prose_plane_c.py",
    "hierarchy_agent_prose_plane_d.py",
    "hierarchy_agent_prose_plane_e.py",
    "hierarchy_agent_prose_plane_f.py",
    "hierarchy_agent_prose_plane_g.py",
    "hierarchy_agent_prose_plane_h.py",
    "hierarchy_agent_prose_plane_i.py",
    "hierarchy_agent_prose_plane_j.py",
]


def main() -> int:
    failed = 0
    for mod in MODULES:
        path = ROOT / "scripts/automation" / mod
        if not path.is_file():
            print(f"SKIP missing {mod}", file=sys.stderr)
            failed += 1
            continue
        print(f"--- {mod} ---")
        rc = subprocess.call([PY, str(path)], cwd=str(ROOT))
        if rc != 0:
            failed += 1
    if failed:
        print(f"{failed} module(s) failed or missing", file=sys.stderr)
        return 1
    print("All agent prose modules applied.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
