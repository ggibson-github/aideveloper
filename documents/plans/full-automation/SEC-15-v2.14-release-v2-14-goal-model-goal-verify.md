<!-- Complete pass 3 2026-06-28 SEC-15 -->

# SEC-15: v2.14 release v2 14 goal model goal verify

**Parent:** — · **Branch SEC** · **Vision §15** · **Release:** v2.14

## Reader narrative
<!-- prose-source: agent meta 2026-06-28 -->

Release v2.14 establishes the goal model in state.json and introduces goal_verify as a first-class field alongside extended check-pipeline-blocked semantics. Without this release, pursuit cannot attach verification to nested goals or distinguish task done from goal achieved.

Deliverables include goal-keeper behavior, additive state.goal schema, and tests that fail if goal_verify is bypassed.

## Purpose

SEC-15-v2.14 defines release v2 14 goal model goal verify for the agent-driven expert system. Roadmap, gap analysis, pursuit flow, decisions.
## Scope

- Owns `SEC-15-v2.14` only; siblings under `SEC-15-v2` must not duplicate this spec.
- Aligns with minimal HITL: H1 plan, H2 blocker, H3 sign-off ([INTRO-1.2](INTRO-1.2-human-touchpoint-contract-h1-h2-h3.md)).
- Conflicts resolve in favor of [Vision §15 — Implementation roadmap (additive v2 releases)](../../full-automation-vision-and-hierarchy.md#15-implementation-roadmap-additive-v2-releases).

```
SEC-15-v2.14 release v2 14 goal model goal verify
```
## Behavior / step logic
<!-- timeline-source: agent cursor-agent 2026-06-28 -->

1. When v2.14 ships, goal-keeper populates state.goal with goal_id, parent_goal, goal_type, success_criteria, and goal_verify_command per [A1](A1-index.md) in the same H1 dual-write that clears plan approval.
2. check-pipeline-blocked.py gains extended semantics: goal_autopilot reads goal fields, evaluates scope completion, and routes to [A2.4](A2.4-goal-scope-complete-run-goal-verify.md) instead of treating implement complete as goal achieved.
3. Tasks still require task-level evidence via [G1.1](G1.1-task-verify-router-verifier.md); v2.14 adds the distinction that passing task verify is necessary while goal_verify is sufficient for H3 transition per [G2.3](G2.3-goal-verify-blocks-h3-until-pass.md).
4. Meta-tests fail if goal_verify is bypassed—pursuit cannot set goal.state=achieved without running goal_verify_command and recording exit code in state.
5. Until the v2.14 goal block exists, preflight treats missing goal fields as H2 blockers rather than improvising pursuit scope on legacy state.json.

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
  "node": "SEC-15-v2.14",
  "description": "release v2 14 goal model goal verify",
  "state": { "ref": "APP-B-state-json-sketch.md" },
  "implemented_in_release": "v2.14+"
}
```


## Repo artifacts (this branch)



## Edge cases

- Operator closes laptop mid-loop â€” state.json must resume from last good dual-write.
- Concurrent manual edit to queue JSON â€” conductor reloads queue each wake; last writer wins with journal note.
- Edge case `SEC-15-v2.14` variant 3: verify state dual-write before continuing pursuit.
- Edge case `SEC-15-v2.14` variant 4: verify state dual-write before continuing pursuit.
- Pass 3: add regression test or evidence path specific to `SEC-15-v2.14`.
- Pass 3: cross-link related nodes in same branch index.

## Failure modes

- **Silent stop:** Agent ends turn without updating queue â†’ mitigated by /loop + check-hierarchy-queue.py EMPTY gate.
- **False complete:** Item marked done without artifact â†’ audit-hierarchy-depth.py re-enqueues deepen pass.
- **Scope bleed:** Worker edits journal/state during planning-only expansion â†’ forbidden in vision-expansion-prompt.
- **Stale design:** Upstream vision Â§ changes â†’ reconcile-stale adds deepen items for affected ids.

## Concrete implementation

1. Map `SEC-15-v2.14` to v2.14â€“v2.23 release row in SEC-15-index.md.
2. Create or extend S0 script if behavior is file-derived.
3. Add unit test under tests/unit/test_sec-15-v2_14.py when script exists.
4. Validate `SEC-15-v2.14` against SEC-15 release checklist and parent index links.
5. Document `SEC-15-v2.14` in parent index with verify command and release tag.
6. Add checklist row in SEC-15 release doc for `SEC-15-v2.14`.

## Release deliverables (SEC-15)

- Schema: additive `state.json` fields only
- Scripts: S0 tools for SEC-15-v2.14
- Skills/tests/docs per vision roadmap row

## Verification

| Check | Command |
|-------|---------|
| Completeness | `python scripts/automation/audit-hierarchy-depth.py --strict --ids SEC-15-v2.14` |
| Conformance | `python scripts/validate-workflow.py` |
| Task evidence | `python scripts/verify-router.py` when implement task exists |

## Dependencies

| Link | Why |
|------|-----|
| [full-automation-vision-and-hierarchy.md](../../full-automation-vision-and-hierarchy.md) §15 | Master hierarchy |
| [SEC-15-v2-index](SEC-15-v2-index.md) | Parent grouping |
| [genius-conductor-tiered-routing.md](../../genius-conductor-tiered-routing.md) | S0–S4 routing |

## Acceptance criteria

- [ ] `python scripts/automation/audit-hierarchy-depth.py --strict --ids SEC-15-v2.14` passes
- [ ] Named script, skill, or test path exists or is listed in SEC-15 release row
- [ ] Linked from [SEC-15-v2-index](SEC-15-v2-index.md)
- [ ] `python scripts/validate-workflow.py` passes after implement

## Cross-links

- [hierarchy-expander SKILL](../../../.cursor/skills/hierarchy-expander/SKILL.md)
