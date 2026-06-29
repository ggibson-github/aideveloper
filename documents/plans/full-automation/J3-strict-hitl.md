<!-- Complete pass 3 2026-06-28 J3 -->

# J3: strict hitl

**Parent:** — · **Branch J** · **Vision §12** · **Release:** v2.15

## Reader narrative
<!-- prose-source: agent plane-j 2026-06-28 -->

`strict_hitl` mode in state.json hitl block forces explicit human clearance for gates that default self-gate would auto-pass with evidence. Enable for regulated environments, external-audit programs, or operator preference during early pack rollout.

When strict_hitl is true, continue and autopilot stop at every pending H1/H2/H3 until journal records explicit approval phrases—observation alone does not unblock ([A6.3](A6.3-operator-observe-without-unblocking-loop.md)). Pack defaults may set strict_hitl per role ([H1.5](H1.5-state-hitl-block.md)).

## Purpose

J3 defines strict hitl for the agent-driven expert system. Governance — policy, waivers, audit, export contract.
## Scope

- Owns `J3` only; siblings under `—` must not duplicate this spec.
- Aligns with minimal HITL: H1 plan, H2 blocker, H3 sign-off ([INTRO-1.2](INTRO-1.2-human-touchpoint-contract-h1-h2-h3.md)).
- Conflicts resolve in favor of [Vision §12 — Branch J — Governance & operator plane](../../full-automation-vision-and-hierarchy.md#12-branch-j-governance-operator-plane).

```
├── J3. strict_hitl mode flag (optional override of self-gates)
```
## Behavior / step logic
<!-- timeline-source: agent cli-composer-2.5 2026-06-28 -->

1. strict_hitl mode in state.json hitl block forces explicit human clearance for gates that default self-gate would auto-pass with evidence
2. When strict_hitl is true, continue and autopilot stop at every pending H1/H2/H3 until journal records explicit approval phrases—observation alone does not unblock (A6.3)
3. During pursuit, enforce the strict and hitl contract within J3 (Plane J).
4. Run [S0](B1.1-s0-deterministic-mandatory-first.md) scripts before improvising when file-derived behavior exists.
5. Dual-write journal and state.json after the step; attach evidence when verification applies.

## JSON example

```json
{
  "node": "J3",
  "description": "strict hitl",
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
- Edge case `J3` variant 3: verify state dual-write before continuing pursuit.
- Edge case `J3` variant 4: verify state dual-write before continuing pursuit.
- Pass 3: add regression test or evidence path specific to `J3`.
- Pass 3: cross-link related nodes in same branch index.

## Failure modes

- **Silent stop:** Agent ends turn without updating queue â†’ mitigated by /loop + check-hierarchy-queue.py EMPTY gate.
- **False complete:** Item marked done without artifact â†’ audit-hierarchy-depth.py re-enqueues deepen pass.
- **Scope bleed:** Worker edits journal/state during planning-only expansion â†’ forbidden in vision-expansion-prompt.
- **Stale design:** Upstream vision Â§ changes â†’ reconcile-stale adds deepen items for affected ids.

## Concrete implementation

1. Map `J3` to v2.14â€“v2.23 release row in SEC-15-index.md.
2. Create or extend S0 script if behavior is file-derived.
3. Add unit test under tests/unit/test_j3.py when script exists.
4. Validate `J3` against SEC-15 release checklist and parent index links.
5. Document `J3` in parent index with verify command and release tag.
6. Add checklist row in SEC-15 release doc for `J3`.

## Verification

| Check | Command |
|-------|---------|
| Completeness | `python scripts/automation/audit-hierarchy-depth.py --strict --ids J3` |
| Conformance | `python scripts/validate-workflow.py` |
| Task evidence | `python scripts/verify-router.py` when implement task exists |

## Dependencies

| Link | Why |
|------|-----|
| [full-automation-vision-and-hierarchy.md](../../full-automation-vision-and-hierarchy.md) §12 | Master hierarchy |
| [—-index](—-index.md) | Parent grouping |
| [genius-conductor-tiered-routing.md](../../genius-conductor-tiered-routing.md) | S0–S4 routing |

## Acceptance criteria

- [ ] `python scripts/automation/audit-hierarchy-depth.py --strict --ids J3` passes
- [ ] Named script, skill, or test path exists or is listed in SEC-15 release row
- [ ] Linked from [—-index](—-index.md)
- [ ] `python scripts/validate-workflow.py` passes after implement

## Cross-links

- [hierarchy-expander SKILL](../../../.cursor/skills/hierarchy-expander/SKILL.md)
