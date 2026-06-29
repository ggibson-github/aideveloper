<!-- Complete pass 3 2026-06-28 SEC-15 -->

# SEC-15: v2.21 release v2 21 data platform pack reference

**Parent:** — · **Branch SEC** · **Vision §15** · **Release:** v2.21

## Reader narrative
<!-- prose-source: agent meta 2026-06-28 -->

Release v2.21 delivers a data platform pack reference implementation parallel to the game studio pack—different integrations and roles, same harness contracts. Multi-domain reuse validates Plane F generality.

Cross-pack lessons feed v2.22 shared library work; data-platform MCP and verify paths must appear in goal_verify for the demo goal.

## Purpose

SEC-15-v2.21 defines release v2 21 data platform pack reference for the agent-driven expert system. Roadmap, gap analysis, pursuit flow, decisions.
## Scope

- Owns `SEC-15-v2.21` only; siblings under `SEC-15-v2` must not duplicate this spec.
- Aligns with minimal HITL: H1 plan, H2 blocker, H3 sign-off ([INTRO-1.2](INTRO-1.2-human-touchpoint-contract-h1-h2-h3.md)).
- Conflicts resolve in favor of [Vision §15 — Implementation roadmap (additive v2 releases)](../../full-automation-vision-and-hierarchy.md#15-implementation-roadmap-additive-v2-releases).

```
SEC-15-v2.21 release v2 21 data platform pack reference
```
## Behavior / step logic
<!-- timeline-source: agent cli-composer-2.5 2026-06-28 -->

1. This release slice delivers a data platform pack reference implementation parallel to the game studio pack—different integrations and roles, same harness contracts
2. Cross-pack lessons feed v2.22 shared library work; data-platform MCP and verify paths must appear in goal_verify for the demo goal
3. This section documents cross-cutting architecture: pursuit flow, migration gaps, or release sequencing for the expert system.
4. Implementers treat SEC rows as program backlog ordering, not as ad hoc prose.
5. Release slices (SEC-15) map harness versions to shippable capability bundles.

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
  "node": "SEC-15-v2.21",
  "description": "release v2 21 data platform pack reference",
  "state": { "ref": "APP-B-state-json-sketch.md" },
  "implemented_in_release": "v2.14+"
}
```


## Repo artifacts (this branch)



## Edge cases

- Operator closes laptop mid-loop â€” state.json must resume from last good dual-write.
- Concurrent manual edit to queue JSON â€” conductor reloads queue each wake; last writer wins with journal note.
- Edge case `SEC-15-v2.21` variant 3: verify state dual-write before continuing pursuit.
- Edge case `SEC-15-v2.21` variant 4: verify state dual-write before continuing pursuit.
- Pass 3: add regression test or evidence path specific to `SEC-15-v2.21`.
- Pass 3: cross-link related nodes in same branch index.

## Failure modes

- **Silent stop:** Agent ends turn without updating queue â†’ mitigated by /loop + check-hierarchy-queue.py EMPTY gate.
- **False complete:** Item marked done without artifact â†’ audit-hierarchy-depth.py re-enqueues deepen pass.
- **Scope bleed:** Worker edits journal/state during planning-only expansion â†’ forbidden in vision-expansion-prompt.
- **Stale design:** Upstream vision Â§ changes â†’ reconcile-stale adds deepen items for affected ids.

## Concrete implementation

1. Map `SEC-15-v2.21` to v2.14â€“v2.23 release row in SEC-15-index.md.
2. Create or extend S0 script if behavior is file-derived.
3. Add unit test under tests/unit/test_sec-15-v2_21.py when script exists.
4. Validate `SEC-15-v2.21` against SEC-15 release checklist and parent index links.
5. Document `SEC-15-v2.21` in parent index with verify command and release tag.
6. Add checklist row in SEC-15 release doc for `SEC-15-v2.21`.

## Release deliverables (SEC-15)

- Schema: additive `state.json` fields only
- Scripts: S0 tools for SEC-15-v2.21
- Skills/tests/docs per vision roadmap row

## Verification

| Check | Command |
|-------|---------|
| Completeness | `python scripts/automation/audit-hierarchy-depth.py --strict --ids SEC-15-v2.21` |
| Conformance | `python scripts/validate-workflow.py` |
| Task evidence | `python scripts/verify-router.py` when implement task exists |

## Dependencies

| Link | Why |
|------|-----|
| [full-automation-vision-and-hierarchy.md](../../full-automation-vision-and-hierarchy.md) §15 | Master hierarchy |
| [SEC-15-v2-index](SEC-15-v2-index.md) | Parent grouping |
| [genius-conductor-tiered-routing.md](../../genius-conductor-tiered-routing.md) | S0–S4 routing |

## Acceptance criteria

- [ ] `python scripts/automation/audit-hierarchy-depth.py --strict --ids SEC-15-v2.21` passes
- [ ] Named script, skill, or test path exists or is listed in SEC-15 release row
- [ ] Linked from [SEC-15-v2-index](SEC-15-v2-index.md)
- [ ] `python scripts/validate-workflow.py` passes after implement

## Cross-links

- [hierarchy-expander SKILL](../../../.cursor/skills/hierarchy-expander/SKILL.md)
