# V2 Implementation Plan — Master Plan

**Status:** Authoritative implementation plan
**Created:** 2026-06-28
**Owner:** Conductor (genius-tier) + operator
**Source of truth for vision:** [`documents/full-automation-vision-and-hierarchy.md`](../documents/full-automation-vision-and-hierarchy.md) (north star) and **281 spec leaves** + H3-SIGNOFF under [`documents/plans/full-automation/`](../documents/plans/full-automation/) (348 files in [08-coverage-ledger.md](08-coverage-ledger.md))

---

## What this is

This folder refactors **all** of the brainstorming documents (the full-automation vision, the 281-leaf hierarchy, the transistor model, and the v2 evolution notes) into **one comprehensive, executable plan** that evolves the existing AI-developer expert system from its current shipped state (**v2.13**) into the full vision (**v2.28**).

It is written so that an agent (or a human) can implement it **release by release**, then use the **[Master Checklist](06-MASTER-CHECKLIST.md)** as a TODO manifest to confirm that **every detail of the vision has been implemented and verified** — checking off items as work completes.

## The deliverable the agent follows

> **[06-MASTER-CHECKLIST.md](06-MASTER-CHECKLIST.md)** is the work manifest.
> Every vision detail is a checkbox with an owning release, concrete repo artifact, and a verification command.
> Nothing is "done" until its checkbox passes its acceptance gate.

---

## Document map (read in this order)

| # | Document | Purpose |
|---|----------|---------|
| 0 | [00-vision-and-scope.md](00-vision-and-scope.md) | Distilled north star: four structural shifts, HITL contract (H1/H2/H3), goal-completion criterion, scope in/out. |
| 1 | [01-current-state-baseline.md](01-current-state-baseline.md) | Exact inventory of what already exists at v2.13 (scripts, skills, commands, rules, state, packs, tests). |
| 2 | [02-gap-analysis.md](02-gap-analysis.md) | Vision − baseline = remaining work, by plane and by release. |
| 3 | [03-target-architecture.md](03-target-architecture.md) | Target `state.json` schema, transistor/workflow model, pack schema, catalog, directory layout. |
| 4 | [04-release-roadmap.md](04-release-roadmap.md) | v2.14 → v2.28 sequenced with dependencies, per-release deliverables and exit gates. |
| 5 | [05-workstreams-by-plane.md](05-workstreams-by-plane.md) | Per-plane (A–J + transistor model) concrete repo changes mapped from each leaf group. |
| 6 | [06-MASTER-CHECKLIST.md](06-MASTER-CHECKLIST.md) | **The work manifest** — every detail as a verifiable checkbox grouped by release. |
| 7 | [07-traceability-matrix.md](07-traceability-matrix.md) | Leaf ID → release → checklist item. Proves every spec leaf is covered. |
| 8 | [08-coverage-ledger.md](08-coverage-ledger.md) | File-by-file checkoff vs `documents/**/*.md` (348 files). |
| 9 | [09-architectural-supplements.md](09-architectural-supplements.md) | Post-review cross-cuts: ADR index, CI matrix pointer, capability-debt window. |

---

## How to execute this plan

1. **One release at a time, in order.** Releases are additive and dependency-ordered (see [04](04-release-roadmap.md)). Do not start v2.N+1 until v2.N's exit gate is green.
2. **Schema is additive.** `journal/state.json` stays `version: 2`. New blocks (`goal`, `pursuit`, `platform`, `company`, `hitl`, `active_workflow`) are added, never breaking existing fields. See [03](03-target-architecture.md).
3. **Generator-first.** After v2.25, deliverables come from workflow DAG terminal nodes — not direct inline implement. See [03 §5](03-target-architecture.md) and [ADR-V2-007](../docs/decisions/v2-evolution-policy-adrs.md).
4. **Every new script gets a unit test** under `tests/unit/`, and integration/e2e where the feature spans phases.
5. **Verify before check-off.** Each checklist item names a command; run it, capture evidence, then tick the box. Honor the repo rules: `evidence-required`, `test-before-push`, `deterministic-first`.
6. **Update the journal each step** (`journal/progress.md` + `journal/state.json`) — conductor dual-writes; workers return summaries only.
7. **Run conformance after each release:** `python scripts/validate-workflow.py` and the full test suite must pass before tagging.

## Conventions

- **Leaf IDs** (e.g. `A2.4`, `E6.2`, `SEC-15-v2.16`) refer to the expanded plan docs under `documents/plans/full-automation/`. They are cited so every checklist item is traceable back to the brainstorm.
- **Levels L0–L6** are the promotion/reuse-maturity ladder (L0 ephemeral → L6 transistor).
- **Planes A–J** are the ten top-level branches of the vision; the transistor model (§19) threads across B6, C6, D1.7, E6, E7, etc.
- **HITL points** are exactly three: H1 (initial plan), H2 (blocker), H3 (final sign-off).
