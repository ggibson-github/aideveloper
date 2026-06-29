<!-- Complete pass 3 2026-06-28 J1 -->

# J1: model policy

**Parent:** — · **Branch J** · **Vision §12** · **Release:** v2.15

## Reader narrative
<!-- prose-source: agent plane-j 2026-06-28 -->

`docs/operator/model-policy.json` defines genius and economy tier Cursor model lists, autopilot defaults, spawn_workers policy, and capability_class routing hints. Operators update tiers as models evolve—fixed model names are not hardcoded in skills or rules.

route-tier.py reads policy plus state to set model_tier each turn ([B3.1](B3.1-genius-orchestration-only-thin-turns.md)). SDK and IDE runtimes share the same policy file ([I2.2](I2.2-runtime-sdk-cursor-api-key-autopilot-model.md)). Policy changes should run validate-workflow.py before unattended autopilot resumes. See [Vision §12](../../full-automation-vision-and-hierarchy.md#12-branch-j-governance-operator-plane).

## Purpose

J1 defines model policy for the agent-driven expert system. Governance — policy, waivers, audit, export contract.
## Scope

- Owns `J1` only; siblings under `—` must not duplicate this spec.
- Aligns with minimal HITL: H1 plan, H2 blocker, H3 sign-off ([INTRO-1.2](INTRO-1.2-human-touchpoint-contract-h1-h2-h3.md)).
- Conflicts resolve in favor of [Vision §12 — Branch J — Governance & operator plane](../../full-automation-vision-and-hierarchy.md#12-branch-j-governance-operator-plane).

```
├── J1. model-policy.json — tiers, autopilot defaults
```
## Behavior / step logic
<!-- timeline-source: agent cursor-agent 2026-06-28 -->

1. On each pursuit wake, the conductor runs `scripts/route-tier.py --apply` (S0) against `docs/operator/model-policy.json` and journal/state.json to set `model_tier`, `spawn_workers`, and `subagent_models` before any skill phase runs.
2. Genius-tier models from policy bind to the conductor orchestration turns under [B3.1](B3.1-genius-orchestration-only-thin-turns.md); economy tiers route to spawned workers per `capability_class`—fixed model names never hardcode in skills or rules.
3. IDE sessions and SDK daemons ([I2.2](I2.2-runtime-sdk-cursor-api-key-autopilot-model.md)) load the same policy file so autopilot routing stays consistent across runtimes.
4. When operators edit tier lists or spawn defaults, `validate-workflow.py` must pass before unattended goal autopilot resumes so corrupt policy cannot silently misroute turns.
5. If policy JSON is missing, invalid, or contradicts state `capability_class`, preflight fails closed at H2 rather than proceeding with an undefined model tier.

## JSON example

```json
{
  "node": "J1",
  "description": "model policy",
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
- Edge case `J1` variant 3: verify state dual-write before continuing pursuit.
- Edge case `J1` variant 4: verify state dual-write before continuing pursuit.
- Pass 3: add regression test or evidence path specific to `J1`.
- Pass 3: cross-link related nodes in same branch index.

## Failure modes

- **Silent stop:** Agent ends turn without updating queue â†’ mitigated by /loop + check-hierarchy-queue.py EMPTY gate.
- **False complete:** Item marked done without artifact â†’ audit-hierarchy-depth.py re-enqueues deepen pass.
- **Scope bleed:** Worker edits journal/state during planning-only expansion â†’ forbidden in vision-expansion-prompt.
- **Stale design:** Upstream vision Â§ changes â†’ reconcile-stale adds deepen items for affected ids.

## Concrete implementation

1. Map `J1` to v2.14â€“v2.23 release row in SEC-15-index.md.
2. Create or extend S0 script if behavior is file-derived.
3. Add unit test under tests/unit/test_j1.py when script exists.
4. Validate `J1` against SEC-15 release checklist and parent index links.
5. Document `J1` in parent index with verify command and release tag.
6. Add checklist row in SEC-15 release doc for `J1`.

## Verification

| Check | Command |
|-------|---------|
| Completeness | `python scripts/automation/audit-hierarchy-depth.py --strict --ids J1` |
| Conformance | `python scripts/validate-workflow.py` |
| Task evidence | `python scripts/verify-router.py` when implement task exists |

## Dependencies

| Link | Why |
|------|-----|
| [full-automation-vision-and-hierarchy.md](../../full-automation-vision-and-hierarchy.md) §12 | Master hierarchy |
| [—-index](—-index.md) | Parent grouping |
| [genius-conductor-tiered-routing.md](../../genius-conductor-tiered-routing.md) | S0–S4 routing |

## Acceptance criteria

- [ ] `python scripts/automation/audit-hierarchy-depth.py --strict --ids J1` passes
- [ ] Named script, skill, or test path exists or is listed in SEC-15 release row
- [ ] Linked from [—-index](—-index.md)
- [ ] `python scripts/validate-workflow.py` passes after implement

## Cross-links

- [hierarchy-expander SKILL](../../../.cursor/skills/hierarchy-expander/SKILL.md)
