<!-- Complete pass 3 2026-06-28 J5 -->

# J5: export contract

**Parent:** — · **Branch J** · **Vision §12** · **Release:** v2.26

## Reader narrative
<!-- prose-source: agent plane-j 2026-06-28 -->

`docs/operator/export-contract.md` defines what pursuit state, evidence bundles, and dashboard artifacts may leave the repo boundary—fields redacted, formats required, and approval needed for external sharing. Export scripts follow the contract; ad-hoc copy/paste of state.json is discouraged.

Pack authors extend export profiles per company template. Export for H3 sign-off packages may include goal_verify evidence rollup ([C3.4](C3.4-task-to-goal-rollup-percent-goal-verify.md)). Contract violations surface H2 before data leaves controlled storage.

## Purpose

J5 defines export contract for the agent-driven expert system. Governance — policy, waivers, audit, export contract.
## Scope

- Owns `J5` only; siblings under `—` must not duplicate this spec.
- Aligns with minimal HITL: H1 plan, H2 blocker, H3 sign-off ([INTRO-1.2](INTRO-1.2-human-touchpoint-contract-h1-h2-h3.md)).
- Conflicts resolve in favor of [Vision §12 — Branch J — Governance & operator plane](../../full-automation-vision-and-hierarchy.md#12-branch-j-governance-operator-plane).

```
├── J5. export-contract for external orchestrators
```
## Behavior / step logic
<!-- timeline-source: agent cursor-agent 2026-06-28 -->

1. Before pursuit state, evidence bundles, or dashboard artifacts cross the repo boundary, export scripts resolve the active profile from `docs/operator/export-contract.md` and the company template-pack—redacting fields, enforcing required formats, and checking H3 approval when external sharing demands it.
2. H3 sign-off packages may aggregate goal_verify evidence per [C3.4](C3.4-task-to-goal-rollup-percent-goal-verify.md); the conductor includes only contract-approved paths and never ad-hoc copy/paste of `state.json`.
3. Pack authors extend export profiles per template-pack; pursuit inherits the profile for the active company goal so external orchestrators receive consistent, policy-bound bundles.
4. Pre-export validation runs as S0 where scripted ([B1.1](B1.1-s0-deterministic-mandatory-first.md)); contract violations surface H2 before data leaves controlled storage.
5. If the export profile is missing, ambiguous, or would leak blocked fields, pursuit halts at H2 until operators reconcile the contract or explicitly resolve the gap at H3.

## JSON example

```json
{
  "node": "J5",
  "description": "export contract",
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
- Edge case `J5` variant 3: verify state dual-write before continuing pursuit.
- Edge case `J5` variant 4: verify state dual-write before continuing pursuit.
- Pass 3: add regression test or evidence path specific to `J5`.
- Pass 3: cross-link related nodes in same branch index.

## Failure modes

- **Silent stop:** Agent ends turn without updating queue â†’ mitigated by /loop + check-hierarchy-queue.py EMPTY gate.
- **False complete:** Item marked done without artifact â†’ audit-hierarchy-depth.py re-enqueues deepen pass.
- **Scope bleed:** Worker edits journal/state during planning-only expansion â†’ forbidden in vision-expansion-prompt.
- **Stale design:** Upstream vision Â§ changes â†’ reconcile-stale adds deepen items for affected ids.

## Concrete implementation

1. Map `J5` to v2.14â€“v2.23 release row in SEC-15-index.md.
2. Create or extend S0 script if behavior is file-derived.
3. Add unit test under tests/unit/test_j5.py when script exists.
4. Validate `J5` against SEC-15 release checklist and parent index links.
5. Document `J5` in parent index with verify command and release tag.
6. Add checklist row in SEC-15 release doc for `J5`.

## Verification

| Check | Command |
|-------|---------|
| Completeness | `python scripts/automation/audit-hierarchy-depth.py --strict --ids J5` |
| Conformance | `python scripts/validate-workflow.py` |
| Task evidence | `python scripts/verify-router.py` when implement task exists |

## Dependencies

| Link | Why |
|------|-----|
| [full-automation-vision-and-hierarchy.md](../../full-automation-vision-and-hierarchy.md) §12 | Master hierarchy |
| [—-index](—-index.md) | Parent grouping |
| [genius-conductor-tiered-routing.md](../../genius-conductor-tiered-routing.md) | S0–S4 routing |

## Acceptance criteria

- [ ] `python scripts/automation/audit-hierarchy-depth.py --strict --ids J5` passes
- [ ] Named script, skill, or test path exists or is listed in SEC-15 release row
- [ ] Linked from [—-index](—-index.md)
- [ ] `python scripts/validate-workflow.py` passes after implement

## Cross-links

- [hierarchy-expander SKILL](../../../.cursor/skills/hierarchy-expander/SKILL.md)
