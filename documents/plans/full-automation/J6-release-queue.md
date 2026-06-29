<!-- Complete pass 3 2026-06-28 J6 -->

# J6: release queue

**Parent:** — · **Branch J** · **Vision §12** · **Release:** v2.16

## Reader narrative
<!-- prose-source: agent plane-j 2026-06-28 -->

`docs/automation/release-queue.json` tracks harness evolution rows—v2.14 through v2.23 SEC-15 capabilities—with implement status, verify commands, and waiver links. It is the operator-facing backlog for platform maturity separate from consumer product goals.

Release queue drain promotes S0 scripts, skills, and pack fragments when rows ship; stale rows re-enqueue via hierarchy-expander audit. Pair with platform promotion_queue in state ([H1.3](H1.3-state-platform-block.md)) and SEC-15-index release checklist. Completed rows update dashboard maturity indicators ([I5.1](I5.1-runtime-notify-status-dashboard-generation.md)).

## Purpose

J6 defines release queue for the agent-driven expert system. Governance — policy, waivers, audit, export contract.
## Scope

- Owns `J6` only; siblings under `—` must not duplicate this spec.
- Aligns with minimal HITL: H1 plan, H2 blocker, H3 sign-off ([INTRO-1.2](INTRO-1.2-human-touchpoint-contract-h1-h2-h3.md)).
- Conflicts resolve in favor of [Vision §12 — Branch J — Governance & operator plane](../../full-automation-vision-and-hierarchy.md#12-branch-j-governance-operator-plane).

```
└── J6. release-queue.json — harness evolution (separate from consumer goals)
```
## Behavior / step logic
<!-- timeline-source: agent cli-composer-2.5 2026-06-28 -->

1. When the operator types `/continue` or a daemon poll fires with autopilot inactive, the conductor runs [A2.1](A2.1-preflight-check-pipeline-blocked-extended.md) via `check-pipeline-blocked.py`—advancing only when status is READY.
2. If preflight reports BLOCKED from [A4](A4-index.md), Continue re-prompts for the specific human action instead of advancing `next_action` or treating the word as implicit approval.
3. On READY, exactly one [A2.2](A2.2-if-ready-execute-one-pipeline-step.md) skill phase executes followed by [A2.3](A2.3-post-step-route-tier-dual-write-increment.md) dual-write—matching [A2.7](A2.7-no-intermediate-wait-for-continue.md) one-step semantics.
4. [A3.4](A3.4-sdk-daemon-run-local-pipeline-24-7.md) SDK daemon invokes the same contract on poll when goal autopilot is off—IDE and headless runners share identical semantics.
5. If the operator intended to approve a design gate or answer a blocker, pursuit stays blocked until an explicit approval phrase per [A5.2](A5.2-continue-not-approval-self-gate-h1-h3-only.md)—Continue alone never clears self-gates.

## JSON example

```json
{
  "node": "J6",
  "description": "release queue",
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
- Edge case `J6` variant 3: verify state dual-write before continuing pursuit.
- Edge case `J6` variant 4: verify state dual-write before continuing pursuit.
- Pass 3: add regression test or evidence path specific to `J6`.
- Pass 3: cross-link related nodes in same branch index.

## Failure modes

- **Silent stop:** Agent ends turn without updating queue â†’ mitigated by /loop + check-hierarchy-queue.py EMPTY gate.
- **False complete:** Item marked done without artifact â†’ audit-hierarchy-depth.py re-enqueues deepen pass.
- **Scope bleed:** Worker edits journal/state during planning-only expansion â†’ forbidden in vision-expansion-prompt.
- **Stale design:** Upstream vision Â§ changes â†’ reconcile-stale adds deepen items for affected ids.

## Concrete implementation

1. Map `J6` to v2.14â€“v2.23 release row in SEC-15-index.md.
2. Create or extend S0 script if behavior is file-derived.
3. Add unit test under tests/unit/test_j6.py when script exists.
4. Validate `J6` against SEC-15 release checklist and parent index links.
5. Document `J6` in parent index with verify command and release tag.
6. Add checklist row in SEC-15 release doc for `J6`.

## Verification

| Check | Command |
|-------|---------|
| Completeness | `python scripts/automation/audit-hierarchy-depth.py --strict --ids J6` |
| Conformance | `python scripts/validate-workflow.py` |
| Task evidence | `python scripts/verify-router.py` when implement task exists |

## Dependencies

| Link | Why |
|------|-----|
| [full-automation-vision-and-hierarchy.md](../../full-automation-vision-and-hierarchy.md) §12 | Master hierarchy |
| [—-index](—-index.md) | Parent grouping |
| [genius-conductor-tiered-routing.md](../../genius-conductor-tiered-routing.md) | S0–S4 routing |

## Acceptance criteria

- [ ] `python scripts/automation/audit-hierarchy-depth.py --strict --ids J6` passes
- [ ] Named script, skill, or test path exists or is listed in SEC-15 release row
- [ ] Linked from [—-index](—-index.md)
- [ ] `python scripts/validate-workflow.py` passes after implement

## Cross-links

- [hierarchy-expander SKILL](../../../.cursor/skills/hierarchy-expander/SKILL.md)
