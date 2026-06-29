#!/usr/bin/env python3
"""Deep pass: rebuild leaf docs via hierarchy_leaf_builder (enrich + deepen + challenge)."""

from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from hierarchy_completeness import item_id_from_path, title_from_path  # noqa: E402
from hierarchy_leaf_depth import challenge_body  # noqa: E402
from hierarchy_queue_data import LEAVES, slug  # noqa: E402

QUEUE = ROOT / "docs/automation/vision-expansion-queue.json"


def process_queue(action: str) -> int:
    data = json.loads(QUEUE.read_text(encoding="utf-8"))
    today = date.today().isoformat()
    done = 0

    for item in data.get("items", []):
        if item.get("status") != "pending" or item.get("action") != action:
            continue
        iid = item["id"]
        raw_title = item.get("title", iid).replace(f"{action} pass for ", "")
        pass_num = item.get("pass", 1)
        out = ROOT / item.get("output", f"documents/plans/full-automation/{iid}-{slug(raw_title)}.md")
        if not out.is_file():
            matches = list((ROOT / "documents/plans/full-automation").glob(f"{iid}-*.md"))
            out = matches[0] if matches else out
        title = LEAVES.get(iid, raw_title if raw_title != iid else iid)

        if action in ("enrich", "deepen", "challenge"):
            from hierarchy_leaf_builder import write_leaf  # noqa: WPS433

            out.parent.mkdir(parents=True, exist_ok=True)
            write_leaf(out, iid, title, pass_num, challenge=True)

        item["status"] = "done"
        item["completed_at"] = today
        done += 1

    QUEUE.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"Processed {done} {action} items")
    return done


def deepen_leaves(ids: list[str] | None = None, pass_num: int = 1) -> int:
    from hierarchy_leaf_builder import write_leaf  # noqa: WPS433

    out_dir = ROOT / "documents/plans/full-automation"
    count = 0
    for p in sorted(out_dir.glob("*.md")):
        if p.name in ("INDEX.md", "H3-SIGNOFF-BUNDLE.md") or p.name.endswith("-index.md"):
            continue
        text = p.read_text(encoding="utf-8")
        iid = item_id_from_path(p, text)
        if ids and not any(iid == x or iid.startswith(x + ".") or iid.startswith(x) for x in ids):
            continue
        title = LEAVES.get(iid) or title_from_path(p, iid)
        write_leaf(p, iid, title, pass_num, challenge=True)
        count += 1
    print(f"Rebuilt {count} leaf files")
    return count


def challenge_leaves(ids: list[str] | None = None, force: bool = False) -> int:
    out_dir = ROOT / "documents/plans/full-automation"
    today = date.today().isoformat()
    count = 0
    for p in sorted(out_dir.glob("*.md")):
        if p.name in ("INDEX.md", "H3-SIGNOFF-BUNDLE.md") or p.name.endswith("-index.md"):
            continue
        text = p.read_text(encoding="utf-8")
        iid = item_id_from_path(p, text)
        if ids and not any(iid == x or iid.startswith(x + ".") or iid.startswith(x) for x in ids):
            continue
        if "## Adversarial review" in text and not force:
            continue
        title = LEAVES.get(iid) or title_from_path(p, iid)
        p.write_text(
            f"<!-- Challenged {today} {iid} -->\n\n{challenge_body(text, iid, title)}",
            encoding="utf-8",
        )
        count += 1
    print(f"Challenged {count} leaf files")
    return count


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--action", choices=("deepen", "challenge", "enrich", "all"), default="all")
    parser.add_argument("--from-queue", action="store_true")
    parser.add_argument("--ids", nargs="*", help="Only process these node ids")
    parser.add_argument("--force-challenge", action="store_true")
    parser.add_argument("--pass-num", type=int, default=1)
    args = parser.parse_args()

    ids = args.ids or None
    if args.from_queue:
        if args.action in ("enrich", "all"):
            process_queue("enrich")
        if args.action in ("deepen", "all"):
            process_queue("deepen")
        if args.action in ("challenge", "all"):
            process_queue("challenge")
    else:
        if args.action in ("deepen", "enrich", "all"):
            deepen_leaves(ids, pass_num=args.pass_num)
        if args.action in ("challenge", "all"):
            challenge_leaves(ids, force=args.force_challenge)
    return 0


if __name__ == "__main__":
    sys.exit(main())
