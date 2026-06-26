#!/usr/bin/env python3
"""Update staleness.json from dependency graph and file mtimes."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STALE = ROOT / "docs" / "manifest" / "staleness.json"


def node_mtime(root: Path, rel_path: str) -> float | None:
    path = root / rel_path
    if path.is_file():
        return path.stat().st_mtime
    if path.is_dir():
        mtimes = [p.stat().st_mtime for p in path.rglob("*") if p.is_file()]
        return max(mtimes) if mtimes else None
    return None


def main() -> int:
    if not STALE.is_file():
        print(f"Missing {STALE}", file=sys.stderr)
        return 1

    data = json.loads(STALE.read_text(encoding="utf-8"))
    graph = data.get("graph", [])
    stale_map = data.get("stale") or {}

    node_by_id = {n["id"]: n for n in graph}
    mtimes: dict[str, float] = {}

    for node in graph:
        m = node_mtime(ROOT, node["path"])
        if m is not None:
            mtimes[node["id"]] = m

    now = datetime.now(timezone.utc).isoformat()

    for node in graph:
        nid = node["id"]
        deps = node.get("depends_on", [])
        if not deps:
            continue
        dep_mt = [mtimes.get(d, 0) for d in deps if d in mtimes]
        my_mt = mtimes.get(nid, 0)
        if dep_mt and max(dep_mt) > my_mt:
            stale_map[nid] = {
                "stale": True,
                "reason": f"dependency newer than {node['path']}",
                "updated_at": now,
            }
        elif nid in stale_map and stale_map[nid].get("stale"):
            stale_map[nid] = {
                "stale": False,
                "reason": "refreshed",
                "updated_at": now,
            }

    data["stale"] = stale_map
    STALE.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    stale_count = sum(1 for v in stale_map.values() if v.get("stale"))
    print(f"update-staleness: {stale_count} stale node(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
