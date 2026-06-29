#!/usr/bin/env python3
"""Resolve paths and settings for a registered hierarchy expansion topic."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
TOPICS_FILE = ROOT / "docs/automation/hierarchy-topics.json"

# Default iteration depth: three full passes before certification exit (operator may override).
DEFAULT_MIN_PASSES = 3
DEFAULT_MAX_PASSES = 3


@dataclass
class TopicConfig:
    topic: str
    title: str
    source: Path
    queue: Path
    prompt: Path
    output_dir: Path
    ledger: Path
    quality_report_json: Path
    quality_report_md: Path
    signoff_bundle: Path
    queue_data_module: str | None
    min_passes: int
    max_passes: int
    html_site_dir: Path | None
    html_site_config: str | None
    html_glossary: str | None

    def rel(self, p: Path) -> str:
        return str(p.relative_to(ROOT)).replace("\\", "/")


def slugify(topic: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", topic.lower()).strip("-")


def load_topics() -> dict:
    if not TOPICS_FILE.is_file():
        return {"version": 1, "topics": {}}
    return json.loads(TOPICS_FILE.read_text(encoding="utf-8"))


def save_topics(data: dict) -> None:
    TOPICS_FILE.parent.mkdir(parents=True, exist_ok=True)
    TOPICS_FILE.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def default_paths_for_topic(topic: str, source: str | None = None) -> dict:
    slug = slugify(topic)
    src = source or f"documents/{slug}-vision-and-hierarchy.md"
    return {
        "title": topic.replace("-", " ").title(),
        "source": src,
        "queue": f"docs/automation/{slug}-expansion-queue.json",
        "prompt": f"docs/automation/{slug}-expansion-prompt.md",
        "output_dir": f"documents/plans/{slug}/",
        "ledger": f"docs/automation/{slug}-iteration-ledger.json",
        "quality_report_json": f"docs/automation/{slug}-quality-report.json",
        "quality_report_md": f"docs/automation/{slug}-quality-report.md",
        "signoff_bundle": f"documents/plans/{slug}/H3-SIGNOFF-BUNDLE.md",
        "queue_data_module": None,
        "min_passes": DEFAULT_MIN_PASSES,
        "max_passes": DEFAULT_MAX_PASSES,
    }


def resolve_topic(
    topic: str,
    *,
    source: str | None = None,
    queue: str | None = None,
    prompt: str | None = None,
    output_dir: str | None = None,
) -> TopicConfig:
    data = load_topics()
    entry = data.get("topics", {}).get(topic)
    if entry is None:
        entry = default_paths_for_topic(topic, source)
    else:
        entry = dict(entry)

    if source:
        entry["source"] = source
    if queue:
        entry["queue"] = queue
    if prompt:
        entry["prompt"] = prompt
    if output_dir:
        entry["output_dir"] = output_dir

    def p(key: str) -> Path:
        return ROOT / entry[key]

    return TopicConfig(
        topic=topic,
        title=entry.get("title", topic),
        source=p("source"),
        queue=p("queue"),
        prompt=p("prompt"),
        output_dir=p("output_dir"),
        ledger=p("ledger"),
        quality_report_json=p("quality_report_json"),
        quality_report_md=p("quality_report_md"),
        signoff_bundle=p("signoff_bundle"),
        queue_data_module=entry.get("queue_data_module"),
        min_passes=int(entry.get("min_passes", DEFAULT_MIN_PASSES)),
        max_passes=int(entry.get("max_passes", DEFAULT_MAX_PASSES)),
        html_site_dir=(ROOT / entry["html_site_dir"]) if entry.get("html_site_dir") else None,
        html_site_config=entry.get("html_site_config"),
        html_glossary=entry.get("html_glossary"),
    )


def register_topic(topic: str, **overrides: str) -> TopicConfig:
    data = load_topics()
    paths = default_paths_for_topic(topic, overrides.get("source"))
    paths.update({k: v for k, v in overrides.items() if v})
    data.setdefault("topics", {})[topic] = paths
    save_topics(data)
    return resolve_topic(topic)


def list_topics() -> list[str]:
    return sorted(load_topics().get("topics", {}).keys())
