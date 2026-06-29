<!-- Complete pass 3 2026-06-28 H2 -->

# H2: journal progress

**Parent:** — · **Branch H** · **Vision §10** · **Release:** cross-cutting

## Reader narrative
<!-- prose-source: agent plane-h 2026-06-28 -->

`journal/progress.md` is the human-readable mirror of machine state—not a second router. It records phase completions, Resolved Q&A, Open questions, Blockers, Evidence files, Context files, Session summary, and Next action in prose operators can skim without parsing JSON.

Only the conductor dual-writes after each pipeline step via journal-keeper; workers return summaries but never edit the journal. Hooks inject journal summary on continue/start ([I1.4](I1.4-runtime-ide-hooks-beforesubmit-subagentstart-pretooluse-prec.md)) but agents must still read the full file. STATUS.md and dashboard.md are generated views ([I5.1](I5.1-runtime-notify-status-dashboard-generation.md)), not authoritative pursuit state.

## Purpose

H2 defines journal progress for the agent-driven expert system. Persistence — journal, state.json, graphs, evidence.
## Scope

- Owns `H2` only; siblings under `—` must not duplicate this spec.
- Aligns with minimal HITL: H1 plan, H2 blocker, H3 sign-off ([INTRO-1.2](INTRO-1.2-human-touchpoint-contract-h1-h2-h3.md)).
- Conflicts resolve in favor of [Vision §10 — Branch H — Persistence & state plane](../../full-automation-vision-and-hierarchy.md#10-branch-h-persistence-state-plane).

```
│   ├── A4.1 human: H1 | H2 | H3
├── A6.2 digest on blocker (H2) not on every step
│   └── B1.5 S4 governance / escalation / H2 packaging
│   ├── D3.4 idle drain: when product waits on external H2
├── G6.2 journal last_failure + structured blocker for H2
│   ├── H1.5 hitl: { pending: H1|H2|H3|null, since, payload }
├── H2. journal/progress.md — human mirror + session summary
└── I5.2 optional webhook/email on H2/H3 only
```
## Behavior / step logic
<!-- timeline-source: agent cursor-agent 2026-06-28 -->

1. After each pipeline step completes, journal-keeper dual-writes journal/progress.md and journal/state.json so the human mirror and machine router stay aligned—workers return summaries only and never edit the journal directly.
2. The conductor records phase completions, Resolved Q&A, Open questions, Blockers, Evidence files, Context files, Session summary, and Next action in prose operators can skim without parsing JSON.
3. On continue/start, [I1.4](I1.4-runtime-ide-hooks-beforesubmit-subagentstart-pretooluse-prec.md) hooks may inject a journal excerpt into the prompt, but pursuit agents must still read the full progress.md before routing—the hook is a pointer, not a substitute.
4. [I5.1](I5.1-runtime-notify-status-dashboard-generation.md) regenerates STATUS.md and docs/operator/dashboard.md as derived views; preflight treats state.json next_action as authoritative when mirror and router disagree.
5. If dual-write fails or journal fields drift from state.json—missing Next action, stale Blockers—integrity stop fires at H2 and pursuit halts until validate-workflow or manual reconciliation restores a single source of truth.

## JSON example

```json
{
  "node": "H2",
  "description": "journal progress",
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
- Edge case `H2` variant 3: verify state dual-write before continuing pursuit.
- Edge case `H2` variant 4: verify state dual-write before continuing pursuit.
- Pass 3: add regression test or evidence path specific to `H2`.
- Pass 3: cross-link related nodes in same branch index.

## Failure modes

- **Silent stop:** Agent ends turn without updating queue â†’ mitigated by /loop + check-hierarchy-queue.py EMPTY gate.
- **False complete:** Item marked done without artifact â†’ audit-hierarchy-depth.py re-enqueues deepen pass.
- **Scope bleed:** Worker edits journal/state during planning-only expansion â†’ forbidden in vision-expansion-prompt.
- **Stale design:** Upstream vision Â§ changes â†’ reconcile-stale adds deepen items for affected ids.

## Concrete implementation

1. Map `H2` to v2.14â€“v2.23 release row in SEC-15-index.md.
2. Create or extend S0 script if behavior is file-derived.
3. Add unit test under tests/unit/test_h2.py when script exists.
4. Validate `H2` against SEC-15 release checklist and parent index links.
5. Document `H2` in parent index with verify command and release tag.
6. Add checklist row in SEC-15 release doc for `H2`.

## Verification

| Check | Command |
|-------|---------|
| Completeness | `python scripts/automation/audit-hierarchy-depth.py --strict --ids H2` |
| Conformance | `python scripts/validate-workflow.py` |
| Task evidence | `python scripts/verify-router.py` when implement task exists |

## Dependencies

| Link | Why |
|------|-----|
| [full-automation-vision-and-hierarchy.md](../../full-automation-vision-and-hierarchy.md) §10 | Master hierarchy |
| [—-index](—-index.md) | Parent grouping |
| [genius-conductor-tiered-routing.md](../../genius-conductor-tiered-routing.md) | S0–S4 routing |

## Acceptance criteria

- [ ] `python scripts/automation/audit-hierarchy-depth.py --strict --ids H2` passes
- [ ] Named script, skill, or test path exists or is listed in SEC-15 release row
- [ ] Linked from [—-index](—-index.md)
- [ ] `python scripts/validate-workflow.py` passes after implement

## Cross-links

- [hierarchy-expander SKILL](../../../.cursor/skills/hierarchy-expander/SKILL.md)
