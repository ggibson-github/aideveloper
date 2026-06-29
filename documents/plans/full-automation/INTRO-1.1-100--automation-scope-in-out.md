<!-- Complete pass 3 2026-06-28 INTRO-1.1-100- -->

# INTRO-1.1-100-: automation scope in out

**Parent:** [INTRO-1-index](INTRO-1-index.md) · **Branch INTRO** · **Vision §11** · **Release:** meta

## Reader narrative
<!-- prose-source: agent meta 2026-06-28 -->

One hundred percent automation does not mean humans disappear—it means humans appear only where policy requires authority, judgment of record, or external access the system cannot obtain. After initial planning is approved, the system owns SDLC execution: implement, test, refactor, integrate, and deploy preparation.

In scope: multi-role company workflows via template-packs, blocker detection with structured escalation, and harness self-improvement through the platform queue. Out of scope: irreversible production actions without verify and rollback, silent waiver of safety gates, and subjective aesthetic approval unless encoded in acceptance tests.

Pack authors and operators use this boundary list when deciding whether a workflow belongs in autonomous pursuit or must remain H2-always. See [INTRO-1.2](INTRO-1.2-human-touchpoint-contract-h1-h2-h3.md) for where humans still interact.

## Purpose

INTRO-1.1 defines 100  automation scope in out for the agent-driven expert system. North star, scope, minimal HITL (H1/H2/H3).
## Scope

- Owns `INTRO-1.1` only; siblings under `INTRO-1` must not duplicate this spec.
- Aligns with minimal HITL: H1 plan, H2 blocker, H3 sign-off ([INTRO-1.2](INTRO-1.2-human-touchpoint-contract-h1-h2-h3.md)).
- Conflicts resolve in favor of [Vision §11 — Branch I — Runtime & integration plane](../../full-automation-vision-and-hierarchy.md#11-branch-i-runtime-integration-plane).

```
INTRO-1.1 100  automation scope in out
```
## Behavior / step logic
<!-- timeline-source: agent cursor-agent 2026-06-28 -->

1. After H1 approves the plan, pursuit enters [A3.2](A3.2-goal-autopilot-until-goal-verify-or-hard-block.md) and the conductor executes SDLC work—implement, test, refactor, integrate, deploy prep—without per-step human nudges except at [INTRO-1.2](INTRO-1.2-human-touchpoint-contract-h1-h2-h3.md) touchpoints.
2. Multi-role company workflows run through template-packs ([F1.1](F1.1-pack-company-yaml-schema.md)); active role, pipeline_id, and allowed_reads bound each turn so autonomous pursuit stays inside pack-defined scope.
3. Blocker detection raises structured H2 pauses with clear unblock criteria when preflight fails, goal_verify fails, or external dependencies are missing—never silent stalls or gate waivers.
4. Harness self-improvement enqueues on the Plane D platform queue and drains on scheduled platform turns when promotion criteria are met, keeping catalog and skills current without manual meta-work each session.
5. Out-of-scope requests—irreversible production without verify/rollback, silent safety-gate waivers, or subjective aesthetic approval—stop at H2 until encoded in machine-checkable success criteria or explicitly resolved at H3.

```mermaid
flowchart TD
  trigger[Trigger condition] --> pre[Preconditions S0]
  pre --> exec[Execute step logic]
  exec --> verify[Verify output]
  verify -->|pass| done[Mark queue item done]
  verify -->|fail| h2[H2 blocker]
```

## JSON example

```json
{
  "node": "INTRO-1.1",
  "description": "100  automation scope in out",
  "state": { "ref": "APP-B-state-json-sketch.md" },
  "implemented_in_release": "v2.14+"
}
```


## Repo artifacts (this branch)



## Edge cases

- Operator closes laptop mid-loop â€” state.json must resume from last good dual-write.
- Concurrent manual edit to queue JSON â€” conductor reloads queue each wake; last writer wins with journal note.
- Edge case `INTRO-1.1` variant 3: verify state dual-write before continuing pursuit.
- Edge case `INTRO-1.1` variant 4: verify state dual-write before continuing pursuit.
- Pass 3: add regression test or evidence path specific to `INTRO-1.1`.
- Pass 3: cross-link related nodes in same branch index.

## Failure modes

- **Silent stop:** Agent ends turn without updating queue â†’ mitigated by /loop + check-hierarchy-queue.py EMPTY gate.
- **False complete:** Item marked done without artifact â†’ audit-hierarchy-depth.py re-enqueues deepen pass.
- **Scope bleed:** Worker edits journal/state during planning-only expansion â†’ forbidden in vision-expansion-prompt.
- **Stale design:** Upstream vision Â§ changes â†’ reconcile-stale adds deepen items for affected ids.

## Concrete implementation

1. Map `INTRO-1.1` to v2.14â€“v2.23 release row in SEC-15-index.md.
2. Create or extend S0 script if behavior is file-derived.
3. Add unit test under tests/unit/test_intro-1_1.py when script exists.
4. Validate `INTRO-1.1` against SEC-15 release checklist and parent index links.
5. Document `INTRO-1.1` in parent index with verify command and release tag.
6. Add checklist row in SEC-15 release doc for `INTRO-1.1`.

## Verification

| Check | Command |
|-------|---------|
| Completeness | `python scripts/automation/audit-hierarchy-depth.py --strict --ids INTRO-1.1` |
| Conformance | `python scripts/validate-workflow.py` |
| Task evidence | `python scripts/verify-router.py` when implement task exists |

## Dependencies

| Link | Why |
|------|-----|
| [full-automation-vision-and-hierarchy.md](../../full-automation-vision-and-hierarchy.md) §11 | Master hierarchy |
| [INTRO-1-index](INTRO-1-index.md) | Parent grouping |
| [genius-conductor-tiered-routing.md](../../genius-conductor-tiered-routing.md) | S0–S4 routing |

## Acceptance criteria

- [ ] `python scripts/automation/audit-hierarchy-depth.py --strict --ids INTRO-1.1` passes
- [ ] Named script, skill, or test path exists or is listed in SEC-15 release row
- [ ] Linked from [INTRO-1-index](INTRO-1-index.md)
- [ ] `python scripts/validate-workflow.py` passes after implement

## Cross-links

- [hierarchy-expander SKILL](../../../.cursor/skills/hierarchy-expander/SKILL.md)
