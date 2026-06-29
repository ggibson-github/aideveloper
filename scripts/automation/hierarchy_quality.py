#!/usr/bin/env python3
"""Multi-dimensional quality measures for hierarchy leaf documents."""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field

from hierarchy_completeness import (
    META_SCAFFOLD_PATTERNS,
    REQUIRED_DEPTH_MARKERS,
    REQUIRED_SECTIONS,
    body_fingerprint,
    item_id_from_path,
    list_leaf_paths,
    prose_word_count,
    score_doc_completeness,
    title_from_path,
)

# Minimum per-dimension score for hierarchy certification
CERT_DIMENSION_MIN = 70
CERT_AGGREGATE_MIN = 85

DIMENSION_WEIGHTS = {
    "structure": 0.15,
    "specificity": 0.20,
    "research": 0.25,
    "depth": 0.20,
    "iteration": 0.10,
    "review": 0.10,
}


@dataclass
class DocQuality:
    id: str
    path: str
    branch: str
    title: str
    structure: int
    specificity: int
    research: int
    depth: int
    iteration: int
    review: int
    aggregate: float
    iteration_pass: int
    word_count: int
    line_count: int
    sources: list[str] = field(default_factory=list)
    gaps: list[str] = field(default_factory=list)
    certified: bool = False

    def to_dict(self) -> dict:
        return asdict(self)


def branch_for(item_id: str) -> str:
    if item_id.startswith("INTRO") or item_id.startswith("MASTER"):
        return "meta"
    if item_id.startswith("SEC") or item_id.startswith("APP"):
        return "meta"
    m = re.match(r"^([A-J])", item_id)
    return m.group(1) if m else "meta"


def iteration_pass_from_text(text: str) -> int:
    m = re.search(r"<!-- Complete pass (\d+)", text)
    if m:
        return int(m.group(1))
    m2 = re.search(r"<!-- (?:Expanded|Deepened|Challenged) [^>]+ (\d{4}-\d{2}-\d{2}) ", text)
    return 1 if m2 else 0


def score_structure(text: str) -> tuple[int, list[str]]:
    gaps: list[str] = []
    score = 100
    for sec in REQUIRED_SECTIONS:
        if sec not in text:
            gaps.append(f"missing {sec}")
            score -= 12
    for marker in REQUIRED_DEPTH_MARKERS:
        if marker not in text:
            gaps.append(f"missing {marker}")
            score -= 8
    for pat in META_SCAFFOLD_PATTERNS:
        if re.search(pat, text, re.IGNORECASE):
            gaps.append("meta-scaffold")
            score -= 20
            break
    return max(0, score), gaps


def score_specificity(text: str, item_id: str, title: str) -> tuple[int, list[str]]:
    gaps: list[str] = []
    score = 100
    bm = re.search(r"## Behavior[^\n]*\n([\s\S]*?)(?=\n## |\Z)", text)
    behavior = bm.group(1) if bm else ""
    if item_id not in text:
        gaps.append("item id not referenced in body")
        score -= 15
    title_words = [w.lower() for w in re.findall(r"[a-zA-Z]{4,}", title) if w.lower() not in ("with", "from", "every", "into", "goal")]
    hits = sum(1 for w in title_words[:6] if w in behavior.lower())
    if title_words and hits == 0:
        gaps.append("behavior lacks title-specific terms")
        score -= 25
    elif hits == 1:
        score -= 5
    steps = len(re.findall(r"^\d+\.\s", behavior, re.MULTILINE))
    if steps < 3:
        gaps.append(f"behavior steps={steps}")
        score -= 15
    if re.search(r"Implement '.*' per parent index", behavior):
        gaps.append("generic behavior fallback")
        score -= 30
    return max(0, score), gaps


def score_research(text: str, item_id: str) -> tuple[int, list[str], list[str]]:
    """Evidence that vision/repo context was gathered into the doc."""
    gaps: list[str] = []
    sources: list[str] = []
    checks = [
        (r"full-automation-vision-and-hierarchy\.md", "vision master"),
        (r"genius-conductor-tiered-routing\.md", "routing doc"),
        (r"scripts/", "repo scripts"),
        (r"\.cursor/skills/", "skills"),
        (r"journal/state\.json|state\.json", "state schema"),
        (r"docs/manifest/|docs/operator/|docs/playbooks/", "operator/manifest"),
        (r"template-packs/", "template-packs"),
        (r"tests/unit/", "unit tests"),
        (r"Hierarchy context", "vision tree context"),
    ]
    hit = 0
    for pat, label in checks:
        if re.search(pat, text):
            hit += 1
            sources.append(label)
    score = min(100, int(hit / len(checks) * 100 + 20))
    if hit < 4:
        gaps.append(f"research refs={hit}/{len(checks)}")
        score = min(score, 50 + hit * 10)
    if "python scripts" not in text and "pytest" not in text:
        gaps.append("no verify command reference")
        score -= 10
    return max(0, score), gaps, sources


def score_depth(text: str) -> tuple[int, list[str]]:
    gaps: list[str] = []
    lines = len(text.splitlines())
    words = prose_word_count(text)
    score = 100
    if lines < 100:
        gaps.append(f"lines={lines}")
        score -= min(40, 100 - lines)
    if words < 400:
        gaps.append(f"words={words}")
        score -= min(30, (400 - words) // 10)
    edge = re.search(r"## Edge cases\s*\n([\s\S]*?)(?=\n## |\Z)", text)
    if edge:
        n = len(re.findall(r"^- ", edge.group(1), re.MULTILINE))
        if n < 3:
            gaps.append(f"edge_cases={n}")
            score -= 10
    impl = re.search(r"## Concrete implementation\s*\n([\s\S]*?)(?=\n## |\Z)", text)
    if impl:
        n = len(re.findall(r"^\d+\.\s", impl.group(1), re.MULTILINE))
        if n < 3:
            gaps.append(f"impl_steps={n}")
            score -= 10
    return max(0, score), gaps


def score_iteration(text: str, ledger_pass: int | None = None) -> tuple[int, list[str], int]:
    gaps: list[str] = []
    doc_pass = iteration_pass_from_text(text)
    effective = max(doc_pass, ledger_pass or 0)
    if effective == 0:
        gaps.append("never iterated (no Complete pass marker)")
        return 0, gaps, 0
    score = min(100, 60 + effective * 15)  # pass 1→75, 2→90, 3+→100 (default pipeline runs 3)
    if effective < 1:
        gaps.append("iteration pass < 1")
    return score, gaps, effective


def score_review(text: str) -> tuple[int, list[str]]:
    gaps: list[str] = []
    score = 0
    if "## Adversarial review" in text:
        score += 50
    else:
        gaps.append("no adversarial review")
    if "### Revisions applied" in text:
        score += 30
    else:
        gaps.append("no revisions applied")
    if "## Sign-off readiness" in text or "strict audit" in text.lower():
        score += 20
    return min(100, score), gaps


def measure_doc_quality(
    text: str,
    item_id: str,
    title: str,
    path: str,
    *,
    ledger_pass: int | None = None,
) -> DocQuality:
    s, sg = score_structure(text)
    sp, spg = score_specificity(text, item_id, title)
    r, rg, sources = score_research(text, item_id)
    d, dg = score_depth(text)
    it, itg, ipass = score_iteration(text, ledger_pass)
    rv, rvg = score_review(text)

    dims = {"structure": s, "specificity": sp, "research": r, "depth": d, "iteration": it, "review": rv}
    aggregate = round(sum(dims[k] * DIMENSION_WEIGHTS[k] for k in DIMENSION_WEIGHTS), 1)
    gaps = sg + spg + rg + dg + itg + rvg

    _, _, complete = score_doc_completeness(text, item_id, title, threshold=90)
    certified = (
        aggregate >= CERT_AGGREGATE_MIN
        and all(dims[k] >= CERT_DIMENSION_MIN for k in dims)
        and complete
    )

    return DocQuality(
        id=item_id,
        path=path,
        branch=branch_for(item_id),
        title=title,
        structure=s,
        specificity=sp,
        research=r,
        depth=d,
        iteration=it,
        review=rv,
        aggregate=aggregate,
        iteration_pass=ipass,
        word_count=prose_word_count(text),
        line_count=len(text.splitlines()),
        sources=sources,
        gaps=gaps,
        certified=certified,
    )


def hierarchy_depth_from_ids(ids: list[str]) -> int:
    depths = []
    for iid in ids:
        parts = iid.replace("SEC-15-", "").replace("SEC-17-", "").split(".")
        depths.append(len(parts) + iid.count("-"))
    return max(depths) if depths else 0


def aggregate_branch_scores(docs: list[DocQuality]) -> dict[str, dict]:
    by_branch: dict[str, list[DocQuality]] = {}
    for d in docs:
        by_branch.setdefault(d.branch, []).append(d)
    out = {}
    for branch, items in sorted(by_branch.items()):
        n = len(items)
        out[branch] = {
            "nodes": n,
            "aggregate_avg": round(sum(x.aggregate for x in items) / n, 1),
            "structure_avg": round(sum(x.structure for x in items) / n, 1),
            "research_avg": round(sum(x.research for x in items) / n, 1),
            "certified": sum(1 for x in items if x.certified),
        }
    return out
