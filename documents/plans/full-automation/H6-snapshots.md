<!-- Complete pass 3 2026-06-28 H6 -->

# H6: snapshots

**Parent:** — · **Branch H** · **Vision §10** · **Release:** v2.15

## Reader narrative
<!-- prose-source: agent plane-h 2026-06-28 -->

Snapshots capture pursuit state before context compaction or session handoff—preCompact hook triggers sync-state.py to write timestamped snapshot files alongside live journal/state.json ([I1.4](I1.4-runtime-ide-hooks-beforesubmit-subagentstart-pretooluse-prec.md)).

Recovery resumes from last good dual-write if operator closes mid-loop; snapshots are recovery aids, not the primary router. SDK daemon and headless runs use the same snapshot contract ([I2.1](I2.1-runtime-sdk-run-local-pipeline-goal-autopilot.md)). validate-workflow.py rejects corrupt state before autopilot continues.

## Purpose

H6 defines snapshots for the agent-driven expert system. Persistence — journal, state.json, graphs, evidence.
## Scope

- Owns `H6` only; siblings under `—` must not duplicate this spec.
- Aligns with minimal HITL: H1 plan, H2 blocker, H3 sign-off ([INTRO-1.2](INTRO-1.2-human-touchpoint-contract-h1-h2-h3.md)).
- Conflicts resolve in favor of [Vision §10 — Branch H — Persistence & state plane](../../full-automation-vision-and-hierarchy.md#10-branch-h-persistence-state-plane).

```
└── H6. Snapshots — preCompact hook, state repair via sync-state.py
```
## Behavior / step logic
<!-- timeline-source: agent cli-composer-2.5 2026-06-28 -->

1. During product pursuit the conductor and S0 scripts detect repeated manual commands, missing playbooks, or verify failures and enqueue platform work items per D2 without blocking the current product `next_action` unless H2 requires it.
2. Each platform turn is scheduled per D3.1—one platform dequeue after K product steps—so delivery continues while reuse matures from L0 ephemeral reasoning toward L2 scripts and L3 skills on the D1 promotion ladder.
3. When dequeuing, D2.3 runs exactly one platform-queue item as an economy turn with S0 extraction scripts before any improvisational catalog work.
4. Completed promotions dual-write to catalog manifests, playbooks, and skills per D1 maturity rungs; staleness nodes bump so E5 reconcile can flag dependents.
5. If platform backlog exceeds age or depth thresholds from D3.5, pursuit prioritizes a drain turn or stops at H2 when enqueue would starve an active goal slice.

## JSON example

```json
{
  "node": "H6",
  "description": "snapshots",
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
- Edge case `H6` variant 3: verify state dual-write before continuing pursuit.
- Edge case `H6` variant 4: verify state dual-write before continuing pursuit.
- Pass 3: add regression test or evidence path specific to `H6`.
- Pass 3: cross-link related nodes in same branch index.

## Failure modes

- **Silent stop:** Agent ends turn without updating queue â†’ mitigated by /loop + check-hierarchy-queue.py EMPTY gate.
- **False complete:** Item marked done without artifact â†’ audit-hierarchy-depth.py re-enqueues deepen pass.
- **Scope bleed:** Worker edits journal/state during planning-only expansion â†’ forbidden in vision-expansion-prompt.
- **Stale design:** Upstream vision Â§ changes â†’ reconcile-stale adds deepen items for affected ids.

## Concrete implementation

1. Map `H6` to v2.14â€“v2.23 release row in SEC-15-index.md.
2. Create or extend S0 script if behavior is file-derived.
3. Add unit test under tests/unit/test_h6.py when script exists.
4. Validate `H6` against SEC-15 release checklist and parent index links.
5. Document `H6` in parent index with verify command and release tag.
6. Add checklist row in SEC-15 release doc for `H6`.

## Verification

| Check | Command |
|-------|---------|
| Completeness | `python scripts/automation/audit-hierarchy-depth.py --strict --ids H6` |
| Conformance | `python scripts/validate-workflow.py` |
| Task evidence | `python scripts/verify-router.py` when implement task exists |

## Dependencies

| Link | Why |
|------|-----|
| [full-automation-vision-and-hierarchy.md](../../full-automation-vision-and-hierarchy.md) §10 | Master hierarchy |
| [—-index](—-index.md) | Parent grouping |
| [genius-conductor-tiered-routing.md](../../genius-conductor-tiered-routing.md) | S0–S4 routing |

## Acceptance criteria

- [ ] `python scripts/automation/audit-hierarchy-depth.py --strict --ids H6` passes
- [ ] Named script, skill, or test path exists or is listed in SEC-15 release row
- [ ] Linked from [—-index](—-index.md)
- [ ] `python scripts/validate-workflow.py` passes after implement

## Cross-links

- [hierarchy-expander SKILL](../../../.cursor/skills/hierarchy-expander/SKILL.md)
