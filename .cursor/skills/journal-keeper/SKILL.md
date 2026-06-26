---
name: journal-keeper
description: >-
  Updates journal/progress.md and journal/state.json after each phase or when
  the user answers a question. Use after every phase completion and whenever
  a decision is recorded.
---

# Journal Keeper

## When to use

- After every phase completion (spec-parser, hld-writer, dd-writer, diagram-generator, task-breakdown, scaffold-project, implement-feature)
- Whenever the user answers a blocking or deferred question (record in same response)
- At session end (write Last session summary; refresh dashboard)

## Instructions

1. **Dual-write every update:**
   - Human journal: `journal/progress.md`
   - Machine router: `journal/state.json` (v2 canonical fields below)

2. **state.json fields** (keep in sync with progress.md):
   - `spec_file`, `spec_version`, `mode`, `phase`, `feature_id`, `repo_url`, `current_branch`
   - `last_completed`, `next_action`, `context_files` (array), `allowed_reads` (array, max ~8 paths), `forbidden_reads` (array)
   - `gates_pending`, `blocking_questions`, `deferred_questions`, `resolved_qa_archive`
   - `blockers`, `pause_reason`, `last_failure`, `completion_status`
   - `evidence_required`, `evidence_files`, `last_verify` (`passed` | `failed` | null)
   - `last_session_summary`

3. **allowed_reads:** Set per `next_action`. Examples:
   - `run spec-parser`: `spec.md`, `journal/*`, `docs/facts/INDEX.md`
   - `run hld-writer`: add `docs/design/requirements-summary.md`
   - `implement-feature (task K/N)`: add `docs/tasks/task-K.md`, playbooks, facts—not full DD unless task card links a section

4. **Archive long Resolved Q&A** to `docs/decisions/archive.md` with date; keep journal pointer only.

5. After each phase: phase completed, artifacts, next action, update `allowed_reads`. Do not mark complete if blocking questions remain.

6. When setting implement/design steps: populate `context_files` and matching `allowed_reads`.

7. **Evidence:** When a task is verified, set `evidence_files`, `last_verify: passed`, clear `evidence_required`. Before advancing past a verified task, require evidence when `evidence_required` is true.

8. Session end: `last_session_summary`; run **generate-dashboard** skill or `python scripts/generate-dashboard.py`; refresh `STATUS.md`.

9. If md/json drift: run `python scripts/sync-state.py`.
