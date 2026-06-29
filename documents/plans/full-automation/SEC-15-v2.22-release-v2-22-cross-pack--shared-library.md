<!-- Complete pass 3 2026-06-28 SEC-15 -->

# SEC-15: v2.22 release v2 22 cross pack  shared library

**Parent:** — · **Branch SEC** · **Vision §15** · **Release:** v2.22

## Reader narrative
<!-- prose-source: agent meta 2026-06-28 -->

Release v2.22 adds template-packs/_shared/ for cross-pack libraries—common roles, hooks, and verification helpers factored out of duplicate pack content. Packs should compose shared fragments rather than fork copy-paste.

Catalog entries should reference _shared components explicitly.

## Purpose

SEC-15-v2.22 defines release v2 22 cross pack  shared library for the agent-driven expert system. Roadmap, gap analysis, pursuit flow, decisions.
## Scope

- Owns `SEC-15-v2.22` only; siblings under `SEC-15-v2` must not duplicate this spec.
- Aligns with minimal HITL: H1 plan, H2 blocker, H3 sign-off ([INTRO-1.2](INTRO-1.2-human-touchpoint-contract-h1-h2-h3.md)).
- Conflicts resolve in favor of [Vision §15 — Implementation roadmap (additive v2 releases)](../../full-automation-vision-and-hierarchy.md#15-implementation-roadmap-additive-v2-releases).

```
SEC-15-v2.22 release v2 22 cross pack  shared library
```
## Behavior / step logic
<!-- timeline-source: agent cli-composer-2.5 2026-06-28 -->

1. When policy, pack authority, or unresolved external dependency requires human judgment beyond [B1.4](B1.4-s3-architecture-ambiguity.md) self-gate, [B2.1](B2.1-conductor-genius-merge-route-platform-drain.md) classifies the turn as S4 and stops pursuit before another [A2.2](A2.2-if-ready-execute-one-pipeline-step.md) phase runs.
2. The conductor packages an H2 blocker with goal_id, missing artifact or authority, typed stop class per [A4.1](A4.1-stop-human-h1-h2-h3.md), and a concrete operator action—never a vague “need help.”
3. Waiver requests, legal/finance pack gates, and multi-goal conflicts dual-write to journal Blockers and state.json `hitl` fields so [A2.1](A2.1-preflight-check-pipeline-blocked-extended.md) returns BLOCKED until cleared.
4. [A6.2](A6.2-notify-digest-on-h2-blocker-not-every-step.md) emits a digest notification on S4 escalation; pursuit does not busy-loop waiting for operator chat acknowledgment.
5. If S4 is invoked for work resolvable by S0/S1/S3, preflight flags mis-routing at H2—S4 is reserved for imminent H2 or policy-mandated review, not default genius-tier convenience.

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
  "node": "SEC-15-v2.22",
  "description": "release v2 22 cross pack  shared library",
  "state": { "ref": "APP-B-state-json-sketch.md" },
  "implemented_in_release": "v2.14+"
}
```


## Repo artifacts (this branch)



## Edge cases

- Operator closes laptop mid-loop â€” state.json must resume from last good dual-write.
- Concurrent manual edit to queue JSON â€” conductor reloads queue each wake; last writer wins with journal note.
- Edge case `SEC-15-v2.22` variant 3: verify state dual-write before continuing pursuit.
- Edge case `SEC-15-v2.22` variant 4: verify state dual-write before continuing pursuit.
- Pass 3: add regression test or evidence path specific to `SEC-15-v2.22`.
- Pass 3: cross-link related nodes in same branch index.

## Failure modes

- **Silent stop:** Agent ends turn without updating queue â†’ mitigated by /loop + check-hierarchy-queue.py EMPTY gate.
- **False complete:** Item marked done without artifact â†’ audit-hierarchy-depth.py re-enqueues deepen pass.
- **Scope bleed:** Worker edits journal/state during planning-only expansion â†’ forbidden in vision-expansion-prompt.
- **Stale design:** Upstream vision Â§ changes â†’ reconcile-stale adds deepen items for affected ids.

## Concrete implementation

1. Map `SEC-15-v2.22` to v2.14â€“v2.23 release row in SEC-15-index.md.
2. Create or extend S0 script if behavior is file-derived.
3. Add unit test under tests/unit/test_sec-15-v2_22.py when script exists.
4. Validate `SEC-15-v2.22` against SEC-15 release checklist and parent index links.
5. Document `SEC-15-v2.22` in parent index with verify command and release tag.
6. Add checklist row in SEC-15 release doc for `SEC-15-v2.22`.

## Release deliverables (SEC-15)

- Schema: additive `state.json` fields only
- Scripts: S0 tools for SEC-15-v2.22
- Skills/tests/docs per vision roadmap row

## Verification

| Check | Command |
|-------|---------|
| Completeness | `python scripts/automation/audit-hierarchy-depth.py --strict --ids SEC-15-v2.22` |
| Conformance | `python scripts/validate-workflow.py` |
| Task evidence | `python scripts/verify-router.py` when implement task exists |

## Dependencies

| Link | Why |
|------|-----|
| [full-automation-vision-and-hierarchy.md](../../full-automation-vision-and-hierarchy.md) §15 | Master hierarchy |
| [SEC-15-v2-index](SEC-15-v2-index.md) | Parent grouping |
| [genius-conductor-tiered-routing.md](../../genius-conductor-tiered-routing.md) | S0–S4 routing |

## Acceptance criteria

- [ ] `python scripts/automation/audit-hierarchy-depth.py --strict --ids SEC-15-v2.22` passes
- [ ] Named script, skill, or test path exists or is listed in SEC-15 release row
- [ ] Linked from [SEC-15-v2-index](SEC-15-v2-index.md)
- [ ] `python scripts/validate-workflow.py` passes after implement

## Cross-links

- [hierarchy-expander SKILL](../../../.cursor/skills/hierarchy-expander/SKILL.md)
