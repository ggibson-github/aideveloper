<!-- Complete pass 3 2026-06-28 J4 -->

# J4: audit

**Parent:** — · **Branch J** · **Vision §12** · **Release:** v2.23

## Reader narrative
<!-- prose-source: agent plane-j 2026-06-28 -->

Audit trail governance spans worker-runs.jsonl ([H5](H5-worker-runs.md)), evidence/ immutability ([H4](H4-evidence.md)), journal Resolved Q&A, waiver registry ([J2](J2-automation-waivers.md)), and export-contract snapshots for external review.

Operators query audit paths to reconstruct who spawned which worker, what verify ran, and which gates cleared. Tamper-evident logs support post-incident review; conductors must not truncate audit history without documented retention policy. CI and headless runs append to the same trails ([I3](I3-index.md)).

## Purpose

J4 defines audit for the agent-driven expert system. Governance — policy, waivers, audit, export contract.
## Scope

- Owns `J4` only; siblings under `—` must not duplicate this spec.
- Aligns with minimal HITL: H1 plan, H2 blocker, H3 sign-off ([INTRO-1.2](INTRO-1.2-human-touchpoint-contract-h1-h2-h3.md)).
- Conflicts resolve in favor of [Vision §12 — Branch J — Governance & operator plane](../../full-automation-vision-and-hierarchy.md#12-branch-j-governance-operator-plane).

```
├── J4. audit: who waived what, when
```
## Behavior / step logic
<!-- timeline-source: agent cli-composer-2.5 2026-06-28 -->

1. When pursuit scope is complete against machine-checkable [success criteria](A1.2-success-criteria-machine-checkable.md), the conductor sets `goal.state` to `verifying` and invokes `goal_verify_command` from state.json before surfacing H3 sign-off.
2. The meta-test aggregates success_criteria predicates, evidence logs, and conformance scripts into one exit code—stricter than any single task-level verify pass.
3. Preflight and check-pipeline-blocked refuse `H3_pending` while goal_verify fails, even when individual implement tasks report `last_verify: passed`.
4. On exit 0, the conductor dual-writes the result to journal and state.json and requests H3 operator sign-off per the H1/H2/H3 contract in [INTRO-1.2](INTRO-1.2-human-touchpoint-contract-h1-h2-h3.md).
5. If goal_verify fails or evidence is incomplete, pursuit halts at H2 with structured notes; the system must not mark the goal achieved or request H3 until the meta-test passes.

## JSON example

```json
{
  "node": "J4",
  "description": "audit",
  "state": { "ref": "APP-B-state-json-sketch.md" },
  "implemented_in_release": "v2.14+"
}
```


## Repo artifacts (this branch)

- `docs/operator/model-policy.json`
- `docs/decisions/automation-waivers.md`
- `docs/automation/release-queue.json`

## Edge cases

- Operator closes laptop mid-loop â€” state.json must resume from last good dual-write.
- Concurrent manual edit to queue JSON â€” conductor reloads queue each wake; last writer wins with journal note.
- Edge case `J4` variant 3: verify state dual-write before continuing pursuit.
- Edge case `J4` variant 4: verify state dual-write before continuing pursuit.
- Pass 3: add regression test or evidence path specific to `J4`.
- Pass 3: cross-link related nodes in same branch index.

## Failure modes

- **Silent stop:** Agent ends turn without updating queue â†’ mitigated by /loop + check-hierarchy-queue.py EMPTY gate.
- **False complete:** Item marked done without artifact â†’ audit-hierarchy-depth.py re-enqueues deepen pass.
- **Scope bleed:** Worker edits journal/state during planning-only expansion â†’ forbidden in vision-expansion-prompt.
- **Stale design:** Upstream vision Â§ changes â†’ reconcile-stale adds deepen items for affected ids.

## Concrete implementation

1. Map `J4` to v2.14â€“v2.23 release row in SEC-15-index.md.
2. Create or extend S0 script if behavior is file-derived.
3. Add unit test under tests/unit/test_j4.py when script exists.
4. Validate `J4` against SEC-15 release checklist and parent index links.
5. Document `J4` in parent index with verify command and release tag.
6. Add checklist row in SEC-15 release doc for `J4`.

## Verification

| Check | Command |
|-------|---------|
| Completeness | `python scripts/automation/audit-hierarchy-depth.py --strict --ids J4` |
| Conformance | `python scripts/validate-workflow.py` |
| Task evidence | `python scripts/verify-router.py` when implement task exists |

## Dependencies

| Link | Why |
|------|-----|
| [full-automation-vision-and-hierarchy.md](../../full-automation-vision-and-hierarchy.md) §12 | Master hierarchy |
| [—-index](—-index.md) | Parent grouping |
| [genius-conductor-tiered-routing.md](../../genius-conductor-tiered-routing.md) | S0–S4 routing |

## Acceptance criteria

- [ ] `python scripts/automation/audit-hierarchy-depth.py --strict --ids J4` passes
- [ ] Named script, skill, or test path exists or is listed in SEC-15 release row
- [ ] Linked from [—-index](—-index.md)
- [ ] `python scripts/validate-workflow.py` passes after implement

## Cross-links

- [hierarchy-expander SKILL](../../../.cursor/skills/hierarchy-expander/SKILL.md)
