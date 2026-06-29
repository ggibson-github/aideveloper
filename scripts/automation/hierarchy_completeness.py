#!/usr/bin/env python3
"""Strict completeness audit for hierarchy leaf documents (S0)."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

# Meta-scaffolding: describes the expansion process, not the node design.
META_SCAFFOLD_PATTERNS = [
    r"action=deepen",
    r"action=expand",
    r"Conductor or `/loop` wake selects this item",
    r"Mark queue item `done`",
    r"Multi-pass quality",
]

GENERIC_CONTENT_PATTERNS = [
    r"Implement '.*' per parent index",
    r"Exact ship release \(v2\.14",
    r"Authoritative design for \*\*.*\*\* \(`",
    r"Deferred questions",
    r"TBD for `",
    r"\bTODO\b",
    r"\bFIXME\b",
    r"<placeholder>",
    r"Generated 20\d\d-\d\d-\d\d hierarchy item",
]

GENERIC_JSON_MARKERS = [
    r'"node"\s*:\s*"[^"]+"\s*,\s*"description"\s*:',
    r'"implemented_in_release"\s*:\s*"v2\.14\+"',
]

REQUIRED_SECTIONS = [
    "## Purpose",
    "## Scope",
    "## Behavior",
    "## Edge cases",
    "## Failure modes",
    "## Concrete implementation",
    "## Adversarial review",
    "## Acceptance criteria",
]

REQUIRED_DEPTH_MARKERS = ["```mermaid", "## JSON example"]


def list_leaf_paths(out_dir: Path) -> list[Path]:
    return sorted(
        p
        for p in out_dir.glob("*.md")
        if p.name != "INDEX.md"
        and not p.name.endswith("-index.md")
        and "platform-queue-index" not in p.name
        and p.name != "H3-SIGNOFF-BUNDLE.md"
    )


def item_id_from_path(path: Path, text: str) -> str:
    m = re.search(r"hierarchy item ([A-Z0-9\.-]+)", text[:300])
    if m:
        return m.group(1)
    stem = path.stem
    try:
        from hierarchy_queue_data import LEAVES, STANDALONE_DOCUMENTS  # noqa: WPS433

        known = list(LEAVES.keys()) + [d["id"] for d in STANDALONE_DOCUMENTS]
        matches = [lid for lid in known if stem == lid or stem.startswith(lid + "-")]
        if matches:
            return max(matches, key=len)
    except ImportError:
        pass
    m_h = re.search(r"^#\s+([A-Z][A-Z0-9.-]*):\s", text, re.MULTILINE)
    if m_h:
        return m_h.group(1)
    m2 = re.match(r"([A-Z0-9\.-]+)-", path.name)
    return m2.group(1) if m2 else path.stem


def title_from_path(path: Path, item_id: str) -> str:
    return path.stem.replace(item_id + "-", "").replace("-", " ")


def prose_word_count(text: str) -> int:
    stripped = re.sub(r"```[\s\S]*?```", " ", text)
    stripped = re.sub(r"[#|`\[\]()>-]", " ", stripped)
    return len(re.findall(r"[a-zA-Z]{3,}", stripped))


def body_fingerprint(text: str) -> str:
    """Normalize body for duplicate detection."""
    norm = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    norm = re.sub(r"```[\s\S]*?```", "BLOCK", norm)
    norm = re.sub(r"#+ .*", "", norm)
    norm = re.sub(r"\s+", " ", norm).strip().lower()
    return hashlib.sha256(norm.encode()).hexdigest()[:16]


def score_doc_completeness(
    text: str,
    item_id: str,
    title: str,
    *,
    threshold: int = 90,
    min_lines: int = 100,
    min_words: int = 400,
) -> tuple[int, list[str], bool]:
    """Return (score, reasons, is_complete). is_complete iff score >= threshold and no blockers."""
    reasons: list[str] = []
    lines = len(text.splitlines())

    if lines < min_lines:
        reasons.append(f"short ({lines} lines, need >={min_lines})")

    words = prose_word_count(text)
    if words < min_words:
        reasons.append(f"thin prose ({words} words, need >={min_words})")

    for pat in META_SCAFFOLD_PATTERNS:
        if re.search(pat, text, re.IGNORECASE):
            reasons.append(f"meta-scaffold: {pat[:48]}")
            break

    for pat in GENERIC_CONTENT_PATTERNS:
        if re.search(pat, text):
            # Only flag generic implement fallback when it appears in behavior (not historical enrich docs)
            if "Implement '" in pat and "## Behavior" in text:
                beh = re.search(r"## Behavior[^\n]*\n([\s\S]*?)(?=\n## |\Z)", text)
                if not beh or not re.search(pat, beh.group(1)):
                    continue
            reasons.append(f"generic/scaffold: {pat[:48]}")
            break

    for sec in REQUIRED_SECTIONS:
        if sec not in text:
            reasons.append(f"missing section: {sec}")

    for marker in REQUIRED_DEPTH_MARKERS:
        if marker not in text:
            reasons.append(f"missing: {marker}")

    json_block = re.search(r"## JSON example\s*\n(```[\s\S]*?```)", text)
    if json_block:
        jb = json_block.group(1)
        if all(re.search(p, jb) for p in GENERIC_JSON_MARKERS[:1]) and item_id in jb:
            if not any(k in jb for k in ("goal", "platform", "pursuit", "state", "pack", "verify")):
                reasons.append("JSON example is generic stub only")

    behavior = ""
    bm = re.search(r"## Behavior[^\n]*\n([\s\S]*?)(?=\n## |\Z)", text)
    if bm:
        behavior = bm.group(1)
    title_words = [w.lower() for w in re.findall(r"[a-zA-Z]{4,}", title) if w.lower() not in ("with", "from", "every", "into")]
    if title_words:
        hits = sum(1 for w in title_words[:5] if w in behavior.lower())
        if hits < 1:
            reasons.append("behavior section lacks node-specific terms from title")

    numbered_steps = len(re.findall(r"^\d+\.\s", behavior, re.MULTILINE))
    if numbered_steps < 3:
        reasons.append(f"behavior has fewer than 3 concrete steps ({numbered_steps})")

    edge = re.search(r"## Edge cases\s*\n([\s\S]*?)(?=\n## |\Z)", text)
    if edge:
        edge_bullets = len(re.findall(r"^- ", edge.group(1), re.MULTILINE))
        if edge_bullets < 3:
            reasons.append(f"edge cases need >= 3 bullets ({edge_bullets})")

    fail = re.search(r"## Failure modes\s*\n([\s\S]*?)(?=\n## |\Z)", text)
    if fail and fail.group(1).count("**") < 3:
        reasons.append("failure modes need >= 3 entries")

    impl = re.search(r"## Concrete implementation\s*\n([\s\S]*?)(?=\n## |\Z)", text)
    if impl:
        numbered = len(re.findall(r"^\d+\.\s", impl.group(1), re.MULTILINE))
        if numbered < 3:
            reasons.append("concrete implementation need >= 3 numbered steps")

    if "## Adversarial review" in text and "### Revisions applied" not in text:
        reasons.append("adversarial review missing revisions")

    ac = re.search(r"## Acceptance criteria\s*\n([\s\S]*?)(?=\n## |\Z)", text)
    if ac and "python scripts" not in ac.group(1) and "pytest" not in ac.group(1):
        reasons.append("acceptance criteria lack concrete verify command")

    penalty = len(reasons) * 12 + max(0, min_lines - lines) + max(0, (min_words - words) // 20)
    score = max(0, 100 - penalty)
    is_complete = score >= threshold and len(reasons) == 0
    return score, reasons, is_complete


def audit_directory(
    out_dir: Path,
    *,
    threshold: int = 90,
) -> dict:
    leaves = list_leaf_paths(out_dir)
    incomplete: list[dict] = []
    fingerprints: dict[str, list[str]] = {}

    for p in leaves:
        text = p.read_text(encoding="utf-8")
        iid = item_id_from_path(p, text)
        title = title_from_path(p, iid)
        score, reasons, is_complete = score_doc_completeness(
            text, iid, title, threshold=threshold
        )
        fp = body_fingerprint(text)
        fingerprints.setdefault(fp, []).append(iid)
        if not is_complete:
            incomplete.append({
                "id": iid,
                "path": str(p.relative_to(ROOT)),
                "score": score,
                "reasons": reasons,
            })

    dupes = {fp: ids for fp, ids in fingerprints.items() if len(ids) > 25}
    dupe_issues = []
    for fp, ids in dupes.items():
        dupe_issues.append({"fingerprint": fp, "ids": ids[:8], "count": len(ids)})

    for item in incomplete:
        iid = item["id"]
        for dupe in dupe_issues:
            if iid in dupe["ids"]:
                item["reasons"].append(f"duplicate body cluster ({dupe['count']} similar docs)")
                break

    return {
        "audited": len(leaves),
        "incomplete": len(incomplete),
        "threshold": threshold,
        "ready_for_signoff": len(incomplete) == 0 and not dupe_issues,
        "duplicate_clusters": len(dupe_issues),
        "items": incomplete,
        "duplicates": dupe_issues[:10],
    }
