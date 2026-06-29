#!/usr/bin/env python3
"""Derive subject-only timeline steps from agent reader narratives and hierarchy context."""

from __future__ import annotations

import re

from hierarchy_book_structure import GROUP_CATALOG, capability_group_id
from hierarchy_html_rules import is_conceptual_capability
from hierarchy_leaf_builder import node_specific_behavior
from hierarchy_queue_data import LEAVES
from hierarchy_reader_narrative import readable_title

OPERATIONAL_KEYWORDS = (
    "when",
    "run",
    "conductor",
    "operator",
    "before",
    "after",
    "on failure",
    "must",
    "never",
    "dual-write",
    "verify",
    "enqueue",
    "dequeue",
    "stop",
    "block",
    "preflight",
    "at h1",
    "at pursuit",
    "if ",
    "exit 0",
    "platform turn",
    "goal_",
    "next_action",
    "worker",
    "autopilot",
    "drain",
    "scheduler",
    "promotion",
    "catalog",
    "compose",
    "pack",
    "role",
    "pipeline",
    "evidence",
    "journal",
    "state.json",
    "h2",
    "h3",
    "s0",
    "spawn",
    "merge",
    "route",
)


def _strip_inline_md(text: str) -> str:
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    return text.strip()


def _split_sentences(text: str) -> list[str]:
    parts = re.split(r'(?<=[.!?])\s+(?=[A-Z"\'(])', text)
    return [p.strip() for p in parts if p.strip()]


def _operational_score(sentence: str) -> int:
    low = sentence.lower()
    return sum(1 for kw in OPERATIONAL_KEYWORDS if kw in low)


def _to_imperative_step(sentence: str) -> str:
    s = _strip_inline_md(sentence).rstrip(".")
    transforms: tuple[tuple[str, str], ...] = (
        (r"^Every pursuit in the expert system begins with", "At goal creation, establish"),
        (r"^Every pursuit begins with", "At goal creation, establish"),
        (r"^This capability defines", "Ensure the system upholds"),
        (r"^This capability requires", "Require that"),
        (r"^This chapter is", "Use this chapter as"),
        (r"^The type enum is not cosmetic\. It tells", "Use goal_type to tell"),
        (r"^It tells", "Use the type enum to tell"),
        (r"^Operators set these fields at H1", "At H1, operators set these fields"),
        (r"^When criteria change mid-pursuit, the conductor must", "When criteria change mid-pursuit, the conductor"),
        (r"^Designers should treat", "Treat"),
        (r"^Autonomous pursuit without bounds", "Enforce budget and deadline fields so pursuit"),
        (r"^Today's harness", "Recognize that today's harness"),
        (r"^The target is", "The north-star system"),
        (r"^Plane [A-J] is", "Understand that this plane"),
        (r"^Release v2\.\d+", "This release slice"),
        (r"^Improve platform work is", "Classify improve-platform work as"),
    )
    for pattern, repl in transforms:
        updated = re.sub(pattern, repl, s, flags=re.I)
        if updated != s:
            return updated
    return s


def domain_steps(item_id: str, title: str, branch: str) -> list[str]:
    """Domain-specific pursuit steps from leaf builder (never generic implement-per-vision)."""
    steps = node_specific_behavior(item_id, title, branch, pass_num=1)
    out: list[str] = []
    for step in steps:
        low = step.lower()
        if low.startswith("define and implement"):
            continue
        if "pass 3:" in low or "pass 2:" in low:
            continue
        if "cross-check parent index" in low:
            continue
        out.append(step)
    if out:
        return out[:5]

    topic = readable_title(LEAVES.get(item_id, title))
    gid = capability_group_id(item_id)
    group_title = GROUP_CATALOG.get(gid, {}).get("title", gid)

    if is_conceptual_capability(item_id, branch):
        return [
            f"Defines {topic} for readers and implementers—what the expert system must uphold.",
            f"Downstream specs in {group_title} assume this framing; conflicts escalate to H2, not silent drift.",
            "Consult the reader narrative above for authoritative context before changing related plane specs.",
        ]

    return [
        f"During pursuit, enforce the {topic} contract within {group_title} (Plane {branch}).",
        "Run [S0](B1.1-s0-deterministic-mandatory-first.md) scripts before improvising when file-derived behavior exists.",
        "Dual-write journal and state.json after the step; attach evidence when verification applies.",
        "On failure or missing prerequisites, stop with structured H2—never mark done without proof.",
    ]


def steps_from_narrative(
    reader_md: str,
    *,
    item_id: str,
    title: str,
    branch: str,
) -> list[str]:
    """Extract 3–5 operational steps from an agent-authored reader narrative."""
    text = re.sub(r"<!--.*?-->", "", reader_md, flags=re.S).strip()
    if not text:
        return domain_steps(item_id, title, branch)

    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    steps: list[str] = []
    seen: set[str] = set()

    for para in paragraphs:
        plain = _strip_inline_md(para)
        sentences = _split_sentences(plain)
        if not sentences:
            continue

        ranked = sorted(
            sentences,
            key=lambda s: (_operational_score(s), len(s)),
            reverse=True,
        )
        chosen = ""
        for candidate in ranked:
            low = candidate.lower()
            if low.startswith("see vision") or low.startswith("see [vision"):
                continue
            if len(candidate) < 20:
                continue
            if _operational_score(candidate) == 0 and steps:
                continue
            chosen = candidate
            break
        if not chosen and sentences and len(steps) < 2:
            chosen = sentences[0]
        if not chosen or chosen in seen:
            continue
        seen.add(chosen)
        steps.append(_to_imperative_step(chosen))
        if len(steps) >= 5:
            break

    if len(steps) < 3:
        for extra in domain_steps(item_id, title, branch):
            if extra not in steps:
                steps.append(extra)
            if len(steps) >= 5:
                break

    if not any(re.search(r"\bh2\b|failure|fail closed|do not mark", s, re.I) for s in steps):
        steps.append(
            "On failure, ambiguity, or missing evidence, stop with a structured H2 blocker—"
            "never mark the step or queue item done without proof."
        )

    return steps[:5]
