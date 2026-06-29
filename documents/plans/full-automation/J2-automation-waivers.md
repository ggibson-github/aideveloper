<!-- Complete pass 3 2026-06-28 J2 -->

# J2: automation waivers

**Parent:** — · **Branch J** · **Vision §12** · **Release:** v2.16

## Reader narrative
<!-- prose-source: agent plane-j 2026-06-28 -->

`docs/decisions/automation-waivers.md` records time-bounded exceptions to default automation rules—skipped verify suites, deferred gates, manual push approvals—with operator, rationale, expiry, and affected goal ids. Waivers are not silent overrides in chat.

Expired waivers revert to strict behavior; pursuit must re-check preflight before continuing. Self-gate middle approvals may be waivable when automatable evidence exists ([A5.2](A5.2-continue-not-approval-self-gate-h1-h3-only.md)); H3 subjective sign-off is never permanently waived without explicit policy. Audit links waivers in [J4](J4-audit.md).

## Purpose

J2 defines automation waivers for the agent-driven expert system. Governance — policy, waivers, audit, export contract.
## Scope

- Owns `J2` only; siblings under `—` must not duplicate this spec.
- Aligns with minimal HITL: H1 plan, H2 blocker, H3 sign-off ([INTRO-1.2](INTRO-1.2-human-touchpoint-contract-h1-h2-h3.md)).
- Conflicts resolve in favor of [Vision §12 — Branch J — Governance & operator plane](../../full-automation-vision-and-hierarchy.md#12-branch-j-governance-operator-plane).

```
├── J2. automation-waivers.md — template self-build only
```
## Behavior / step logic
<!-- timeline-source: agent cli-composer-2.5 2026-06-28 -->

1. During active product pursuit, [D2](D2-index.md) enqueue signals—repeated manual commands, verify gaps, worker-flagged repetition—land in the platform queue without blocking the current goal's next_action.
2. [D3](D3-index.md) scheduling drains one platform turn per K product turns (or on idle when product waits at H2) so self-improvement runs alongside delivery rather than starving the active goal.
3. Platform work follows the promotion ladder from [D1](D1-index.md): ephemeral fixes become playbooks, S0 scripts, skills, and template-pack fragments via [D4](D4-index.md) extractors.
4. Completed platform items wire into catalog, task cards, and staleness nodes per [D5](D5-index.md) and [D6](D6-index.md) so the next pursuit turn can compose reuse instead of re-improvising.
5. If platform drain would violate product budget caps from [A1.4](A1.4-deadline-budget-steps-tokens-wall-clock.md) or displace a blocked H2 product goal, scheduling defers platform turns and records the deferral in state rather than silently skipping self-improvement forever.

## JSON example

```json
{
  "node": "J2",
  "description": "automation waivers",
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
- Edge case `J2` variant 3: verify state dual-write before continuing pursuit.
- Edge case `J2` variant 4: verify state dual-write before continuing pursuit.
- Pass 3: add regression test or evidence path specific to `J2`.
- Pass 3: cross-link related nodes in same branch index.

## Failure modes

- **Silent stop:** Agent ends turn without updating queue â†’ mitigated by /loop + check-hierarchy-queue.py EMPTY gate.
- **False complete:** Item marked done without artifact â†’ audit-hierarchy-depth.py re-enqueues deepen pass.
- **Scope bleed:** Worker edits journal/state during planning-only expansion â†’ forbidden in vision-expansion-prompt.
- **Stale design:** Upstream vision Â§ changes â†’ reconcile-stale adds deepen items for affected ids.

## Concrete implementation

1. Map `J2` to v2.14â€“v2.23 release row in SEC-15-index.md.
2. Create or extend S0 script if behavior is file-derived.
3. Add unit test under tests/unit/test_j2.py when script exists.
4. Validate `J2` against SEC-15 release checklist and parent index links.
5. Document `J2` in parent index with verify command and release tag.
6. Add checklist row in SEC-15 release doc for `J2`.

## Verification

| Check | Command |
|-------|---------|
| Completeness | `python scripts/automation/audit-hierarchy-depth.py --strict --ids J2` |
| Conformance | `python scripts/validate-workflow.py` |
| Task evidence | `python scripts/verify-router.py` when implement task exists |

## Dependencies

| Link | Why |
|------|-----|
| [full-automation-vision-and-hierarchy.md](../../full-automation-vision-and-hierarchy.md) §12 | Master hierarchy |
| [—-index](—-index.md) | Parent grouping |
| [genius-conductor-tiered-routing.md](../../genius-conductor-tiered-routing.md) | S0–S4 routing |

## Acceptance criteria

- [ ] `python scripts/automation/audit-hierarchy-depth.py --strict --ids J2` passes
- [ ] Named script, skill, or test path exists or is listed in SEC-15 release row
- [ ] Linked from [—-index](—-index.md)
- [ ] `python scripts/validate-workflow.py` passes after implement

## Cross-links

- [hierarchy-expander SKILL](../../../.cursor/skills/hierarchy-expander/SKILL.md)
