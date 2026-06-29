#!/usr/bin/env python3
"""Sync V2 master plan implementation tracker with 06-MASTER-CHECKLIST.md.

Reads checkbox items from the manifest, assigns stable IDs, and writes:
  - V2_Implementation_Plan/11-implementation-tracker.md  (human progress view)
  - docs/automation/implementation-tracker-registry.json (stable ID registry)

Usage:
  python scripts/automation/sync-implementation-tracker.py
  python scripts/automation/sync-implementation-tracker.py --apply-to-manifest
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "V2_Implementation_Plan" / "06-MASTER-CHECKLIST.md"
TRACKER = ROOT / "V2_Implementation_Plan" / "11-implementation-tracker.md"
REGISTRY = ROOT / "docs" / "automation" / "implementation-tracker-registry.json"

CHECKBOX_RE = re.compile(r"^- \[( |x|~)\] (.+)$")
SECTION_RE = re.compile(r"^## (.+)$")
SUBSECTION_RE = re.compile(r"^\*\*(.+)\*\*$")

SECTION_PREFIX = {
    "Pre-flight (do once, before v2.14)": "PF",
    "G5 — Mistake → control mapping (verify each control is live)": "G5",
    "Cross-cutting invariants (must hold across all releases)": "INV",
    "Final acceptance (vision achieved)": "FA",
}


def section_prefix(section: str) -> str:
    if section in SECTION_PREFIX:
        return SECTION_PREFIX[section]
    m = re.match(r"^v2\.(\d+)", section)
    if m:
        return f"V2{m.group(1)}"
    slug = re.sub(r"[^A-Za-z0-9]+", "", section)[:6].upper()
    return slug or "MISC"


def text_hash(text: str) -> str:
    normalized = re.sub(r"\s+", " ", text.strip())
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:16]


def parse_manifest(content: str) -> list[dict]:
    items: list[dict] = []
    section = ""
    subsection = ""
    for line in content.splitlines():
        sm = SECTION_RE.match(line)
        if sm:
            section = sm.group(1)
            subsection = ""
            continue
        subm = SUBSECTION_RE.match(line)
        if subm and not line.startswith("- "):
            subsection = subm.group(1)
            continue
        cb = CHECKBOX_RE.match(line)
        if cb and section:
            items.append(
                {
                    "section": section,
                    "subsection": subsection,
                    "status": cb.group(1),
                    "text": cb.group(2),
                    "hash": text_hash(cb.group(2)),
                    "manifest_line": line,
                }
            )
    return items


def load_registry() -> dict:
    if REGISTRY.exists():
        return json.loads(REGISTRY.read_text(encoding="utf-8"))
    return {"version": 1, "items": {}}


def save_registry(registry: dict) -> None:
    REGISTRY.parent.mkdir(parents=True, exist_ok=True)
    REGISTRY.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")


def assign_ids(items: list[dict], registry: dict) -> list[dict]:
    """Assign stable IDs; reuse by text hash within section."""
    hash_to_id: dict[str, str] = {}
    for item_id, meta in registry.get("items", {}).items():
        hash_to_id[meta["hash"]] = item_id

    section_counters: dict[str, int] = defaultdict(int)
    for meta in registry.get("items", {}).values():
        prefix = meta.get("prefix", "")
        num = int(meta.get("num", 0))
        if num >= section_counters[prefix]:
            section_counters[prefix] = num

    enriched: list[dict] = []
    for item in items:
        h = item["hash"]
        if h in hash_to_id:
            item_id = hash_to_id[h]
        else:
            prefix = section_prefix(item["section"])
            section_counters[prefix] += 1
            num = section_counters[prefix]
            item_id = f"{prefix}-{num:03d}"
            hash_to_id[h] = item_id
            registry.setdefault("items", {})[item_id] = {
                "hash": h,
                "prefix": prefix,
                "num": num,
                "section": item["section"],
                "text_preview": item["text"][:120],
            }
        item["id"] = item_id
        registry["items"][item_id]["status"] = item["status"]
        registry["items"][item_id]["section"] = item["section"]
        enriched.append(item)
    return enriched


def summarize(items: list[dict]) -> dict[str, dict[str, int]]:
    by_section: dict[str, dict[str, int]] = defaultdict(lambda: {"done": 0, "wip": 0, "total": 0})
    for item in items:
        sec = item["section"]
        by_section[sec]["total"] += 1
        if item["status"] == "x":
            by_section[sec]["done"] += 1
        elif item["status"] == "~":
            by_section[sec]["wip"] += 1
    return dict(by_section)


def status_icon(status: str) -> str:
    return {" ": "[ ]", "x": "[x]", "~": "[~]"}.get(status, "[ ]")


def render_tracker(items: list[dict], registry: dict) -> str:
    summary = summarize(items)
    total = len(items)
    done = sum(1 for i in items if i["status"] == "x")
    wip = sum(1 for i in items if i["status"] == "~")
    pct = round(100 * done / total, 1) if total else 0.0
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    lines = [
        "# 11 — Implementation Tracker",
        "",
        "**Purpose:** Single progress view for every checkbox in the V2 master plan.",
        "**Detail manifest:** [06-MASTER-CHECKLIST.md](06-MASTER-CHECKLIST.md)",
        "**Registry:** [docs/automation/implementation-tracker-registry.json](../docs/automation/implementation-tracker-registry.json)",
        "",
        f"**Last synced:** {now} · **Progress:** {done} / {total} done ({pct}%) · {wip} in progress",
        "",
        "## How to use",
        "",
        "1. Implement work using [06-MASTER-CHECKLIST.md](06-MASTER-CHECKLIST.md) (full artifact + verify detail).",
        "2. Check items off in **either** 06 or this file (`[ ]` → `[x]` when verified).",
        "3. Run `python scripts/automation/sync-implementation-tracker.py` to refresh counts.",
        "4. Run with `--apply-to-manifest` to push checkbox states from this file back into 06.",
        "",
        "Status: `[ ]` not started · `[~]` in progress · `[x]` done & verified.",
        "",
        "---",
        "",
        "## Progress by release",
        "",
        "| Release | Done | WIP | Total | % |",
        "|---------|------|-----|-------|---|",
    ]

    section_order: list[str] = []
    seen: set[str] = set()
    for item in items:
        if item["section"] not in seen:
            section_order.append(item["section"])
            seen.add(item["section"])

    for sec in section_order:
        s = summary[sec]
        spct = round(100 * s["done"] / s["total"], 1) if s["total"] else 0
        short = sec.replace(" — ", " — ").split(" — ")[0]
        if len(short) > 40:
            short = short[:37] + "..."
        lines.append(f"| {short} | {s['done']} | {s['wip']} | {s['total']} | {spct}% |")

    lines.extend(["", "---", "", "## All items", ""])

    current_section = ""
    current_sub = ""
    for item in items:
        if item["section"] != current_section:
            current_section = item["section"]
            current_sub = ""
            lines.extend(["", f"### {current_section}", ""])
        if item["subsection"] and item["subsection"] != current_sub:
            current_sub = item["subsection"]
            lines.append(f"*{current_sub}*")
            lines.append("")
        box = status_icon(item["status"])
        lines.append(f"- {box} **{item['id']}** — {item['text']}")
        lines.append("")

    lines.extend(
        [
            "---",
            "",
            f"*Generated by `scripts/automation/sync-implementation-tracker.py` · {total} items · registry v{registry.get('version', 1)}*",
            "",
        ]
    )
    return "\n".join(lines)


def apply_tracker_to_manifest(manifest_content: str, items: list[dict]) -> str:
    """Replace manifest checkboxes using tracker item statuses matched by hash."""
    hash_to_status = {item["hash"]: item["status"] for item in items}
    out_lines: list[str] = []
    for line in manifest_content.splitlines():
        cb = CHECKBOX_RE.match(line)
        if cb:
            h = text_hash(cb.group(2))
            status = hash_to_status.get(h, cb.group(1))
            out_lines.append(f"- [{status}] {cb.group(2)}")
        else:
            out_lines.append(line)
    return "\n".join(out_lines) + "\n"


def parse_tracker(content: str) -> list[dict]:
    """Parse checkbox states from 11-implementation-tracker.md."""
    items: list[dict] = []
    section = ""
    for line in content.splitlines():
        sm = re.match(r"^### (.+)$", line)
        if sm:
            section = sm.group(1)
            continue
        cb = re.match(r"^- \[( |x|~)\] \*\*([A-Z0-9-]+)\*\* — (.+)$", line)
        if cb:
            text = cb.group(3)
            if text.endswith("..."):
                # truncated preview — match via registry
                items.append(
                    {
                        "id": cb.group(2),
                        "status": cb.group(1),
                        "section": section,
                        "text": text,
                        "hash": None,
                    }
                )
            else:
                items.append(
                    {
                        "id": cb.group(2),
                        "status": cb.group(1),
                        "section": section,
                        "text": text,
                        "hash": text_hash(text),
                    }
                )
    return items


def merge_tracker_status(manifest_items: list[dict], tracker_items: list[dict], registry: dict) -> None:
    id_to_status = {t["id"]: t["status"] for t in tracker_items}
    for item in manifest_items:
        tid = item["id"]
        if tid in id_to_status:
            item["status"] = id_to_status[tid]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--apply-to-manifest",
        action="store_true",
        help="Write checkbox states from tracker back into 06-MASTER-CHECKLIST.md",
    )
    args = parser.parse_args()

    if not MANIFEST.exists():
        raise SystemExit(f"Manifest not found: {MANIFEST}")

    manifest_content = MANIFEST.read_text(encoding="utf-8")
    manifest_items = parse_manifest(manifest_content)
    registry = load_registry()

    if TRACKER.exists():
        tracker_parsed = parse_tracker(TRACKER.read_text(encoding="utf-8"))
        if tracker_parsed:
            # First pass IDs from manifest
            manifest_items = assign_ids(manifest_items, registry)
            merge_tracker_status(manifest_items, tracker_parsed, registry)
        else:
            manifest_items = assign_ids(manifest_items, registry)
    else:
        manifest_items = assign_ids(manifest_items, registry)

    registry["last_sync"] = datetime.now(timezone.utc).isoformat()
    registry["totals"] = {
        "total": len(manifest_items),
        "done": sum(1 for i in manifest_items if i["status"] == "x"),
        "wip": sum(1 for i in manifest_items if i["status"] == "~"),
    }
    save_registry(registry)

    tracker_md = render_tracker(manifest_items, registry)
    TRACKER.write_text(tracker_md, encoding="utf-8")

    if args.apply_to_manifest:
        updated = apply_tracker_to_manifest(manifest_content, manifest_items)
        MANIFEST.write_text(updated, encoding="utf-8")
        print(f"Updated manifest: {MANIFEST}")

    totals = registry["totals"]
    print(f"Tracker synced: {TRACKER}")
    print(f"Registry: {REGISTRY}")
    print(f"Progress: {totals['done']}/{totals['total']} done, {totals['wip']} in progress")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
