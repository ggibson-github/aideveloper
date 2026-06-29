<!-- Complete pass 3 2026-06-28 H3 -->

# H3: artifact graphs

**Parent:** — · **Branch H** · **Vision §10** · **Release:** v2.18

## Reader narrative
<!-- prose-source: agent plane-h 2026-06-28 -->

Artifact graphs declare dependency edges between design nodes, task cards, pack fragments, and integration manifest entries—program mode reads the graph before parallel spawn ([B5.3](B5.3-handoff-manifest-artifact-graph.md), [C4.4](C4.4-artifact-graph-per-program-and-pack.md)).

reconcile-artifact-graph marks nodes stale when upstream changes; reconcile-stale plans re-runs ([E5.1](E5.1-staleness-design-graph-staleness-json.md)). Graph state persists in state.json program block and docs/manifest/staleness.json. Workers must not proceed on stale manifest nodes without conductor reconcile approval.

## Purpose

H3 defines artifact graphs for the agent-driven expert system. Persistence — journal, state.json, graphs, evidence.
## Scope

- Owns `H3` only; siblings under `—` must not duplicate this spec.
- Aligns with minimal HITL: H1 plan, H2 blocker, H3 sign-off ([INTRO-1.2](INTRO-1.2-human-touchpoint-contract-h1-h2-h3.md)).
- Conflicts resolve in favor of [Vision §10 — Branch H — Persistence & state plane](../../full-automation-vision-and-hierarchy.md#10-branch-h-persistence-state-plane).

```
│   ├── A2.5 if goal_verify pass → transition to H3 pending (final sign-off)
│   ├── A2.6 loop until: blocked | budget | achieved | H3 reject
│   ├── A4.1 human: H1 | H2 | H3
│   ├── A5.2 “continue” ≠ approval (move approvals to self-gate or H1/H3 only)
│   ├── G2.3 blocks H3 until pass
│   ├── H1.5 hitl: { pending: H1|H2|H3|null, since, payload }
├── H3. Artifact graphs — design + program + platform staleness
└── I5.2 optional webhook/email on H2/H3 only
```
## Behavior / step logic
<!-- timeline-source: agent cursor-agent 2026-06-28 -->

1. Before orchestrate-program spawns parallel lanes, the conductor loads the artifact graph from state.json and the integration manifest so each downstream node declares dependencies on upstream design, task-card, and pack artifacts ([B5.3](B5.3-handoff-manifest-artifact-graph.md), [C4.4](C4.4-artifact-graph-per-program-and-pack.md)).
2. When an upstream spec or design file changes, reconcile-artifact-graph marks affected graph nodes stale in docs/manifest/staleness.json and the state.json program block so pursuit cannot treat dependents as current ([E5.1](E5.1-staleness-design-graph-staleness-json.md)).
3. If reconcile-stale finds stale manifest nodes, the conductor halts ready lane spawn until it plans the prescribed re-run or records an operator-approved waiver—workers fail closed on stale graph entries.
4. Graph edges tie design nodes, task cards, pack fragments, and manifest rows together so handoff and integration checks can verify cross-stream contracts before parallel execution proceeds.
5. On missing dependency metadata, unresolved stale nodes, or graph drift between staleness.json and state.json, pursuit stops at H2 until reconcile completes and preflight passes again.

## JSON example

```json
{
  "node": "H3",
  "description": "artifact graphs",
  "state": { "ref": "APP-B-state-json-sketch.md" },
  "implemented_in_release": "v2.14+"
}
```


## Repo artifacts (this branch)

- `journal/state.json`
- `journal/progress.md`
- `evidence/`
- `docs/manifest/staleness.json`

## Edge cases

- Operator closes laptop mid-loop â€” state.json must resume from last good dual-write.
- Concurrent manual edit to queue JSON â€” conductor reloads queue each wake; last writer wins with journal note.
- Edge case `H3` variant 3: verify state dual-write before continuing pursuit.
- Edge case `H3` variant 4: verify state dual-write before continuing pursuit.
- Pass 3: add regression test or evidence path specific to `H3`.
- Pass 3: cross-link related nodes in same branch index.

## Failure modes

- **Silent stop:** Agent ends turn without updating queue â†’ mitigated by /loop + check-hierarchy-queue.py EMPTY gate.
- **False complete:** Item marked done without artifact â†’ audit-hierarchy-depth.py re-enqueues deepen pass.
- **Scope bleed:** Worker edits journal/state during planning-only expansion â†’ forbidden in vision-expansion-prompt.
- **Stale design:** Upstream vision Â§ changes â†’ reconcile-stale adds deepen items for affected ids.

## Concrete implementation

1. Map `H3` to v2.14â€“v2.23 release row in SEC-15-index.md.
2. Create or extend S0 script if behavior is file-derived.
3. Add unit test under tests/unit/test_h3.py when script exists.
4. Validate `H3` against SEC-15 release checklist and parent index links.
5. Document `H3` in parent index with verify command and release tag.
6. Add checklist row in SEC-15 release doc for `H3`.

## Verification

| Check | Command |
|-------|---------|
| Completeness | `python scripts/automation/audit-hierarchy-depth.py --strict --ids H3` |
| Conformance | `python scripts/validate-workflow.py` |
| Task evidence | `python scripts/verify-router.py` when implement task exists |

## Dependencies

| Link | Why |
|------|-----|
| [full-automation-vision-and-hierarchy.md](../../full-automation-vision-and-hierarchy.md) §10 | Master hierarchy |
| [—-index](—-index.md) | Parent grouping |
| [genius-conductor-tiered-routing.md](../../genius-conductor-tiered-routing.md) | S0–S4 routing |

## Acceptance criteria

- [ ] `python scripts/automation/audit-hierarchy-depth.py --strict --ids H3` passes
- [ ] Named script, skill, or test path exists or is listed in SEC-15 release row
- [ ] Linked from [—-index](—-index.md)
- [ ] `python scripts/validate-workflow.py` passes after implement

## Cross-links

- [hierarchy-expander SKILL](../../../.cursor/skills/hierarchy-expander/SKILL.md)
