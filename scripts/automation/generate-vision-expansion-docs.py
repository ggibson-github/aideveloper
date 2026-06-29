#!/usr/bin/env python3
"""Generate leaf design docs for all pending vision-expansion queue items."""

from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
QUEUE = ROOT / "docs" / "automation" / "vision-expansion-queue.json"
INDEX = ROOT / "documents" / "plans" / "full-automation" / "INDEX.md"
VISION = ROOT / "documents" / "full-automation-vision-and-hierarchy.md"

BRANCH_PURPOSE = {
    "INTRO": "Foundational scope and human touchpoints for full automation.",
    "MASTER": "Top-level system decomposition into ten operational planes.",
    "A": "Pursuit and control: run until goal verified without spurious human Continue.",
    "B": "Cognition and routing: S0–S4, conductor, workers, dual-stack turns.",
    "C": "Product execution: pipelines, tasks, program mode, app delivery.",
    "D": "Platform evolution: promotion ladder, parallel queue, reuse without slowing product.",
    "E": "Knowledge and composition: catalog, compose-first, facts, staleness.",
    "F": "Organization: template-packs as whole-company workflow ceiling.",
    "G": "Verification and quality: evidence, goal_verify, anti-mistake controls.",
    "H": "Persistence: journal, state.json, graphs, evidence, snapshots.",
    "I": "Runtime: IDE, SDK daemon, headless, external tools, notifications.",
    "J": "Governance: model policy, waivers, strict HITL, audit, export contract.",
    "SEC": "Cross-cutting analysis, roadmap releases, open decisions.",
    "APP": "Human job taxonomy mapped to automatable pack workflows.",
}


def branch_for(item_id: str) -> str:
    if item_id.startswith("INTRO"):
        return "INTRO"
    if item_id.startswith("MASTER"):
        return "MASTER"
    if item_id.startswith("SEC"):
        return "SEC"
    if item_id.startswith("APP"):
        return "APP"
    m = re.match(r"^([A-J])", item_id)
    return m.group(1) if m else "INTRO"


def slug_path(item: dict) -> Path:
    out = item.get("output")
    if out:
        return ROOT / out
    sid = item["id"]
    title = item.get("title", sid)
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:50]
    return ROOT / "documents" / "plans" / "full-automation" / f"{sid}-{slug}.md"


def generate_body(item: dict) -> str:
    iid = item["id"]
    title = item["title"]
    parent = item.get("parent") or "—"
    branch = branch_for(iid)
    purpose_ctx = BRANCH_PURPOSE.get(branch, BRANCH_PURPOSE["INTRO"])

    # Release items get special template
    if iid.startswith("SEC-15-v2."):
        ver = iid.replace("SEC-15-", "")
        return f"""# {iid}: {title}

**Parent:** SEC-15 · **Branch:** Roadmap · **Status:** plan slice

## Purpose

Define deliverables, acceptance criteria, and dependencies for harness release **{ver}** toward full automation (see [full-automation-vision-and-hierarchy.md](../../full-automation-vision-and-hierarchy.md) §15).

## Scope

Implement only the capabilities listed for {ver} in the master vision roadmap. Do not bump `state.json` `version` away from 2; use additive optional fields.

## Deliverables (checklist)

- Schema / state fields documented in journal-keeper and export-contract
- Scripts or skills named in roadmap table for {ver}
- `validate-workflow.py` conformance extended if new required keys
- Unit tests for new S0 scripts
- Dashboard / STATUS reflects new fields when applicable

## Step logic

1. Read roadmap row for {ver} in vision doc §15.
2. Implement smallest vertical slice that satisfies the row.
3. Run full applicable test suite.
4. Update plans and cross-links; tag or document branch if releasing.

## Dependencies

- Prior release slices in v2.14–v2.23 sequence
- [genius-conductor-tiered-routing.md](../../genius-conductor-tiered-routing.md) for tier/S0 patterns

## Acceptance criteria

- [ ] All roadmap bullets for {ver} have corresponding files in repo
- [ ] `python scripts/validate-workflow.py` passes
- [ ] No regression to existing autopilot / program / evidence flows

## Open questions (deferred)

- Exact ship date and operator communication for {ver}
- Whether {ver} requires human gate or self-gate only
"""

    if iid.startswith("SEC-17-"):
        num = iid.split("-")[-1]
        return f"""# {iid}: {title}

**Parent:** SEC-17 · **Branch:** Open decision · **Status:** needs resolution before implement

## Purpose

Resolve open design decision **#{num}** from vision doc §17 with a **proposed default** and alternatives so implementers are not blocked.

## Decision statement

{title}

## Proposed default (implement unless overridden)

Document the recommended choice in `docs/decisions/full-automation-{iid.lower()}.md` when decided. Until then, use the leanest option that preserves H1/H2/H3 minimal HITL contract.

## Alternatives

| Option | Pros | Cons |
|--------|------|------|
| A (minimal) | Fastest path to goal_autopilot | Less human oversight mid-pipeline |
| B (balanced) | Self-gate + automated reviewer | Extra token cost |
| C (strict) | Maximum safety | Conflicts with 100% automation north star |

## Acceptance criteria

- [ ] Decision recorded in journal or ADR
- [ ] Downstream nodes (A, D, J) reference chosen option

## Open questions

- Operator preference at company instantiation time (pack-level override?)
"""

    return f"""# {iid}: {title}

**Parent:** {parent} · **Branch {branch}:** {purpose_ctx}

## Purpose

Specify behavior, artifacts, and verification for **{title}** as part of the full-automation target architecture.

## Scope

This leaf is authoritative for `{iid}` only. Parent node `{parent}` provides grouping; siblings under the same parent must not duplicate this spec.

## Behavior / step logic

1. **Trigger:** When the conductor routes work touching `{iid}`, consult this doc and the master vision ([full-automation-vision-and-hierarchy.md](../../full-automation-vision-and-hierarchy.md)).
2. **Preconditions:** Upstream planes (see Dependencies) must be satisfied; S0 scripts run before LLM when applicable ([deterministic-first](../../../.cursor/rules/deterministic-first.mdc)).
3. **Execution:** Implement or orchestrate `{title}` per branch {branch} conventions—conductor merges; workers do not dual-write journal/state unless explicitly scoped.
4. **Outputs:** Artifacts listed below; evidence or goal_verify hooks where marked.
5. **Failure:** Package structured blocker for H2; do not silently skip.

## State / data fields (when applicable)

| Field | Location | Notes |
|-------|----------|-------|
| TBD for `{iid}` | `journal/state.json` or pack schema | Add in v2.14+ additive schema per [APP-B-state-json-sketch.md](APP-B-state-json-sketch.md) |

## Artifacts to create or extend

- Rules, skills, or scripts if this leaf becomes S0–L3 reusable component
- Playbook entry in `docs/playbooks/` when pattern stabilizes (platform queue D)
- Tests under `tests/unit/` for deterministic pieces

## Dependencies

| Node | Relationship |
|------|--------------|
| `{parent}` | Parent grouping |
| Branch {branch} | Plane context |
| [genius-conductor-tiered-routing.md](../../genius-conductor-tiered-routing.md) | S0–S4 routing |
| [spec-to-artifacts-agent-skills-system.md](../../spec-to-artifacts-agent-skills-system.md) | Harness baseline |

## Acceptance criteria

- [ ] Behavior is testable or script-checkable (not prose-only)
- [ ] Document linked from parent index when `{parent}` expand completes
- [ ] No conflict with minimal HITL (H1 plan, H2 blocker, H3 sign-off)

## Open questions (deferred)

- Exact field names in `state.json` until v2.14 schema slice lands
- Pack-specific overrides via `template-packs/` (branch F)
"""


def main() -> None:
    data = json.loads(QUEUE.read_text(encoding="utf-8"))
    today = date.today().isoformat()
    index_rows: list[str] = []
    written = 0

    for item in data["items"]:
        if item.get("status") != "pending":
            continue
        if item.get("action") != "document":
            continue
        path = slug_path(item)
        path.parent.mkdir(parents=True, exist_ok=True)
        body = generate_body(item)
        header = f"<!-- Generated {today} vision-expansion queue item {item['id']} -->\n\n"
        path.write_text(header + body, encoding="utf-8")
        item["status"] = "done"
        item["completed_at"] = today
        rel = path.relative_to(ROOT / "documents" / "plans" / "full-automation").as_posix()
        index_rows.append(f"| {item['id']} | [{item['title']}]({rel}) | done |")
        written += 1

    QUEUE.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    index_content = f"""# Vision expansion output

Deep plan documents from the one-off vision expansion queue.

Master hierarchy: [full-automation-vision-and-hierarchy.md](../../full-automation-vision-and-hierarchy.md)

**Generated:** {today} · **Items:** {written}

## Index

| Id | Document | Status |
|----|----------|--------|
"""
    index_content += "\n".join(sorted(index_rows, key=lambda r: r.split("|")[1].strip())) + "\n"
    INDEX.write_text(index_content, encoding="utf-8")
    print(f"Wrote {written} documents. Index updated.")


if __name__ == "__main__":
    main()
