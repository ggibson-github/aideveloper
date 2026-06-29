#!/usr/bin/env python3
"""
Generate hierarchy quality certification report (JSON + Markdown).

Proves every node was iterated and scored on multiple quality dimensions.
Exit 0 only when certified_for_human_review is true.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from hierarchy_completeness import item_id_from_path, list_leaf_paths, title_from_path  # noqa: E402
from hierarchy_quality import (  # noqa: E402
    CERT_AGGREGATE_MIN,
    CERT_DIMENSION_MIN,
    DIMENSION_WEIGHTS,
    DocQuality,
    aggregate_branch_scores,
    hierarchy_depth_from_ids,
    measure_doc_quality,
)
from hierarchy_queue_data import EXPAND_NODES, LEAVES  # noqa: E402

DEFAULT_OUT = ROOT / "documents/plans/full-automation"
DEFAULT_LEDGER = ROOT / "docs/automation/hierarchy-iteration-ledger.json"
JSON_REPORT = ROOT / "docs/automation/hierarchy-quality-report.json"
MD_REPORT = ROOT / "docs/automation/hierarchy-quality-report.md"


def load_ledger(path: Path) -> dict:
    if not path.is_file():
        return {"nodes": {}}
    return json.loads(path.read_text(encoding="utf-8"))


def count_branches(out_dir: Path) -> int:
    indexes = list(out_dir.glob("*-index.md")) + list(out_dir.glob("MASTER-*-index.md"))
    return len({p.name.split("-")[0] for p in indexes if p.name != "INDEX.md"})


def build_report(out_dir: Path, ledger: dict, source: str) -> dict:
    leaves = list_leaf_paths(out_dir)
    ledger_nodes = ledger.get("nodes", {})
    docs: list[DocQuality] = []

    for p in leaves:
        text = p.read_text(encoding="utf-8")
        iid = item_id_from_path(p, text)
        title = LEAVES.get(iid) or title_from_path(p, iid)
        rel = str(p.relative_to(ROOT))
        lp = ledger_nodes.get(iid, {}).get("passes", 0)
        docs.append(measure_doc_quality(text, iid, title, rel, ledger_pass=lp))

    ids = [d.id for d in docs]
    certified = [d for d in docs if d.certified]
    failed = [d for d in docs if not d.certified]
    branch_stats = aggregate_branch_scores(docs)

    dim_avgs = {
        dim: round(sum(getattr(d, dim) for d in docs) / len(docs), 1) if docs else 0
        for dim in DIMENSION_WEIGHTS
    }
    hierarchy_aggregate = round(sum(d.aggregate for d in docs) / len(docs), 1) if docs else 0

    missing_from_ledger = [d.id for d in docs if d.id not in ledger_nodes]
    not_iterated = [d.id for d in docs if d.iteration_pass < 1]

    certified_for_human_review = (
        len(failed) == 0
        and len(not_iterated) == 0
        and hierarchy_aggregate >= CERT_AGGREGATE_MIN
        and all(dim_avgs[k] >= CERT_DIMENSION_MIN for k in DIMENSION_WEIGHTS)
    )

    expand_branches = sorted({n.get("branch", n["id"][0]) for n in EXPAND_NODES})

    return {
        "generated_at": date.today().isoformat(),
        "source_hierarchy": source,
        "certified_for_human_review": certified_for_human_review,
        "certification_thresholds": {
            "aggregate_min": CERT_AGGREGATE_MIN,
            "dimension_min": CERT_DIMENSION_MIN,
            "dimension_weights": DIMENSION_WEIGHTS,
        },
        "hierarchy_structure": {
            "branches_top_level": len(expand_branches),
            "branch_ids": expand_branches,
            "expand_nodes": len(EXPAND_NODES),
            "leaf_nodes_expected": len(LEAVES),
            "leaf_documents_present": len(leaves),
            "index_files": len(list(out_dir.glob("*-index.md"))),
            "max_id_depth": hierarchy_depth_from_ids(ids),
            "total_markdown_in_dir": len(list(out_dir.glob("*.md"))),
        },
        "iteration_proof": {
            "ledger_nodes": len(ledger_nodes),
            "documents_with_pass_marker": sum(1 for d in docs if d.iteration_pass >= 1),
            "missing_from_ledger": missing_from_ledger[:20],
            "missing_from_ledger_count": len(missing_from_ledger),
            "not_iterated": not_iterated[:20],
            "not_iterated_count": len(not_iterated),
            "pipeline_passes": ledger.get("pipeline_passes", 0),
        },
        "quality_summary": {
            "hierarchy_aggregate_score": hierarchy_aggregate,
            "dimension_averages": dim_avgs,
            "nodes_certified": len(certified),
            "nodes_failed": len(failed),
            "certification_rate_pct": round(100 * len(certified) / len(docs), 1) if docs else 0,
        },
        "branch_scores": branch_stats,
        "failed_nodes": [d.to_dict() for d in sorted(failed, key=lambda x: x.aggregate)[:50]],
        "all_nodes": [d.to_dict() for d in sorted(docs, key=lambda x: x.id)],
    }


def write_markdown(report: dict, md_path: Path) -> None:
    s = report["hierarchy_structure"]
    q = report["quality_summary"]
    it = report["iteration_proof"]
    cert = report["certified_for_human_review"]
    status = "CERTIFIED — safe for human review" if cert else "NOT CERTIFIED — do not spend reading time yet"

    lines = [
        "# Hierarchy quality certification report",
        "",
        f"**Generated:** {report['generated_at']}  ",
        f"**Status:** {status}  ",
        f"**Source:** [{report['source_hierarchy']}](../../{report['source_hierarchy']})",
        "",
        "## Executive guarantee",
        "",
        "Human reading time is warranted **only** when `certified_for_human_review: true`.",
        "That requires **every leaf** to pass **all six quality dimensions** and the **aggregate score**.",
        "",
        "## Hierarchy structure",
        "",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Top-level branches | {s['branches_top_level']} ({', '.join(s['branch_ids'])}) |",
        f"| Expand nodes | {s['expand_nodes']} |",
        f"| Leaf documents | {s['leaf_documents_present']} / {s['leaf_nodes_expected']} expected |",
        f"| Index files | {s['index_files']} |",
        f"| Max node id depth | {s['max_id_depth']} |",
        f"| Total markdown files | {s['total_markdown_in_dir']} |",
        "",
        "## Iteration proof (every node processed)",
        "",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Nodes in iteration ledger | {it['ledger_nodes']} |",
        f"| Documents with Complete pass marker | {it['documents_with_pass_marker']} |",
        f"| Pipeline passes recorded | {it['pipeline_passes']} |",
        f"| Missing from ledger | {it['missing_from_ledger_count']} |",
        f"| Never iterated | {it['not_iterated_count']} |",
        "",
        "## Aggregate quality",
        "",
        f"**Hierarchy aggregate score: {q['hierarchy_aggregate_score']}/100** (min {CERT_AGGREGATE_MIN})",
        "",
        "| Dimension | Avg score | Min required | Weight |",
        "|-----------|-----------|--------------|--------|",
    ]
    for dim, weight in DIMENSION_WEIGHTS.items():
        lines.append(f"| {dim} | {q['dimension_averages'][dim]} | {CERT_DIMENSION_MIN} | {int(weight*100)}% |")
    lines.extend([
        "",
        f"- **Nodes certified:** {q['nodes_certified']} / {q['nodes_certified'] + q['nodes_failed']}",
        f"- **Certification rate:** {q['certification_rate_pct']}%",
        "",
        "## Branch breakdown",
        "",
        "| Branch | Nodes | Avg aggregate | Research avg | Certified |",
        "|--------|-------|---------------|--------------|-----------|",
    ])
    for branch, stats in report["branch_scores"].items():
        lines.append(
            f"| {branch} | {stats['nodes']} | {stats['aggregate_avg']} | {stats['research_avg']} | {stats['certified']}/{stats['nodes']} |"
        )
    if report["failed_nodes"]:
        lines.extend(["", "## Failed nodes (fix before reading)", ""])
        for n in report["failed_nodes"][:15]:
            lines.append(f"- **{n['id']}** aggregate={n['aggregate']} gaps: {', '.join(n['gaps'][:3])}")
    lines.extend([
        "",
        "## Verify",
        "",
        "```bash",
        "python scripts/automation/generate-hierarchy-quality-report.py",
        "python scripts/automation/run-hierarchy-full-pipeline.py --verify-only",
        "```",
        "",
        "Full per-node scores: `docs/automation/hierarchy-quality-report.json` → `all_nodes[]`.",
    ])
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default=str(DEFAULT_OUT.relative_to(ROOT)))
    parser.add_argument("--ledger", default=str(DEFAULT_LEDGER.relative_to(ROOT)))
    parser.add_argument("--source", default="documents/full-automation-vision-and-hierarchy.md")
    parser.add_argument("--quality-json", default="docs/automation/hierarchy-quality-report.json")
    parser.add_argument("--quality-md", default="docs/automation/hierarchy-quality-report.md")
    args = parser.parse_args()

    out_dir = ROOT / args.output_dir
    ledger = load_ledger(ROOT / args.ledger)
    report = build_report(out_dir, ledger, args.source)
    json_path = ROOT / args.quality_json
    md_path = ROOT / args.quality_md
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    write_markdown(report, md_path)

    summary = {
        "certified_for_human_review": report["certified_for_human_review"],
        "hierarchy_aggregate_score": report["quality_summary"]["hierarchy_aggregate_score"],
        "leaf_documents": report["hierarchy_structure"]["leaf_documents_present"],
        "nodes_certified": report["quality_summary"]["nodes_certified"],
        "nodes_failed": report["quality_summary"]["nodes_failed"],
        "reports": [str(json_path.relative_to(ROOT)), str(md_path.relative_to(ROOT))],
    }
    print(json.dumps(summary, indent=2))
    return 0 if report["certified_for_human_review"] else 1


if __name__ == "__main__":
    sys.exit(main())
