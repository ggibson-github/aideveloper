#!/usr/bin/env python3
"""Verify hierarchy expansion coverage: files, queue, scaffolds."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from hierarchy_queue_data import LEAVES, STANDALONE_DOCUMENTS, slug  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--queue", default="docs/automation/vision-expansion-queue.json")
    parser.add_argument("--output-dir", default="documents/plans/full-automation")
    args = parser.parse_args()

    out_dir = ROOT / args.output_dir
    queue_path = ROOT / args.queue
    issues: list[str] = []

    missing = []
    for lid, title in LEAVES.items():
        if not list(out_dir.glob(f"{lid}-*.md")):
            missing.append(lid)
    for doc in STANDALONE_DOCUMENTS:
        if doc.get("output") and not (ROOT / doc["output"]).is_file():
            issues.append(f"missing standalone: {doc['id']}")

    if missing:
        issues.append(f"missing {len(missing)} leaf files: {missing[:5]}...")

    scaffolds = 0
    for p in out_dir.glob("*.md"):
        if p.name == "INDEX.md" or p.name.endswith("-index.md"):
            continue
        t = p.read_text(encoding="utf-8")
        if "TBD for `" in t or ("Generated 20" in t and "Expanded 20" not in t):
            scaffolds += 1

    pending = 0
    if queue_path.is_file():
        data = json.loads(queue_path.read_text(encoding="utf-8"))
        pending = sum(1 for i in data.get("items", []) if i.get("status") == "pending")
        if not data.get("unified"):
            issues.append("queue missing unified: true")
        if data.get("expansion_status") != "complete" and pending == 0:
            pass  # ok if enriched in place

    md_count = len(list(out_dir.glob("*.md")))
    print(json.dumps({
        "output_dir": str(out_dir),
        "markdown_files": md_count,
        "expected_leaves": len(LEAVES),
        "missing_leaves": len(missing),
        "scaffold_docs": scaffolds,
        "queue_pending": pending,
        "ok": not issues and not missing and scaffolds == 0 and pending == 0,
        "issues": issues,
    }, indent=2))
    return 0 if not issues and not missing and scaffolds == 0 and pending == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
