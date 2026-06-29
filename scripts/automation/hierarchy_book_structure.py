#!/usr/bin/env python3
"""Book structure: plane → group → capability hierarchy for HTML publication."""

from __future__ import annotations

import re
from collections import defaultdict

from hierarchy_queue_data import EXPAND_NODES, LEAVES  # noqa: E402

# Groups where leaf order is a sequential flow (show arrow diagram).
SEQUENTIAL_GROUPS = frozenset({
    "A2", "C2", "D2", "E2", "E6", "E7", "G2", "I2",
    "SEC-15", "APP-A",
})

# Book order for meta branch groups (front matter → appendices).
META_GROUP_ORDER: list[str] = [
    "INTRO-0", "INTRO-1", "INTRO-2", "MASTER", "SEC-13", "SEC-14", "SEC-15", "SEC-17", "SEC-18", "APP-A", "APP-B",
]

META_GROUP_TITLES: dict[str, str] = {
    "INTRO-0": "Executive summary (§0)",
    "INTRO-1": "North star definition (§1)",
    "INTRO-2": "Transistor building blocks north star (§19)",
    "MASTER": "Master hierarchy — planes A–J (§2)",
    "SEC-13": "End-to-end pursuit flow (§13)",
    "SEC-14": "Gap analysis: today → target (§14)",
    "SEC-15": "Implementation roadmap v2.14–v2.28 (§15)",
    "SEC-17": "Open design decisions (§17)",
    "SEC-18": "Transistor model A–Z reference (§19)",
    "APP-A": "Full human job taxonomy (§18)",
    "APP-B": "state.json sketch — additive fields (§20)",
}

META_READING_HINTS: dict[str, str] = {
    "INTRO-0": "Where we are today and the four structural shifts.",
    "INTRO-1": "Scope, H1/H2/H3, and when a goal is truly done.",
    "INTRO-2": "Generator workflows built from transistors—the fourth structural shift.",
    "MASTER": "One-page summary per plane before detailed specs.",
    "SEC-13": "End-to-end pursuit control flow.",
    "SEC-14": "Migration table from v2.13 to the target.",
    "SEC-15": "Release train v2.14 through v2.28.",
    "SEC-17": "Decisions still awaiting an ADR (including resolved transistor decisions).",
    "SEC-18": "Authoritative A–Z transistor and generator workflow model.",
    "APP-A": "Job taxonomy for template-pack authors.",
    "APP-B": "Additive state.json field sketch.",
}

META_GROUP_INTROS: dict[str, str] = {
    "INTRO-0": "Opens the book: where the harness is today, where it is going, and the four structural shifts (pursuit loop, parallel product and self-improvement, template-pack companies, transistor workflows).",
    "INTRO-1": "Defines 100% automation scope, the H1/H2/H3 contract, and when a goal is truly achieved—policy boundaries every plane assumes.",
    "INTRO-2": "Introduces transistors and generator workflows: compose executable DAGs before inventing long prose implement chains.",
    "MASTER": "The ten-plane map (A–J): one chapter per plane summarizing its role before you dive into detailed capabilities.",
    "SEC-13": "The target end-to-end pursuit diagram—how H1, loop, platform slots, goal_verify, H3, and H2 interleave.",
    "SEC-14": "A migration table from v2.13 behavior to north-star behavior with primary bridge references.",
    "SEC-15": "Additive releases v2.14 through v2.28—read in order; each release unlocks the next layer of autonomy.",
    "SEC-17": "Explicit open and resolved decisions—self-gate rigor, H3 granularity, platform K ratio, budgets, pack authority, multi-goal, transistor model.",
    "SEC-18": "Complete A–Z reference for transistor manifests, workflow DAGs, composition, execution, and v2.24–v2.28 releases.",
    "APP-A": "The full human job taxonomy for pack authors: discover through improve—every leaf should map to pipeline + verify.",
    "APP-B": "Additive state.json field sketch for implementers reading Plane H specs.",
}

META_CHAPTER_GROUPS = frozenset(META_GROUP_ORDER)

GROUP_CATALOG: dict[str, dict[str, str]] = {
    e["id"]: {"title": e["title"], "branch": e.get("branch", ""), "section": e.get("source_section", "")}
    for e in EXPAND_NODES
}

PLANE_INTROS: dict[str, str] = {
    "A": (
        "Plane A is the pursuit and control layer. It replaces burst-and-wait automation with "
        "goal-directed loops: define the goal, run preflight, execute one step, verify, and stop only "
        "for human touchpoints, budgets, or completion."
    ),
    "B": (
        "Plane B decides how each turn is executed—deterministic scripts first (S0), economy workers for "
        "mechanical work (S1), templated artifacts (S2), architecture judgment (S3), and governance "
        "escalation (S4)—with a thin genius-tier conductor."
    ),
    "C": (
        "Plane C is product execution: pipelines, phases, task cards, program parallelism, and delivery "
        "of features and applications from design through tests."
    ),
    "D": (
        "Plane D is how the system improves itself while it works—promotion queue, interleaved scheduling so "
        "delivery and self-improvement both advance, and maturing reuse from one-off reasoning to template-pack fragments."
    ),
    "E": (
        "Plane E is knowledge and composition: one catalog to discover capabilities, mandatory compose-before-invent, "
        "facts, decisions, context layers, and staleness when designs change."
    ),
    "F": (
        "Plane F defines organization through template-packs—company schema, roles, pipelines, and example "
        "packs for game studio and data platform scenarios."
    ),
    "G": (
        "Plane G is verification and quality: evidence gates, goal-level verification, conformance, automated "
        "review triggers, mistake-class controls, and rollback."
    ),
    "H": (
        "Plane H persists state—journal and machine state dual-write, artifact graphs, evidence logs, "
        "worker audit trails, and snapshots."
    ),
    "I": (
        "Plane I integrates runtime environments: Cursor IDE, local SDK daemon, headless CI, external tools, "
        "and operator notifications."
    ),
    "J": (
        "Plane J governs operators—model policy, automation waivers, strict HITL mode, audit, export contracts, "
        "and release queue evolution."
    ),
    "meta": (
        "The meta sections are the book's front matter and appendices: executive summary and north star, "
        "the ten-plane map, end-to-end pursuit flow, gap analysis from today's harness to the target, "
        "the v2.14–v2.23 implementation roadmap, open design decisions, the human job taxonomy for "
        "template-pack authors, and the additive state.json sketch."
    ),
}


def ordered_group_ids(branch_id: str, group_ids: list[str]) -> list[str]:
    """Return group ids in book reading order for a branch."""
    if branch_id == "meta":
        order = {g: i for i, g in enumerate(META_GROUP_ORDER)}
        return sorted(group_ids, key=lambda g: order.get(g, 999))
    return sorted(group_ids, key=lambda g: (g[0], g))


def capability_group_id(item_id: str) -> str:
    """Map leaf id to book group (A1, A2, SEC-15, INTRO-1, …)."""
    if item_id.startswith("SEC-15-"):
        return "SEC-15"
    if item_id.startswith("SEC-17-"):
        return "SEC-17"
    m = re.match(r"^([A-J]\d+)", item_id)
    if m:
        return m.group(1)
    if item_id.startswith("INTRO-"):
        return item_id.rsplit(".", 1)[0] if "." in item_id else item_id
    if item_id.startswith("MASTER-"):
        return "MASTER"
    if item_id.startswith("APP-A-"):
        return "APP-A"
    if re.match(r"^[A-J]\d*$", item_id):
        return item_id
    if re.match(r"^H\d", item_id):
        return "H"
    if re.match(r"^J\d", item_id):
        return "J"
    if item_id.startswith("SEC-"):
        return item_id.split("-")[0] + "-" + item_id.split("-")[1] if item_id.count("-") >= 1 else item_id
    return item_id.split(".")[0] if "." in item_id else item_id


def group_nodes(nodes: list) -> dict[str, list]:
    """Group ParsedNode list by capability_group_id, preserving leaf order."""
    by_group: dict[str, list] = defaultdict(list)
    for n in nodes:
        by_group[capability_group_id(n.id)].append(n)
    for gid in by_group:
        by_group[gid].sort(key=lambda x: x.id)
    return dict(by_group)


def group_title(group_id: str) -> str:
    if group_id in META_GROUP_TITLES:
        return META_GROUP_TITLES[group_id]
    if group_id in GROUP_CATALOG:
        return GROUP_CATALOG[group_id]["title"]
    if group_id in LEAVES:
        return LEAVES[group_id]
    return group_id.replace("-", " ").replace("_", " ")


def is_sequential_group(group_id: str) -> bool:
    return group_id in SEQUENTIAL_GROUPS


def plane_intro(branch_id: str) -> str:
    return PLANE_INTROS.get(branch_id, "")
