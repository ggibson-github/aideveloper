# Implement feature workflow (v2)

1. Read `journal/state.json` and `docs/tasks/task-K.md` (K from next_action).
2. Read only paths in `allowed_reads` (playbooks, facts)—not `docs/design/dd.md` unless task card links a section file.
3. Implement **one** task; do not skip ahead.
4. Set `evidence_required: true` in state when starting work.
5. Spawn **verifier** (shell subagent): run Test command from task card → `evidence/task-K-test.log`.
6. On pass: update `evidence_files`, `last_verify: passed`, `evidence_required: false`.
7. On fail: `blockers`, `last_failure`; do not advance.
8. Conductor updates journal + state; next_action → task K+1 or `done`.

Blockers, dependencies, user help: same as v1—do not skip failed downloads or credentials.
