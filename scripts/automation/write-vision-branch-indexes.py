#!/usr/bin/env python3
"""Write branch index stubs linking all child docs under each expand node."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
QUEUE = ROOT / "docs" / "automation" / "vision-expansion-queue.json"
OUT = ROOT / "documents" / "plans" / "full-automation"


def main() -> None:
    data = json.loads(QUEUE.read_text(encoding="utf-8"))
    by_parent: dict[str, list[dict]] = {}
    for item in data["items"]:
        p = item.get("parent")
        if p:
            by_parent.setdefault(p, []).append(item)

    for parent, children in sorted(by_parent.items()):
        docs = [c for c in children if c.get("action") == "document" and c.get("status") == "done"]
        if not docs:
            continue
        lines = [
            f"# {parent} — index",
            "",
            f"Children of **{parent}** from vision expansion.",
            "",
            "| Id | Title | Doc |",
            "|----|-------|-----|",
        ]
        for c in sorted(docs, key=lambda x: x["id"]):
            out = c.get("output", "").replace("documents/plans/full-automation/", "")
            lines.append(f"| {c['id']} | {c['title']} | [{out}]({out}) |")
        path = OUT / f"{parent}-index.md"
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"Wrote {path.name} ({len(docs)} children)")


if __name__ == "__main__":
    main()
