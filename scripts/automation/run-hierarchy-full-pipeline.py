#!/usr/bin/env python3
"""
Fully automated hierarchy pipeline: iterate EVERY node, score quality, certify for human review.

Usage:
  python scripts/automation/run-hierarchy-full-pipeline.py
  python scripts/automation/generate-hierarchy-quality-report.py   # certification report only
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from hierarchy_completeness import audit_directory, item_id_from_path, list_leaf_paths, title_from_path  # noqa: E402
from hierarchy_iteration_ledger import record_pipeline_pass  # noqa: E402
from hierarchy_topic_config import DEFAULT_MAX_PASSES, DEFAULT_MIN_PASSES  # noqa: E402
from hierarchy_leaf_builder import resolve_leaf_path, write_leaf  # noqa: E402
from hierarchy_prose_editor import run_prose_editor_pass  # noqa: E402

DEFAULT_QUEUE = ROOT / "docs/automation/vision-expansion-queue.json"
DEFAULT_OUT = ROOT / "documents/plans/full-automation"
DEFAULT_LEDGER = ROOT / "docs/automation/hierarchy-iteration-ledger.json"
DEFAULT_SOURCE = "documents/full-automation-vision-and-hierarchy.md"
DEFAULT_QUALITY_JSON = ROOT / "docs/automation/hierarchy-quality-report.json"
DEFAULT_QUALITY_MD = ROOT / "docs/automation/hierarchy-quality-report.md"
DEFAULT_SIGNOFF = DEFAULT_OUT / "H3-SIGNOFF-BUNDLE.md"
REPORT = ROOT / "docs/automation/hierarchy-pipeline-report.json"


def load_leaves_map(queue_data_module: str | None) -> dict:
    if not queue_data_module:
        return {}
    import importlib

    mod = importlib.import_module(queue_data_module)
    return getattr(mod, "LEAVES", {})


def run(cmd: list[str]) -> tuple[int, str]:
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def ensure_structure(py: str, queue: str, out_dir: str) -> None:
    _, out = run([py, "scripts/automation/verify-hierarchy-expansion.py", "--queue", queue, "--output-dir", out_dir])
    print(out)
    data = json.loads(out[out.index("{"):])
    if not data.get("ok"):
        print("=== Generating missing leaf files ===")
        run([py, "scripts/automation/generate-vision-expansion-docs.py"])
        run([py, "scripts/automation/write-vision-branch-indexes.py"])


def iterate_all_leaves(out_dir: Path, pass_num: int, leaves: dict, ledger_path: Path, source: str) -> int:
    """Process every single leaf document (not only failures)."""
    count = 0
    for p in list_leaf_paths(out_dir):
        text = p.read_text(encoding="utf-8")
        iid = item_id_from_path(p, text)
        title = leaves.get(iid) or title_from_path(p, iid)
        write_leaf(p, iid, title, pass_num, challenge=True, ledger_path=ledger_path)
        count += 1
    vision = ROOT / source
    editor = run_prose_editor_pass(out_dir, vision_path=vision)
    print(f"Prose editor pass: {editor['edited']} leaves updated")
    record_pipeline_pass(pass_num, nodes_processed=count, ledger_path=ledger_path)
    return count


def run_quality_report(
    py: str,
    output_dir: str,
    ledger: str,
    source: str,
    quality_json: Path,
    quality_md: Path,
) -> dict:
    _, out = run([
        py, "scripts/automation/generate-hierarchy-quality-report.py",
        "--output-dir", output_dir,
        "--ledger", ledger,
        "--source", source,
        "--quality-json", str(quality_json.relative_to(ROOT)).replace("\\", "/"),
        "--quality-md", str(quality_md.relative_to(ROOT)).replace("\\", "/"),
    ])
    print(out)
    if quality_json.is_file():
        return json.loads(quality_json.read_text(encoding="utf-8"))
    return {}


def mark_queue_pass(queue_path: Path, pass_num: int, quality: dict) -> None:
    if not queue_path.is_file():
        return
    data = json.loads(queue_path.read_text(encoding="utf-8"))
    data["automation_pass"] = pass_num
    data["depth_pass"] = pass_num
    data["quality_certification"] = {
        "certified_for_human_review": quality.get("certified_for_human_review", False),
        "hierarchy_aggregate_score": quality.get("quality_summary", {}).get("hierarchy_aggregate_score"),
        "nodes_certified": quality.get("quality_summary", {}).get("nodes_certified"),
        "nodes_failed": quality.get("quality_summary", {}).get("nodes_failed"),
    }
    certified = quality.get("certified_for_human_review", False)
    if certified:
        data["signoff_ready"] = True
        data["signoff_at"] = date.today().isoformat()
        data["expansion_status"] = "complete"
        data["enrichment_status"] = "complete"
        data["hitl"] = {"pending": "H3", "payload": "full-automation hierarchy plan bundle"}
    else:
        data["signoff_ready"] = False
        data["enrichment_status"] = "in_progress"
    queue_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def write_signoff(signoff_path: Path, passes: int, quality: dict, quality_md: Path) -> None:
    q = quality["quality_summary"]
    s = quality["hierarchy_structure"]
    rel_report = quality_md.relative_to(ROOT).as_posix()
    signoff_path.parent.mkdir(parents=True, exist_ok=True)
    signoff_path.write_text(f"""# H3 Sign-off bundle — hierarchy plan

**Date:** {date.today().isoformat()}  
**Status:** CERTIFIED for human review  
**Automation passes:** {passes}  
**Hierarchy aggregate quality:** {q['hierarchy_aggregate_score']}/100

## Certification

This bundle is backed by `{rel_report}`:

- **{s['leaf_documents_present']}** leaf documents across **{s['branches_top_level']}** branches
- **{q['nodes_certified']}** / {q['nodes_certified'] + q['nodes_failed']} nodes certified (all dimensions >= 70, aggregate >= 85)
- Every node has iteration proof in the iteration ledger

```bash
python scripts/automation/hierarchy-expander-run.py --topic <TOPIC> certify
```

## Human H3

Accept to proceed to implementation, or reject specific node ids.
""", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--min-passes",
        type=int,
        default=DEFAULT_MIN_PASSES,
        help=f"Minimum full iterations before cert exit (default {DEFAULT_MIN_PASSES})",
    )
    parser.add_argument(
        "--max-passes",
        type=int,
        default=DEFAULT_MAX_PASSES,
        help=f"Max iterations (default {DEFAULT_MAX_PASSES}; 0 = unlimited until certified)",
    )
    parser.add_argument("--threshold", type=int, default=90)
    parser.add_argument("--stagnation-limit", type=int, default=5)
    parser.add_argument("--queue", default="docs/automation/vision-expansion-queue.json")
    parser.add_argument("--output-dir", default="documents/plans/full-automation")
    parser.add_argument("--ledger", default="docs/automation/hierarchy-iteration-ledger.json")
    parser.add_argument("--source", default=DEFAULT_SOURCE)
    parser.add_argument("--quality-json", default="docs/automation/hierarchy-quality-report.json")
    parser.add_argument("--quality-md", default="docs/automation/hierarchy-quality-report.md")
    parser.add_argument("--signoff", default="documents/plans/full-automation/H3-SIGNOFF-BUNDLE.md")
    parser.add_argument("--queue-data-module", default="hierarchy_queue_data")
    parser.add_argument("--verify-only", action="store_true", help="Quality report only")
    parser.add_argument("--skip-iterate", action="store_true", help="Audit/report only, no rebuild")
    args = parser.parse_args()

    py = sys.executable
    out_dir = ROOT / args.output_dir
    queue_path = ROOT / args.queue
    ledger_path = ROOT / args.ledger
    quality_json = ROOT / args.quality_json
    quality_md = ROOT / args.quality_md
    signoff_path = ROOT / args.signoff
    leaves = load_leaves_map(args.queue_data_module or None)

    def quality_report() -> dict:
        return run_quality_report(
            py, args.output_dir, args.ledger, args.source, quality_json, quality_md,
        )

    if args.verify_only:
        quality = quality_report()
        audit = audit_directory(out_dir, threshold=args.threshold)
        print(json.dumps({"audit_ready": audit["ready_for_signoff"], "quality_certified": quality.get("certified_for_human_review")}, indent=2))
        return 0 if quality.get("certified_for_human_review") else 1

    ensure_structure(py, args.queue, args.output_dir)

    passes = 0
    prev_failed = None
    stagnation = 0
    min_passes = max(1, args.min_passes)
    if args.max_passes == 0:
        max_passes = 10_000
    else:
        max_passes = max(args.max_passes, min_passes)

    while passes < max_passes:
        passes += 1
        print(f"\n{'='*60}\n=== Automation pass {passes} — iterate ALL nodes ===\n{'='*60}")

        if not args.skip_iterate:
            n = iterate_all_leaves(out_dir, passes, leaves, ledger_path, args.source)
            print(f"Iterated {n} leaf documents (100% of leaves)")

        quality = quality_report()
        failed = quality.get("quality_summary", {}).get("nodes_failed", 999)
        certified = quality.get("certified_for_human_review", False)

        summary = {
            "pass": passes,
            "certified_for_human_review": certified,
            "hierarchy_aggregate_score": quality.get("quality_summary", {}).get("hierarchy_aggregate_score"),
            "nodes_failed": failed,
        }
        print(json.dumps(summary, indent=2))

        mark_queue_pass(queue_path, passes, quality)
        REPORT.write_text(json.dumps({"passes": passes, "quality": quality}, indent=2) + "\n", encoding="utf-8")

        if certified and passes >= min_passes:
            write_signoff(signoff_path, passes, quality, quality_md)
            print(f"\nCERTIFIED for human review after {passes} passes (min {min_passes}).")
            print(f"Quality report: {quality_md}")
            print(f"H3 bundle: {signoff_path}")
            return 0

        if prev_failed is not None and failed >= prev_failed:
            stagnation += 1
            if stagnation >= args.stagnation_limit:
                print("\nBLOCKED: quality stagnation — see hierarchy-quality-report.md failed_nodes")
                return 1
        else:
            stagnation = 0
        prev_failed = failed

    print(f"\nBLOCKED: {passes} pass(es) completed (min {min_passes}, max {max_passes}) without certification")
    return 1


if __name__ == "__main__":
    sys.exit(main())
