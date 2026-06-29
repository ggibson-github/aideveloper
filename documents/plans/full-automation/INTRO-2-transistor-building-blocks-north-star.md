<!-- Complete pass 1 2026-06-28 INTRO-2 -->

# INTRO-2: Transistor building blocks north star

**Parent:** [INTRO-index](INTRO-index.md) · **Branch INTRO** · **Vision §19** · **Release:** v2.24

## Reader narrative
<!-- prose-source: agent transistor-expansion 2026-06-28 -->

The fourth structural shift after pursuit loops, dual-stack platform evolution, and template-pack companies: **generator workflows** built from **transistors**—registered composable blocks with typed inputs, outputs, executors, and per-block verify—instead of long prose-only skill chains.

Agents compose before they invent: search the transistor registry, stitch a DAG, execute one node per turn with evidence, promote misses to the platform queue. Read [SEC-18](SEC-18-transistor-model-a-to-z.md) for the complete A–Z reference.

See [Vision §19 — Transistor & generator workflow model](../../full-automation-vision-and-hierarchy.md#transistor--generator-workflow-model) and [SEC-18-transistor-model-a-to-z](SEC-18-transistor-model-a-to-z.md).

## Purpose

INTRO-2 defines transistor building blocks north star for the agent-driven expert system. Transistor & generator workflow model (§19).
## Scope

- Owns `INTRO-2` only; siblings under `INTRO` must not duplicate this spec.
- Aligns with minimal HITL: H1 plan, H2 blocker, H3 sign-off ([INTRO-1.2](INTRO-1.2-human-touchpoint-contract-h1-h2-h3.md)).
- Conflicts resolve in favor of [Vision §11 — Branch I — Runtime & integration plane](../../full-automation-vision-and-hierarchy.md#11-branch-i-runtime-integration-plane).

```
INTRO-2 Transistor building blocks north star
```
## Behavior / step logic
<!-- timeline-source: agent transistor-expansion 2026-06-28 -->

1. After H1 approves a goal, pursuit must produce or bind a generator workflow DAG before direct implement improvisation when goal type is app, feature, milestone, or pack-defined deliverable.
2. Each workflow node references a catalog transistor or records an L0 miss plus promotion_queue enqueue per E7.4.
3. Product turns execute the current workflow node; platform turns mint new transistors from repeated L0 patterns per D4.7.
4. Goal completion requires workflow completion rollup (C6.5) plus goal_verify—not merely task cards closed in chat order.
5. Skills and playbooks remain orchestration documentation; transistors are the executable contract the conductor and S0 tools enforce.

```mermaid
flowchart TD
  compose[Compose workflow] --> validate[validate-workflow-dag S0]
  validate -->|pass| exec[Execute one node]
  exec --> nodeVerify[Transistor verify]
  nodeVerify -->|pass| next[Advance active_workflow]
  nodeVerify -->|fail| h2[H2 or retry gate]
  next --> goalVerify[goal_verify rollup]
```

## JSON example

```json
{
  "node": "INTRO-2",
  "description": "transistor building blocks north star",
  "state": { "ref": "APP-B-state-json-sketch.md", "active_workflow": "H1.7" },
  "implemented_in_release": "v2.24+"
}
```

## Repo artifacts (this branch)

- `docs/platform/transistors/`
- `docs/platform/schemas/transistor.v1.json`
- `docs/platform/schemas/workflow-dag.v1.json`
- `docs/workflows/`
- `scripts/automation/list-transistors.py`
- `scripts/automation/validate-workflow-dag.py`

## Edge cases

- Operator closes laptop mid-loop — state.json must resume from last good dual-write including active_workflow.
- Transistor version bump mid-pursuit — E5.4 marks workflow stale; re-validate before next node.
- L0 waiver node without promotion progress — D3.3 priority boost then H2 if threshold exceeded.
- Pack overlay id collision — F5.4 semver fork per D5.3, not silent overwrite.
- Parallel branch join missing typed input — validate-workflow-dag fails at compose time.

## Failure modes

- **Fuzzy chain:** Implement without workflow_node_id when C6.1 applies → G5.8 blocks at preflight.
- **False complete:** Node marked done without transistor verify evidence → G2.5 goal_verify fails closed.
- **Stale workflow:** active_workflow.validation_hash mismatch → E5.4 reconcile before advance.
- **Duplicate transistor:** G5.6 list-transistors --check-duplicates rejects promotion.
- **Scope bleed:** Worker runs transistors outside bound node → C6.3 conformance failure.

## Concrete implementation

1. Map `INTRO-2` to release row in [SEC-15-index](SEC-15-index.md) (v2.24).
2. Implement behavior per [SEC-18](SEC-18-transistor-model-a-to-z.md) acceptance checklist.
3. Add or extend S0 script when behavior is file-derived.
4. Add unit test under `tests/unit/` when script exists.
5. Link from [INTRO-index](INTRO-index.md).
6. Run `python scripts/validate-workflow.py` after implement.

## Verification

| Check | Command |
|-------|---------|
| Completeness | `python scripts/automation/audit-hierarchy-depth.py --strict --ids INTRO-2` |
| Conformance | `python scripts/validate-workflow.py` |
| DAG validity | `python scripts/automation/validate-workflow-dag.py` when workflow exists |
| Task evidence | `python scripts/verify-router.py` when implement task exists |

## Dependencies

| Link | Why |
|------|-----|
| [SEC-18-transistor-model-a-to-z](SEC-18-transistor-model-a-to-z.md) | A–Z authority |
| [full-automation-vision-and-hierarchy.md](../../full-automation-vision-and-hierarchy.md) §19 | Master hierarchy |
| [INTRO-index](INTRO-index.md) | Parent grouping |
| [genius-conductor-tiered-routing.md](../../genius-conductor-tiered-routing.md) | S0–S4 routing |

## Acceptance criteria

- [ ] `python scripts/automation/audit-hierarchy-depth.py --strict --ids INTRO-2` passes
- [ ] Named script, skill, or test path exists or is listed in SEC-15 release row
- [ ] Linked from [INTRO-index](INTRO-index.md)
- [ ] Aligned with SEC-18 transistor model
- [ ] `python scripts/validate-workflow.py` passes after implement

## Cross-links

- [hierarchy-expander SKILL](../../../.cursor/skills/hierarchy-expander/SKILL.md)
- [INTRO-2-transistor-building-blocks-north-star](INTRO-2-transistor-building-blocks-north-star.md)
