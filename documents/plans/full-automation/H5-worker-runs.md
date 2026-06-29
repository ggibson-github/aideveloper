<!-- Complete pass 3 2026-06-28 H5 -->

# H5: worker runs

**Parent:** — · **Branch H** · **Vision §10** · **Release:** v2.15

## Reader narrative
<!-- prose-source: agent plane-h 2026-06-28 -->

`worker-runs.jsonl` append-only audit records each subagent spawn: role, model_tier, allowed_reads, task id, timestamps, and outcome summary. The conductor logs spawns; workers do not self-log journal/state changes.

Audit trail supports cost review, debugging scope bleed, and [J4](J4-audit.md) governance queries. Parallel program lanes produce interleaved lines—correlate by goal id and lane lease ([C4.1](C4.1-workstreams-lane-json-leases.md)). Retention policy belongs in operator pack; default keeps full session history locally.

## Purpose

H5 defines worker runs for the agent-driven expert system. Persistence — journal, state.json, graphs, evidence.
## Scope

- Owns `H5` only; siblings under `—` must not duplicate this spec.
- Aligns with minimal HITL: H1 plan, H2 blocker, H3 sign-off ([INTRO-1.2](INTRO-1.2-human-touchpoint-contract-h1-h2-h3.md)).
- Conflicts resolve in favor of [Vision §10 — Branch H — Persistence & state plane](../../full-automation-vision-and-hierarchy.md#10-branch-h-persistence-state-plane).

```
├── H5. worker-runs.jsonl — audit subagent usage
```
## Behavior / step logic
<!-- timeline-source: agent cli-composer-2.5 2026-06-28 -->

1. After H1 approves the plan, the conductor sets autopilot.active and loops pursuit without a per-session step ceiling.
2. Each iteration runs S0 preflight then exactly one pipeline phase per A2.2.
3. When scope is complete, pursuit triggers goal_verify per A2.4 instead of another implement task.
4. The loop stops on goal_verify pass, a hard block from A4, or budget exhaustion from A1.4.
5. On corrupt state or failed validate-workflow, pursuit halts at H2 rather than continuing with bad state.

## JSON example

```json
{
  "node": "H5",
  "description": "worker runs",
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
- Edge case `H5` variant 3: verify state dual-write before continuing pursuit.
- Edge case `H5` variant 4: verify state dual-write before continuing pursuit.
- Pass 3: add regression test or evidence path specific to `H5`.
- Pass 3: cross-link related nodes in same branch index.

## Failure modes

- **Silent stop:** Agent ends turn without updating queue â†’ mitigated by /loop + check-hierarchy-queue.py EMPTY gate.
- **False complete:** Item marked done without artifact â†’ audit-hierarchy-depth.py re-enqueues deepen pass.
- **Scope bleed:** Worker edits journal/state during planning-only expansion â†’ forbidden in vision-expansion-prompt.
- **Stale design:** Upstream vision Â§ changes â†’ reconcile-stale adds deepen items for affected ids.

## Concrete implementation

1. Map `H5` to v2.14â€“v2.23 release row in SEC-15-index.md.
2. Create or extend S0 script if behavior is file-derived.
3. Add unit test under tests/unit/test_h5.py when script exists.
4. Validate `H5` against SEC-15 release checklist and parent index links.
5. Document `H5` in parent index with verify command and release tag.
6. Add checklist row in SEC-15 release doc for `H5`.

## Verification

| Check | Command |
|-------|---------|
| Completeness | `python scripts/automation/audit-hierarchy-depth.py --strict --ids H5` |
| Conformance | `python scripts/validate-workflow.py` |
| Task evidence | `python scripts/verify-router.py` when implement task exists |

## Dependencies

| Link | Why |
|------|-----|
| [full-automation-vision-and-hierarchy.md](../../full-automation-vision-and-hierarchy.md) §10 | Master hierarchy |
| [—-index](—-index.md) | Parent grouping |
| [genius-conductor-tiered-routing.md](../../genius-conductor-tiered-routing.md) | S0–S4 routing |

## Acceptance criteria

- [ ] `python scripts/automation/audit-hierarchy-depth.py --strict --ids H5` passes
- [ ] Named script, skill, or test path exists or is listed in SEC-15 release row
- [ ] Linked from [—-index](—-index.md)
- [ ] `python scripts/validate-workflow.py` passes after implement

## Cross-links

- [hierarchy-expander SKILL](../../../.cursor/skills/hierarchy-expander/SKILL.md)
