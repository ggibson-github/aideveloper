<!-- Complete pass 3 2026-06-28 H4 -->

# H4: evidence

**Parent:** — · **Branch H** · **Vision §10** · **Release:** exists

## Reader narrative
<!-- prose-source: agent plane-h 2026-06-28 -->

The `evidence/` directory holds immutable verify logs—pytest output, tool runs, checksums—written by verify-router.py or verifier shell workers before tasks complete. state.json `evidence_files` and journal Evidence files mirror paths for audit.

Non-pytest evidence types follow `docs/operator/evidence-types.md` ([I4.3](I4.3-runtime-external-evidence-types-non-pytest.md)). Evidence is append-only; failed verify retains logs for escalation ([B3.3](B3.3-escalation-loop-on-verify-fail.md)). Push and git-workflow require last_verify passed or documented journal exception per evidence-required rule.

## Purpose

H4 defines evidence for the agent-driven expert system. Persistence — journal, state.json, graphs, evidence.
## Scope

- Owns `H4` only; siblings under `—` must not duplicate this spec.
- Aligns with minimal HITL: H1 plan, H2 blocker, H3 sign-off ([INTRO-1.2](INTRO-1.2-human-touchpoint-contract-h1-h2-h3.md)).
- Conflicts resolve in favor of [Vision §10 — Branch H — Persistence & state plane](../../full-automation-vision-and-hierarchy.md#10-branch-h-persistence-state-plane).

```
├── H4. evidence/ — immutable logs per verify
```
## Behavior / step logic
<!-- timeline-source: agent cli-composer-2.5 2026-06-28 -->

1. `journal/progress.md` mirrors machine state in prose—phase completions, Resolved Q&A, Open questions, Blockers, Evidence files, Context files, Session summary, and Next action—for operators who skim without parsing state.json.
2. Only the conductor dual-writes the journal after each pipeline step via journal-keeper; workers return summaries but never edit progress.md directly.
3. The **full prompt** from the queue (with `## Your task` and `## Reader narrative`), or
4. A specific **leaf ID** (e.g. `I2.2`, `G2.4`) you want rewritten.

## JSON example

```json
{
  "node": "H4",
  "description": "evidence",
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
- Edge case `H4` variant 3: verify state dual-write before continuing pursuit.
- Edge case `H4` variant 4: verify state dual-write before continuing pursuit.
- Pass 3: add regression test or evidence path specific to `H4`.
- Pass 3: cross-link related nodes in same branch index.

## Failure modes

- **Silent stop:** Agent ends turn without updating queue â†’ mitigated by /loop + check-hierarchy-queue.py EMPTY gate.
- **False complete:** Item marked done without artifact â†’ audit-hierarchy-depth.py re-enqueues deepen pass.
- **Scope bleed:** Worker edits journal/state during planning-only expansion â†’ forbidden in vision-expansion-prompt.
- **Stale design:** Upstream vision Â§ changes â†’ reconcile-stale adds deepen items for affected ids.

## Concrete implementation

1. Map `H4` to v2.14â€“v2.23 release row in SEC-15-index.md.
2. Create or extend S0 script if behavior is file-derived.
3. Add unit test under tests/unit/test_h4.py when script exists.
4. Validate `H4` against SEC-15 release checklist and parent index links.
5. Document `H4` in parent index with verify command and release tag.
6. Add checklist row in SEC-15 release doc for `H4`.

## Verification

| Check | Command |
|-------|---------|
| Completeness | `python scripts/automation/audit-hierarchy-depth.py --strict --ids H4` |
| Conformance | `python scripts/validate-workflow.py` |
| Task evidence | `python scripts/verify-router.py` when implement task exists |

## Dependencies

| Link | Why |
|------|-----|
| [full-automation-vision-and-hierarchy.md](../../full-automation-vision-and-hierarchy.md) §10 | Master hierarchy |
| [—-index](—-index.md) | Parent grouping |
| [genius-conductor-tiered-routing.md](../../genius-conductor-tiered-routing.md) | S0–S4 routing |

## Acceptance criteria

- [ ] `python scripts/automation/audit-hierarchy-depth.py --strict --ids H4` passes
- [ ] Named script, skill, or test path exists or is listed in SEC-15 release row
- [ ] Linked from [—-index](—-index.md)
- [ ] `python scripts/validate-workflow.py` passes after implement

## Cross-links

- [hierarchy-expander SKILL](../../../.cursor/skills/hierarchy-expander/SKILL.md)
