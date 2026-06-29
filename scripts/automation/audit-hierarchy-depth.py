#!/usr/bin/env python3
"""Audit leaf docs for completeness; enqueue enrich/deepen/challenge (S0)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from hierarchy_completeness import (  # noqa: E402
    audit_directory,
    item_id_from_path,
    list_leaf_paths,
    score_doc_completeness,
    title_from_path,
)

DEFAULT_OUT = ROOT / "documents/plans/full-automation"
DEFAULT_QUEUE = ROOT / "docs/automation/vision-expansion-queue.json"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default=str(DEFAULT_OUT.relative_to(ROOT)))
    parser.add_argument("--queue", default=str(DEFAULT_QUEUE.relative_to(ROOT)))
    parser.add_argument("--threshold", type=int, default=90, help="Score below = incomplete")
    parser.add_argument("--strict", action="store_true", help="Require zero reasons (default with --strict)")
    parser.add_argument("--enqueue", action="store_true", help="Append enrich/deepen/challenge items")
    parser.add_argument("--pass-num", type=int, default=1)
    parser.add_argument("--ids", nargs="*", help="Only audit these ids")
    args = parser.parse_args()

    if args.strict:
        args.threshold = max(args.threshold, 90)

    out_dir = ROOT / args.output_dir
    queue_path = ROOT / args.queue

    if args.ids:
        incomplete = []
        audited = 0
        for p in list_leaf_paths(out_dir):
            text = p.read_text(encoding="utf-8")
            iid = item_id_from_path(p, text)
            if not any(iid == x or iid.startswith(x + ".") or iid.startswith(x) for x in args.ids):
                continue
            title = title_from_path(p, iid)
            score, reasons, is_complete = score_doc_completeness(
                text, iid, title, threshold=args.threshold
            )
            audited += 1
            if not is_complete:
                incomplete.append({
                    "id": iid,
                    "path": str(p.relative_to(ROOT)),
                    "score": score,
                    "reasons": reasons,
                })
        report = {
            "audited": audited,
            "incomplete": len(incomplete),
            "threshold": args.threshold,
            "strict": args.strict,
            "pass": args.pass_num,
            "ready_for_signoff": len(incomplete) == 0,
            "items": incomplete,
        }
    else:
        full = audit_directory(out_dir, threshold=args.threshold)
        report = {
            "audited": full["audited"],
            "incomplete": full["incomplete"],
            "shallow": full["incomplete"],
            "threshold": args.threshold,
            "strict": args.strict,
            "pass": args.pass_num,
            "ready_for_signoff": full["ready_for_signoff"],
            "duplicate_clusters": full.get("duplicate_clusters", 0),
            "items": full["items"][:20],
        }

    print(json.dumps(report, indent=2))
    incomplete_all = report["incomplete"]
    if incomplete_all > 20 and not args.ids:
        print(f"... and {incomplete_all - 20} more incomplete docs")

    if args.enqueue and queue_path.is_file() and incomplete_all > 0:
        data = json.loads(queue_path.read_text(encoding="utf-8"))
        data["depth_pass"] = args.pass_num
        data["depth_audit"] = {
            "incomplete_count": incomplete_all,
            "threshold": args.threshold,
            "strict": args.strict,
        }
        existing = {(i["id"], i.get("action")) for i in data.get("items", []) if i.get("status") == "pending"}
        appended = 0
        items_to_enqueue = report["items"] if args.ids else _load_all_incomplete(out_dir, args.threshold)
        for s in items_to_enqueue:
            iid = s["id"]
            for action in ("enrich", "deepen", "challenge"):
                key = (iid, action)
                if key in existing:
                    continue
                data["items"].append({
                    "id": iid,
                    "status": "pending",
                    "action": action,
                    "pass": args.pass_num,
                    "title": f"{action} pass for {iid}",
                    "reason": "; ".join(s.get("reasons", [])[:5]),
                    "output": s.get("path", ""),
                })
                appended += 1
        queue_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        print(f"Enqueued {appended} enrich/deepen/challenge items")

    return 0 if report["ready_for_signoff"] else 1


def _load_all_incomplete(out_dir: Path, threshold: int) -> list[dict]:
    full = audit_directory(out_dir, threshold=threshold)
    return full["items"]


if __name__ == "__main__":
    sys.exit(main())
