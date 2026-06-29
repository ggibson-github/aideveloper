<!-- Complete pass 3 2026-06-28 SEC-15 -->

# SEC-15: v2.15 release v2 15 pursuit loop goal autopilot self gate

**Parent:** — · **Branch SEC** · **Vision §15** · **Release:** v2.15

## Reader narrative
<!-- prose-source: agent meta 2026-06-28 -->

Release v2.15 hardens the pursuit loop: goal_autopilot mode, optional uncapped session settings, and self-gate defaults for HLD/DD when strict_hitl is false. This is the release that makes "always-on" real rather than a 25-step autopilot cap.

Preflight, one-step execution, and stop-reason taxonomy from Plane A must be green before later platform work relies on them.

## Purpose

SEC-15-v2.15 defines release v2 15 pursuit loop goal autopilot self gate for the agent-driven expert system. Roadmap, gap analysis, pursuit flow, decisions.
## Scope

- Owns `SEC-15-v2.15` only; siblings under `SEC-15-v2` must not duplicate this spec.
- Aligns with minimal HITL: H1 plan, H2 blocker, H3 sign-off ([INTRO-1.2](INTRO-1.2-human-touchpoint-contract-h1-h2-h3.md)).
- Conflicts resolve in favor of [Vision §15 — Implementation roadmap (additive v2 releases)](../../full-automation-vision-and-hierarchy.md#15-implementation-roadmap-additive-v2-releases).

```
SEC-15-v2.15 release v2 15 pursuit loop goal autopilot self gate
```
## Behavior / step logic
<!-- timeline-source: agent cli-composer-2.5 2026-06-28 -->

1. When `next_action` lands on a templated design phase—HLD, DD, diagrams, or task-breakdown—the genius conductor invokes the matching S2 skill (hld-writer, dd-writer, task-breakdown, diagram-generator) rather than improvising artifact structure in chat.
2. S2 skills write into repo template paths under `docs/design/`, task cards, and diagram stubs; the conductor then runs [B1.1](B1.1-s0-deterministic-mandatory-first.md) validation to check template conformance before dual-write advances `next_action`.
3. Phase outputs declare catalog component refs so S2 artifacts register on Plane E staleness graphs and bind to Plane G evidence paths for downstream implement turns.
4. Active template packs extend S2 surfaces in template-packs per Plane F; consumer goals compose from pack fragments instead of forking ad hoc template copies that drift from certification baselines.
5. If template validation fails, critic review finds structural gaps, or declared S2 artifacts are missing on disk, pursuit stops at H2 until the conductor re-runs the S2 skill with reconciled inputs.

```mermaid
flowchart TD
  start[Pursuit turn] --> pre[S0 preflight]
  pre -->|READY| step[One step]
  pre -->|BLOCKED| exit[Stop: H2 or budget]
  step --> goal{goal_scope_complete?}
  goal -->|yes| gv[goal_verify]
  goal -->|no| start
  gv -->|pass| h3[H3 pending]
  gv -->|fail| exit
```

## JSON example

```json
{
  "node": "SEC-15-v2.15",
  "description": "release v2 15 pursuit loop goal autopilot self gate",
  "state": { "ref": "APP-B-state-json-sketch.md" },
  "implemented_in_release": "v2.14+"
}
```


## Repo artifacts (this branch)



## Edge cases

- Operator closes laptop mid-loop â€” state.json must resume from last good dual-write.
- Concurrent manual edit to queue JSON â€” conductor reloads queue each wake; last writer wins with journal note.
- Edge case `SEC-15-v2.15` variant 3: verify state dual-write before continuing pursuit.
- Edge case `SEC-15-v2.15` variant 4: verify state dual-write before continuing pursuit.
- Pass 3: add regression test or evidence path specific to `SEC-15-v2.15`.
- Pass 3: cross-link related nodes in same branch index.

## Failure modes

- **Silent stop:** Agent ends turn without updating queue â†’ mitigated by /loop + check-hierarchy-queue.py EMPTY gate.
- **False complete:** Item marked done without artifact â†’ audit-hierarchy-depth.py re-enqueues deepen pass.
- **Scope bleed:** Worker edits journal/state during planning-only expansion â†’ forbidden in vision-expansion-prompt.
- **Stale design:** Upstream vision Â§ changes â†’ reconcile-stale adds deepen items for affected ids.

## Concrete implementation

1. Map `SEC-15-v2.15` to v2.14â€“v2.23 release row in SEC-15-index.md.
2. Create or extend S0 script if behavior is file-derived.
3. Add unit test under tests/unit/test_sec-15-v2_15.py when script exists.
4. Validate `SEC-15-v2.15` against SEC-15 release checklist and parent index links.
5. Document `SEC-15-v2.15` in parent index with verify command and release tag.
6. Add checklist row in SEC-15 release doc for `SEC-15-v2.15`.

## Release deliverables (SEC-15)

- Schema: additive `state.json` fields only
- Scripts: S0 tools for SEC-15-v2.15
- Skills/tests/docs per vision roadmap row

## Verification

| Check | Command |
|-------|---------|
| Completeness | `python scripts/automation/audit-hierarchy-depth.py --strict --ids SEC-15-v2.15` |
| Conformance | `python scripts/validate-workflow.py` |
| Task evidence | `python scripts/verify-router.py` when implement task exists |

## Dependencies

| Link | Why |
|------|-----|
| [full-automation-vision-and-hierarchy.md](../../full-automation-vision-and-hierarchy.md) §15 | Master hierarchy |
| [SEC-15-v2-index](SEC-15-v2-index.md) | Parent grouping |
| [genius-conductor-tiered-routing.md](../../genius-conductor-tiered-routing.md) | S0–S4 routing |

## Acceptance criteria

- [ ] `python scripts/automation/audit-hierarchy-depth.py --strict --ids SEC-15-v2.15` passes
- [ ] Named script, skill, or test path exists or is listed in SEC-15 release row
- [ ] Linked from [SEC-15-v2-index](SEC-15-v2-index.md)
- [ ] `python scripts/validate-workflow.py` passes after implement

## Cross-links

- [hierarchy-expander SKILL](../../../.cursor/skills/hierarchy-expander/SKILL.md)
