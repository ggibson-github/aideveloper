#!/usr/bin/env python3
"""Initialize ONE unified hierarchy queue — all branches A–J in a single items[] list.

The /loop processes first pending item across branch boundaries until EMPTY.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

# Import shared node data (full-automation topic)
sys.path.insert(0, str(Path(__file__).resolve().parent))
from hierarchy_queue_data import (  # noqa: E402
    EXPAND_NODES,
    LEAVES,
    STANDALONE_DOCUMENTS,
    leaves_for_parent,
    parent_id,
    slug,
)

DEFAULT_SOURCE = "documents/full-automation-vision-and-hierarchy.md"
DEFAULT_PROMPT = "docs/automation/vision-expansion-prompt.md"
DEFAULT_OUTPUT = "documents/plans/full-automation/"
DEFAULT_QUEUE = "docs/automation/vision-expansion-queue.json"


def _expand_item(node: dict, *, status: str = "pending") -> dict:
    item = {
        "id": node["id"],
        "status": status,
        "action": "expand",
        "title": node["title"],
        "branch": node.get("branch", ""),
    }
    for key in ("source_section", "parent"):
        if key in node:
            item[key] = node[key]
    return item


def _document_item(
    item_id: str,
    title: str,
    output_dir: str,
    *,
    status: str = "pending",
    **extra: str,
) -> dict:
    out = extra.get("output") or f"{output_dir.rstrip('/')}/{item_id}-{slug(title)}.md"
    item = {
        "id": item_id,
        "status": status,
        "action": "document",
        "title": title,
        "output": out,
    }
    p = extra.get("parent") or parent_id(item_id)
    if p:
        item["parent"] = p
    for key in ("source_section", "branch"):
        if key in extra:
            item[key] = extra[key]
    return item


def build_unified_items(output_dir: str, *, mode: str) -> list[dict]:
    """Build single ordered queue: meta → A → B → … → I → J → meta appendices.

    All branches live in ONE items[] array. The loop walks FIFO across branches
    until the entire hierarchy is complete (checker EMPTY).
    """
    items: list[dict] = []

    standalone_after: dict[str, list[dict]] = {
        "H1": [d for d in STANDALONE_DOCUMENTS if d["id"].startswith("H") and d["id"] != "H1"],
        "I5": [d for d in STANDALONE_DOCUMENTS if d["id"].startswith("J")],
    }
    before_sec15 = [d for d in STANDALONE_DOCUMENTS if d["id"] in ("SEC-13", "SEC-14")]
    after_app_a = [d for d in STANDALONE_DOCUMENTS if d["id"] == "APP-B"]
    inserted_standalone = set()

    for node in EXPAND_NODES:
        if node["id"] == "SEC-15":
            for doc in before_sec15:
                items.append(_document_item(
                    doc["id"], doc["title"], output_dir, status="pending",
                    output=doc.get("output", ""), parent=doc.get("parent", ""),
                    source_section=doc.get("source_section", ""), branch=doc.get("branch", ""),
                ))
                inserted_standalone.add(doc["id"])

        if mode == "full":
            items.append(_expand_item(node, status="done"))
            for lid, title in leaves_for_parent(node["id"]):
                items.append(_document_item(
                    lid, title, output_dir, status="pending", parent=node["id"],
                    branch=node.get("branch", ""),
                ))
        else:
            items.append(_expand_item(node, status="pending"))

        for doc in standalone_after.get(node["id"], []):
            items.append(_document_item(
                doc["id"], doc["title"], output_dir, status="pending",
                output=doc.get("output", ""), parent=doc.get("parent", ""),
                source_section=doc.get("source_section", ""), branch=doc.get("branch", ""),
            ))
            inserted_standalone.add(doc["id"])

        if node["id"] == "APP-A" and mode == "full":
            for doc in after_app_a:
                items.append(_document_item(
                    doc["id"], doc["title"], output_dir, status="pending",
                    output=doc.get("output", ""), branch=doc.get("branch", ""),
                ))
                inserted_standalone.add(doc["id"])

    # Any standalone not yet placed (bootstrap mode: all at end in branch order)
    if mode == "bootstrap":
        for doc in STANDALONE_DOCUMENTS:
            if doc["id"] not in inserted_standalone:
                items.append(_document_item(
                    doc["id"], doc["title"], output_dir, status="pending",
                    output=doc.get("output", ""), parent=doc.get("parent", ""),
                    source_section=doc.get("source_section", ""), branch=doc.get("branch", ""),
                ))

    if mode == "full":
        covered = {i["id"] for i in items}
        for lid, title in sorted(LEAVES.items()):
            if lid in covered:
                continue
            items.append(_document_item(lid, title, output_dir, branch=lid[0] if lid and lid[0].isalpha() else "meta"))

    return items


def main() -> int:
    parser = argparse.ArgumentParser(description="Init unified hierarchy expansion queue")
    parser.add_argument("--queue", default=DEFAULT_QUEUE)
    parser.add_argument("--source", default=DEFAULT_SOURCE)
    parser.add_argument("--prompt", default=DEFAULT_PROMPT)
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--mode",
        choices=("bootstrap", "full"),
        default="full",
        help="bootstrap=expand only; full=all branches+leaves in one queue (default)",
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    items = build_unified_items(args.output_dir, mode=args.mode)
    branches = sorted({i.get("branch", "?") for i in items})
    pending = sum(1 for i in items if i["status"] == "pending")

    queue = {
        "version": 1,
        "description": "Unified queue: ALL branches (A–J + meta) in one items[] list. Loop until EMPTY.",
        "unified": True,
        "source": args.source,
        "prompt": args.prompt,
        "output_dir": args.output_dir,
        "items": items,
    }

    if args.dry_run:
        print(json.dumps({"total": len(items), "pending": pending, "branches": branches}, indent=2))
        return 0

    path = ROOT / args.queue
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(queue, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote unified queue: {path}")
    print(f"  items={len(items)} pending={pending} branches={branches}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
