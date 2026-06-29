#!/usr/bin/env python3
"""Load site config and derive branch metadata for hierarchy HTML publication."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from hierarchy_html_parse import ParsedNode, parse_markdown  # noqa: E402
from hierarchy_html_rules import BRANCH_COLOR_PALETTE  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent.parent
TEMPLATE_DIR = ROOT / "docs/automation/templates/hierarchy-html"
DEFAULT_SITE_CONFIG = TEMPLATE_DIR / "default-site-config.json"
DEFAULT_GLOSSARY = TEMPLATE_DIR / "glossary-base.json"


def deep_merge(base: dict, overlay: dict) -> dict:
    out = dict(base)
    for k, v in overlay.items():
        if k in out and isinstance(out[k], dict) and isinstance(v, dict):
            out[k] = deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def load_json(path: Path) -> dict:
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_site_config_paths(topic: str, html_site_config: str | None = None) -> tuple[Path, Path | None]:
    topic_overlay = TEMPLATE_DIR / f"{topic}-site-config.json"
    if html_site_config:
        return DEFAULT_SITE_CONFIG, ROOT / html_site_config
    if topic_overlay.is_file():
        return DEFAULT_SITE_CONFIG, topic_overlay
    return DEFAULT_SITE_CONFIG, None


def resolve_glossary_paths(topic: str, html_glossary: str | None = None) -> tuple[Path, Path | None]:
    topic_overlay = TEMPLATE_DIR / f"{topic}-glossary.json"
    if html_glossary:
        return DEFAULT_GLOSSARY, ROOT / html_glossary
    if topic_overlay.is_file():
        return DEFAULT_GLOSSARY, topic_overlay
    return DEFAULT_GLOSSARY, None


def load_site_config(topic: str, *, html_site_config: str | None = None) -> dict[str, Any]:
    base_path, overlay_path = resolve_site_config_paths(topic, html_site_config)
    cfg = load_json(base_path)
    if overlay_path and overlay_path.is_file():
        cfg = deep_merge(cfg, load_json(overlay_path))
    return cfg


def load_glossary_config(topic: str, *, html_glossary: str | None = None) -> list[dict]:
    base_path, overlay_path = resolve_glossary_paths(topic, html_glossary)
    base = load_json(base_path).get("entries", [])
    by_id = {e["id"]: e for e in base}
    if overlay_path and overlay_path.is_file():
        for e in load_json(overlay_path).get("entries", []):
            by_id[e["id"]] = e
    return list(by_id.values())


def _title_from_master(text: str, branch_id: str) -> str:
    m = re.search(rf"^#\s+MASTER-{re.escape(branch_id)}:\s*(.+)$", text, re.MULTILINE | re.I)
    if m:
        title = m.group(1).strip()
        stripped = re.match(rf"^Branch\s+{re.escape(branch_id)}\s*[—–-]\s*", title, re.I)
        if stripped:
            title = title[stripped.end() :].strip()
        return title
    m2 = re.search(r"^#\s+[^:]+:\s*(.+)$", text, re.MULTILINE)
    return m2.group(1).strip() if m2 else branch_id


def _story_from_purpose(purpose: str) -> str:
    p = re.sub(r"\*\*", "", purpose.strip())
    m = re.match(
        r"^MASTER-[\w-]+ defines (.+?) for the .+?\.\s*(.+)$",
        p,
        re.I | re.S,
    )
    if m:
        extra = m.group(2).strip()
        if extra:
            return extra.split(".")[0].strip()
        return m.group(1).strip().rstrip(".")
    if not p:
        return ""
    first = p.split(".")[0].strip()
    return first if len(first) > 20 else p[:200]


def derive_branch_meta(output_dir: Path, nodes: list[ParsedNode]) -> dict[str, dict[str, str]]:
    """Build branch titles/stories/colors from MASTER-* leaves or node purposes."""
    by_branch: dict[str, list[ParsedNode]] = {}
    for n in nodes:
        by_branch.setdefault(n.branch, []).append(n)

    meta: dict[str, dict[str, str]] = {}
    ordered = sorted(by_branch.keys(), key=lambda b: (b != "meta", b))
    for i, bid in enumerate(ordered):
        title = bid
        story = ""
        master = list(output_dir.glob(f"MASTER-{bid}*.md")) or list(output_dir.glob(f"MASTER-{bid.upper()}*.md"))
        if master:
            parsed = parse_markdown(master[0])
            title = _title_from_master(master[0].read_text(encoding="utf-8"), bid) or parsed.title
            story = _story_from_purpose(parsed.purpose)
        elif by_branch[bid]:
            n0 = by_branch[bid][0]
            story = _story_from_purpose(n0.purpose)
            title = n0.title if len(by_branch[bid]) == 1 else f"Branch {bid}"
        if bid == "meta":
            meta[bid] = {
                "title": "Front matter & cross-cutting architecture",
                "subtitle": "Introduction, flow, roadmap, decisions, appendices",
                "story": (
                    "Read these sections before the ten planes: north star and HITL contract, "
                    "the A–J map, pursuit flow, gap analysis, release roadmap, open decisions, "
                    "and pack authoring taxonomy."
                ),
                "color": BRANCH_COLOR_PALETTE[i % len(BRANCH_COLOR_PALETTE)],
            }
            continue
        meta[bid] = {
            "title": title,
            "subtitle": title,
            "story": story or f"Capabilities grouped under branch {bid}.",
            "color": BRANCH_COLOR_PALETTE[i % len(BRANCH_COLOR_PALETTE)],
        }
    return meta


def branch_sort_key(branch_id: str) -> tuple:
    if branch_id == "meta":
        return (-1, branch_id)
    if len(branch_id) == 1 and branch_id.isalpha():
        return (0, branch_id)
    return (1, branch_id)


def ordered_branches(by_branch: dict[str, list]) -> list[str]:
    return sorted(by_branch.keys(), key=branch_sort_key)


def resolve_index_stats(cfg: dict, *, node_count: int, branch_count: int) -> list[tuple[str, str]]:
    stats: list[tuple[str, str]] = []
    for item in cfg.get("index_stats", []):
        kind = item.get("kind", "static")
        label = item.get("label", "")
        if kind == "node_count":
            stats.append((str(node_count), label))
        elif kind == "branch_count":
            stats.append((str(branch_count), label))
        elif kind == "static":
            stats.append((str(item.get("value", "")), label))
    return stats
