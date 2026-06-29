#!/usr/bin/env python3
"""Parse hierarchy leaf markdown into structured content for HTML publishing."""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path

from hierarchy_completeness import item_id_from_path, list_leaf_paths, title_from_path  # noqa: E402
from hierarchy_quality import branch_for  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent.parent


@dataclass
class ParsedNode:
    id: str
    slug: str
    title: str
    branch: str
    parent: str = ""
    vision_section: str = ""
    release: str = ""
    purpose: str = ""
    scope: list[str] = field(default_factory=list)
    behavior_steps: list[str] = field(default_factory=list)
    mermaid: str = ""
    json_example: str = ""
    edge_cases: list[str] = field(default_factory=list)
    failure_modes: list[str] = field(default_factory=list)
    implementation: list[str] = field(default_factory=list)
    verification: list[dict[str, str]] = field(default_factory=list)
    artifacts: list[str] = field(default_factory=list)
    dependencies: list[dict[str, str]] = field(default_factory=list)
    acceptance: list[str] = field(default_factory=list)
    adversarial: list[str] = field(default_factory=list)
    narrative: str = ""
    reader_narrative: str = ""
    source_path: str = ""
    quality: dict | None = None

    def to_dict(self) -> dict:
        return asdict(self)


def _section(text: str, name: str) -> str:
    m = re.search(rf"## {re.escape(name)}[^\n]*\n([\s\S]*?)(?=\n## |\Z)", text)
    return m.group(1).strip() if m else ""


def _bullets(block: str) -> list[str]:
    return [re.sub(r"^\-\s+", "", ln.strip()) for ln in block.splitlines() if ln.strip().startswith("-")]


def _numbered(block: str) -> list[str]:
    return [
        re.sub(r"^\d+\.\s+", "", ln.strip())
        for ln in block.splitlines()
        if re.match(r"^\d+\.\s", ln.strip())
    ]


def _table_rows(block: str) -> list[dict[str, str]]:
    lines = [ln.strip() for ln in block.splitlines() if ln.strip().startswith("|")]
    if len(lines) < 2:
        return []
    headers = [c.strip() for c in lines[0].strip("|").split("|")]
    rows: list[dict[str, str]] = []
    for ln in lines[2:]:
        cells = [c.strip() for c in ln.strip("|").split("|")]
        if len(cells) == len(headers):
            rows.append(dict(zip(headers, cells)))
    return rows


def _fenced(text: str, lang: str) -> str:
    m = re.search(rf"```{lang}\n([\s\S]*?)```", text)
    return m.group(1).strip() if m else ""


def _meta_field(text: str, label: str) -> str:
    m = re.search(rf"\*\*{re.escape(label)}:\*\*\s*([^\n·]+)", text)
    return m.group(1).strip() if m else ""


def _compose_narrative(purpose: str, behavior: list[str], title: str) -> str:
    lead = purpose.strip() or f"This capability defines {title}."
    if behavior:
        flow = behavior[0].rstrip(".")
        if len(behavior) > 1:
            flow += f", then {behavior[1].lower().rstrip('.')}"
        return f"{lead} In practice, the system {flow.lower()}."
    return lead


def parse_markdown(path: Path, text: str | None = None) -> ParsedNode:
    raw = text if text is not None else path.read_text(encoding="utf-8")
    item_id = item_id_from_path(path, raw)
    title_m = re.search(r"^#\s+[^:]+:\s*(.+)$", raw, re.MULTILINE)
    title = title_m.group(1).strip() if title_m else title_from_path(path, item_id)

    purpose = _section(raw, "Purpose")
    purpose = re.sub(r"\*\*[^*]+\*\*", lambda m: m.group(0).strip("*"), purpose).strip()

    node = ParsedNode(
        id=item_id,
        slug=path.stem,
        title=title,
        branch=branch_for(item_id),
        parent=_meta_field(raw, "Parent"),
        vision_section=_meta_field(raw, "Vision"),
        release=_meta_field(raw, "Release"),
        purpose=purpose,
        scope=_bullets(_section(raw, "Scope")),
        behavior_steps=_numbered(_section(raw, "Behavior / step logic") or _section(raw, "Behavior")),
        mermaid=_fenced(raw, "mermaid"),
        json_example=_fenced(raw, "json"),
        edge_cases=_bullets(_section(raw, "Edge cases")),
        failure_modes=_bullets(_section(raw, "Failure modes")),
        implementation=_numbered(_section(raw, "Concrete implementation")),
        verification=_table_rows(_section(raw, "Verification")),
        artifacts=_bullets(_section(raw, "Repo artifacts (this branch)") or _section(raw, "Repo artifacts")),
        dependencies=_table_rows(_section(raw, "Dependencies")),
        acceptance=_bullets(_section(raw, "Acceptance criteria")),
        adversarial=_bullets(_section(raw, "Adversarial review")),
        reader_narrative=_section(raw, "Reader narrative"),
        source_path=str(path.relative_to(ROOT)).replace("\\", "/"),
    )
    node.narrative = _compose_narrative(node.purpose, node.behavior_steps, node.title)
    return node


def load_all_nodes(out_dir: Path, quality_nodes: dict | None = None) -> list[ParsedNode]:
    quality_nodes = quality_nodes or {}
    nodes: list[ParsedNode] = []
    for path in list_leaf_paths(out_dir):
        n = parse_markdown(path)
        q = quality_nodes.get(n.id)
        if q:
            n.quality = {
                "aggregate": q.get("aggregate"),
                "structure": q.get("structure"),
                "specificity": q.get("specificity"),
                "research": q.get("research"),
                "depth": q.get("depth"),
                "iteration": q.get("iteration"),
                "review": q.get("review"),
            }
        nodes.append(n)
    return nodes


def write_node_json(node: ParsedNode, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(node.to_dict(), indent=2) + "\n", encoding="utf-8")
