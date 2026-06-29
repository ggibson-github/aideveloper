#!/usr/bin/env python3
"""Record per-node iteration and sources gathered during hierarchy expansion."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_LEDGER = ROOT / "docs/automation/hierarchy-iteration-ledger.json"


def load_ledger(path: Path = DEFAULT_LEDGER) -> dict:
    if path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))
    return {
        "version": 1,
        "pipeline_passes": 0,
        "nodes": {},
    }


def save_ledger(data: dict, path: Path = DEFAULT_LEDGER) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def record_node_iteration(
    item_id: str,
    *,
    pass_num: int,
    sources: list[str],
    path: str,
    ledger_path: Path = DEFAULT_LEDGER,
) -> None:
    data = load_ledger(ledger_path)
    now = datetime.now(timezone.utc).isoformat()
    node = data["nodes"].setdefault(item_id, {"passes": 0, "history": []})
    node["passes"] = max(node.get("passes", 0), pass_num)
    node["last_path"] = path
    node["last_at"] = now
    node["sources"] = sorted(set(node.get("sources", []) + sources))
    node["history"].append({
        "pass": pass_num,
        "at": now,
        "sources_added": sources,
    })
    # cap history
    node["history"] = node["history"][-20:]
    save_ledger(data, ledger_path)


def record_pipeline_pass(pass_num: int, *, nodes_processed: int, ledger_path: Path = DEFAULT_LEDGER) -> None:
    data = load_ledger(ledger_path)
    data["pipeline_passes"] = pass_num
    data["last_pipeline_at"] = datetime.now(timezone.utc).isoformat()
    data["last_nodes_processed"] = nodes_processed
    save_ledger(data, ledger_path)


def ensure_all_leaves_in_ledger(leaf_ids: list[str], ledger_path: Path = DEFAULT_LEDGER) -> list[str]:
    """Return ids still missing iteration record."""
    data = load_ledger(ledger_path)
    missing = [i for i in leaf_ids if i not in data.get("nodes", {}) or data["nodes"][i].get("passes", 0) < 1]
    return missing
