<!-- Complete pass 3 2026-06-28 SEC-15 -->

# SEC-15: v2.23 release v2 23 operator polish h2 audit dashboard

**Parent:** — · **Branch SEC** · **Vision §15** · **Release:** v2.23

## Reader narrative
<!-- prose-source: agent meta 2026-06-28 -->

Release v2.23 polishes operator experience: H2 notifications, self-gate audit trails, and dashboard surfaces for goal depth and queue depth. Autonomy without observability erodes trust—this release makes pursuit legible from STATUS.md and dashboard.md.

It closes the initial v2.14–v2.23 roadmap; later work continues additively on state.json version 2.

## Purpose

SEC-15-v2.23 defines release v2 23 operator polish h2 audit dashboard for the agent-driven expert system. Roadmap, gap analysis, pursuit flow, decisions.
## Scope

- Owns `SEC-15-v2.23` only; siblings under `SEC-15-v2` must not duplicate this spec.
- Aligns with minimal HITL: H1 plan, H2 blocker, H3 sign-off ([INTRO-1.2](INTRO-1.2-human-touchpoint-contract-h1-h2-h3.md)).
- Conflicts resolve in favor of [Vision §15 — Implementation roadmap (additive v2 releases)](../../full-automation-vision-and-hierarchy.md#15-implementation-roadmap-additive-v2-releases).

```
SEC-15-v2.23 release v2 23 operator polish h2 audit dashboard
```
## Behavior / step logic
<!-- timeline-source: agent cli-composer-2.5 2026-06-28 -->

1. When [A3.2](A3.2-goal-autopilot-until-goal-verify-or-hard-block.md) goal_autopilot is active, [A1.4](A1.4-deadline-budget-steps-tokens-wall-clock.md) budget fields in state.goal govern max steps, tokens, and wall-clock—operators choose unlimited pursuit versus checkpoint caps via this open SEC-17 decision.
2. Each pursuit wake increments budget counters in state.json after [A2.3](A2.3-post-step-route-tier-dual-write-increment.md) dual-write so dashboards and autopilot daemons share the same consumption picture before the next [A2.1](A2.1-preflight-check-pipeline-blocked-extended.md) preflight.
3. Unlimited mode lets goal_autopilot run until goal_verify, a hard [A4](A4-index.md) block, or HITL—without arbitrary daily ceilings beyond operator-approved H1 plan bounds.
4. Checkpoint mode stops pursuit when any budget exhausts and surfaces H2 via [A4.3](A4.3-stop-resource-max-steps-max-cost-lease-expired.md) resource stop taxonomy until the operator resets caps or approves continuation.
5. If budget telemetry is missing or counters desync from journal step counts, pursuit fails closed at H2—never silently continuing goal_autopilot without visibility into cost burn.

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
  "node": "SEC-15-v2.23",
  "description": "release v2 23 operator polish h2 audit dashboard",
  "state": { "ref": "APP-B-state-json-sketch.md" },
  "implemented_in_release": "v2.14+"
}
```


## Repo artifacts (this branch)



## Edge cases

- Operator closes laptop mid-loop â€” state.json must resume from last good dual-write.
- Concurrent manual edit to queue JSON â€” conductor reloads queue each wake; last writer wins with journal note.
- Edge case `SEC-15-v2.23` variant 3: verify state dual-write before continuing pursuit.
- Edge case `SEC-15-v2.23` variant 4: verify state dual-write before continuing pursuit.
- Pass 3: add regression test or evidence path specific to `SEC-15-v2.23`.
- Pass 3: cross-link related nodes in same branch index.

## Failure modes

- **Silent stop:** Agent ends turn without updating queue â†’ mitigated by /loop + check-hierarchy-queue.py EMPTY gate.
- **False complete:** Item marked done without artifact â†’ audit-hierarchy-depth.py re-enqueues deepen pass.
- **Scope bleed:** Worker edits journal/state during planning-only expansion â†’ forbidden in vision-expansion-prompt.
- **Stale design:** Upstream vision Â§ changes â†’ reconcile-stale adds deepen items for affected ids.

## Concrete implementation

1. Map `SEC-15-v2.23` to v2.14â€“v2.23 release row in SEC-15-index.md.
2. Create or extend S0 script if behavior is file-derived.
3. Add unit test under tests/unit/test_sec-15-v2_23.py when script exists.
4. Validate `SEC-15-v2.23` against SEC-15 release checklist and parent index links.
5. Document `SEC-15-v2.23` in parent index with verify command and release tag.
6. Add checklist row in SEC-15 release doc for `SEC-15-v2.23`.

## Release deliverables (SEC-15)

- Schema: additive `state.json` fields only
- Scripts: S0 tools for SEC-15-v2.23
- Skills/tests/docs per vision roadmap row

## Verification

| Check | Command |
|-------|---------|
| Completeness | `python scripts/automation/audit-hierarchy-depth.py --strict --ids SEC-15-v2.23` |
| Conformance | `python scripts/validate-workflow.py` |
| Task evidence | `python scripts/verify-router.py` when implement task exists |

## Dependencies

| Link | Why |
|------|-----|
| [full-automation-vision-and-hierarchy.md](../../full-automation-vision-and-hierarchy.md) §15 | Master hierarchy |
| [SEC-15-v2-index](SEC-15-v2-index.md) | Parent grouping |
| [genius-conductor-tiered-routing.md](../../genius-conductor-tiered-routing.md) | S0–S4 routing |

## Acceptance criteria

- [ ] `python scripts/automation/audit-hierarchy-depth.py --strict --ids SEC-15-v2.23` passes
- [ ] Named script, skill, or test path exists or is listed in SEC-15 release row
- [ ] Linked from [SEC-15-v2-index](SEC-15-v2-index.md)
- [ ] `python scripts/validate-workflow.py` passes after implement

## Cross-links

- [hierarchy-expander SKILL](../../../.cursor/skills/hierarchy-expander/SKILL.md)
