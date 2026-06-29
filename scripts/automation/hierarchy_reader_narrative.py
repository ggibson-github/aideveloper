#!/usr/bin/env python3
"""Generate human-readable teaching prose for hierarchy capability pages (book mode)."""

from __future__ import annotations

import re

from hierarchy_book_structure import (  # noqa: E402
    GROUP_CATALOG,
    META_GROUP_TITLES,
    group_title,
    plane_intro,
)
from hierarchy_html_parse import ParsedNode  # noqa: E402
from hierarchy_html_rules import is_conceptual_capability  # noqa: E402
from hierarchy_prose import ProseContext  # noqa: E402
from hierarchy_vision_context import section_for_branch  # noqa: E402


def readable_title(title: str) -> str:
    """Turn snake_case spec titles into readable phrases."""
    t = title.strip()
    if re.match(r"^[a-z0-9_]+( [a-z0-9_]+)+$", t):
        parts = [p.replace("_", " ") for p in t.split()]
        if len(parts) == 1:
            return parts[0]
        if len(parts) == 2:
            return f"{parts[0]} and {parts[1]}"
        return ", ".join(parts[:-1]) + f", and {parts[-1]}"
    return t.replace("_", " ")


from hierarchy_queue_data import LEAVES  # noqa: E402


def display_title(node: ParsedNode) -> str:
    """Human-facing page title."""
    if node.id in LEAVES:
        raw = LEAVES[node.id]
    else:
        raw = node.title
    t = raw.replace("_", " ").strip()
    if len(t) > 55 and " " in t:
        return t[0].upper() + t[1:]
    return readable_title(raw)


def _vision_phrase(ctx: ProseContext, item_id: str) -> str:
    sec = section_for_branch(item_id) or "§3"
    return ctx.vision_md_link(sec)


def _strip_spec_boilerplate(purpose: str, item_id: str) -> str:
    p = purpose.strip()
    p = re.sub(
        rf"^{re.escape(item_id)} defines (.+?) for the agent-driven expert system\.?\s*",
        r"\1. ",
        p,
        flags=re.I,
    )
    for noise in (
        r"Pursuit & control plane — autonomous loops until goal verified\.?\s*",
        r"Cognition & routing — S0–S4, conductor, workers, dual-stack\.?\s*",
        r"Product execution plane[^.]*\.?\s*",
        r"Platform evolution plane[^.]*\.?\s*",
    ):
        p = re.sub(noise, "", p, flags=re.I)
    return p.strip()


def _scope_prose(node: ParsedNode) -> list[str]:
    lines: list[str] = []
    for bullet in node.scope[:4]:
        b = bullet.strip()
        if b.lower().startswith("owns "):
            continue
        if "conflicts resolve" in b.lower():
            continue
        if "hitl" in b.lower():
            lines.append(
                "The design keeps human involvement minimal: approve the plan at H1, "
                "assist when blocked at H2, and sign off verified outcomes at H3."
            )
            continue
        if b.startswith("Aligns with"):
            continue
        lines.append(b.rstrip("."))
    return lines


def _plane_context(branch: str) -> str:
    intro = plane_intro(branch)
    if intro:
        return intro
    return f"This capability belongs to architectural plane {branch}."


def _group_context(group_id: str) -> str:
    if group_id in META_GROUP_TITLES:
        return f"This section belongs to {group_id}: {META_GROUP_TITLES[group_id]}."
    if group_id in GROUP_CATALOG:
        return f"This section is part of **{group_id}: {GROUP_CATALOG[group_id]['title']}**."
    if group_id in ("INTRO-0", "INTRO-1"):
        return "This section introduces the overall automation vision and operating model."
    if group_id.startswith("SEC-"):
        return "This section documents cross-cutting architecture, roadmap, or open decisions."
    if group_id.startswith("MASTER"):
        return "This chapter summarizes a top-level architectural plane."
    return ""


def build_branch_story_md(branch_id: str, branch_title: str, group_ids: list[str]) -> str:
    from hierarchy_book_structure import META_GROUP_TITLES, ordered_group_ids  # noqa: WPS433

    if branch_id == "meta":
        return (
            f"{plane_intro('meta')}\n\n"
            "Use the numbered chapter list below in order. Each link opens a chapter; "
            "within each chapter, open individual sections for diagrams and verification."
        )
    intro = plane_intro(branch_id) or f"Plane {branch_id} groups related capabilities."
    return (
        f"{intro}\n\n"
        f"This plane has {len(group_ids)} topic groups listed below. "
        f"Open a group to see its capabilities; sequential groups include a flow diagram."
    )


def build_group_story_md(group_id: str, nodes: list[ParsedNode], branch_title: str) -> str:
    from hierarchy_book_structure import META_GROUP_INTROS  # noqa: WPS433

    if group_id in META_GROUP_INTROS:
        title = group_title(group_id)
        count = len(nodes)
        return (
            f"{META_GROUP_INTROS[group_id]} "
            f"This chapter ({title}) contains {count} sections—open each for diagrams, verification, and contracts."
        )
    title = group_title(group_id)
    count = len(nodes)
    seq = (
        "The capabilities below follow a sequential flow—read them in order."
        if group_id in {"A2", "C2", "D2", "E2", "G2", "SEC-15", "APP-A"}
        else "The capabilities below are related contracts within this topic."
    )
    return (
        f"{group_id}: {title} — a chapter within {branch_title}. "
        f"{seq} {count} capabilities are listed below."
    )


_AGENT_MARKER = re.compile(r"<!--\s*prose-source:\s*agent[^>]*-->\s*", re.I)
_MIN_CHAPTER_WORDS = 35
MIN_READER_NARRATIVE_WORDS = 40

# Template openers from build_reader_story_md / _group_context — not substantive author prose.
_TEMPLATE_READER_OPENERS = re.compile(
    r"^(This section is part of|This section belongs to|This section documents|"
    r"This section introduces|This chapter summarizes)",
    re.I,
)


def reader_narrative_word_count(text: str) -> int:
    """Word count after stripping agent prose-source marker."""
    cleaned = _AGENT_MARKER.sub("", text).strip()
    return len(re.findall(r"\w+", cleaned))


def should_preserve_reader_narrative(section_text: str) -> bool:
    """
    Return True when an existing ## Reader narrative must not be replaced by template prose.

    Preserves agent-marked prose and any narrative at or above the book word minimum.
    """
    body = section_text.strip()
    if not body:
        return False
    if _AGENT_MARKER.search(body):
        return True
    return reader_narrative_word_count(body) >= MIN_READER_NARRATIVE_WORDS


def _clean_reader_narrative(text: str) -> str:
    return _AGENT_MARKER.sub("", text).strip()


def build_chapter_story_md(
    group_id: str,
    nodes: list[ParsedNode],
    branch_title: str,
    *,
    branch_id: str = "",
) -> str:
    """Chapter page prose: prefer agent Reader narrative over template group blurbs."""
    from hierarchy_book_structure import META_GROUP_INTROS  # noqa: WPS433

    narratives = [
        clean
        for n in nodes
        if (clean := _clean_reader_narrative(n.reader_narrative))
        and len(clean.split()) >= _MIN_CHAPTER_WORDS
    ]

    if len(nodes) == 1 and narratives:
        return narratives[0]

    if branch_id in "ABCDEFGHIJ" and narratives and len(narratives) == len(nodes):
        title = group_title(group_id)
        seq = (
            "The capabilities below follow a sequential flow—read them in order."
            if group_id in {"A2", "C2", "D2", "E2", "G2", "SEC-15", "APP-A"}
            else "Open each capability below for diagrams, verification, and contracts."
        )
        body_parts = narratives[:5]
        if len(nodes) > 5:
            return (
                f"{group_id}: {title}. {seq}\n\n"
                + "\n\n".join(body_parts)
                + f"\n\n({len(nodes)} capabilities in this chapter.)"
            )
        return f"{group_id}: {title}. {seq}\n\n" + "\n\n".join(body_parts)

    if branch_id == "meta" and narratives:
        intro = META_GROUP_INTROS.get(group_id, "")
        if len(nodes) <= 3 and len(narratives) == len(nodes):
            parts = [p for p in ([intro] if intro else []) + narratives if p]
            return "\n\n".join(parts)
        seq = (
            "The sections below follow release order—read them in sequence."
            if group_id in {"SEC-15", "APP-A"}
            else "Open each section below for diagrams, verification, and contracts."
        )
        lead = f"{intro}\n\n{seq}" if intro else seq
        if narratives and len(nodes) > 3:
            lead += "\n\n" + narratives[0].split("\n\n")[0]
        return lead

    return build_group_story_md(group_id, nodes, branch_title)


def build_reader_story_md(node: ParsedNode, ctx: ProseContext, branch_title: str) -> str:
    """Full teaching prose for ## Reader narrative."""
    from hierarchy_book_structure import capability_group_id

    gid = capability_group_id(node.id)
    topic = display_title(node)
    parts: list[str] = []

    gc = _group_context(gid)
    if gc:
        parts.append(gc)

    cleaned = _strip_spec_boilerplate(node.purpose, node.id)
    if cleaned and len(cleaned) > 25:
        lead = cleaned[0].upper() + cleaned[1:] if cleaned[0].islower() else cleaned
        if not lead.endswith("."):
            lead += "."
        parts.append(f"**{topic}** — {lead}")
    else:
        parts.append(
            f"**{topic}** specifies one contract in the expert system: what must hold, "
            f"how the system behaves, and how operators know it succeeded."
        )

    parts.append(_plane_context(node.branch))

    for line in _scope_prose(node):
        parts.append(line + ("." if not line.endswith(".") else ""))

    if node.edge_cases:
        sample = node.edge_cases[0].split("—")[0].strip().rstrip(".")
        parts.append(
            f"Designers should plan for real-world friction—for example: {sample.lower()}."
        )

    if node.verification:
        parts.append(
            "Success is not assumed: explicit verification commands and evidence paths "
            "are part of this contract."
        )

    if node.acceptance:
        parts.append(
            "Acceptance criteria define when this capability is considered correctly implemented."
        )

    parts.append(f"See {_vision_phrase(ctx, node.id)} for how this plane fits the full architecture.")
    return "\n\n".join(parts)


def humanize_timeline_step(step: str, node: ParsedNode) -> str:
    """Turn spec-style behavior steps into short teaching sentences."""
    s = step.strip()
    s = re.sub(r"\[\[+", "[", s)
    s = re.sub(r"\]\([^)]+\)(?: — [^\[]+\]\([^)]+\))+", "", s)

    low = s.lower()
    topic = readable_title(node.title)

    # Agent-authored timelines are already reader-ready; only strip corrupted link tails.
    if not low.startswith("define and implement") and "map `" not in low and "sec-15-index" not in low:
        if "establish " not in low or "pursuit and state records" not in low:
            s = re.sub(r" per \[[^\]]+\]\([^)]+\)(?:[^\[]+\[[^\]]+\]\([^)]+\))*\.?", ".", s)
            return s if len(s) > 20 else s

    if is_conceptual_capability(node.id, node.branch):
        if low.startswith("define and implement") or low.startswith("implement "):
            return (
                f"Defines {topic} for the expert system—what must hold, who it affects, "
                f"and how later plane specs build on it."
            )
        s = re.sub(r" per \[[^\]]+\]\([^)]+\)(?:[^\[]+\[[^\]]+\]\([^)]+\))*\.?", ".", s)
        return s if len(s) > 20 else f"Clarifies how {topic} fits the overall architecture."

    if low.startswith("define and implement") or low.startswith("implement "):
        return (
            f"Establish {topic} in pursuit and state records, aligned with the "
            f"Plane {node.branch} design."
        )
    if "prefer" in low and "s0" in low:
        return (
            "When behavior maps to an existing script under `scripts/`, run the S0 "
            "deterministic path first ([Deterministic-first rule](B1.1-s0-deterministic-mandatory-first.md))."
        )
    if "unit test" in low or "test_" in low:
        return "Add or extend automated tests so regressions cannot pass unnoticed."
    if "dual-write" in low:
        return "Record outcomes in both the human journal and machine state for safe resume."
    if "preflight" in low or "check-pipeline-blocked" in low:
        return "Run preflight; proceed only when the pipeline reports READY."
    if "execute" in low and "step" in low:
        return "Execute exactly one pipeline skill phase, then capture evidence."
    if "goal_verify" in low or "goal_scope" in low:
        return "When scope is complete, run goal-level verification—not only task-level checks."
    if "h3" in low and "pending" in low:
        return "On successful goal verification, request final human sign-off (H3)."
    if "loop until" in low:
        return "Repeat the pursuit cycle until blocked, out of budget, complete, or rejected at H3."
    if "on failure" in low and "h2" in low:
        return "On failure, stop and surface a structured H2 blocker—never mark done without proof."
    if "catalog" in low or "compose" in low:
        return "Resolve catalog components before improvising new implementation."
    if "pack" in low and node.branch == "F":
        return "Update the template-pack artifact so roles and pipelines can bind to it."

    s = re.sub(r" per \[[^\]]+\]\([^)]+\)(?:[^\[]+\[[^\]]+\]\([^)]+\))*\.?", ".", s)
    return s if len(s) > 20 else f"Apply the {topic} contract during normal operation."
