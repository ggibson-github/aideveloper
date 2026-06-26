---
name: verifier
description: >-
  Runs test command from task card via shell subagent; writes evidence log and
  sets last_verify in state. Use before marking implement tasks complete or before push.
---

# Verifier

## When to use

- After implement-feature for current task
- User runs `/verify` or git-workflow before push
- `evidence_required` is true in state.json

## Instructions

1. Read `journal/state.json` and current task card `docs/tasks/task-NNN.md` (from next_action).
2. Extract **Test command** from task card (or use project default from TODOS if no card yet).
3. Spawn **shell** subagent to run the command; capture full output.
4. Write log to `evidence/task-NNN-test.log` (create `evidence/` if needed).
5. Conductor updates state:
   - `evidence_files`: include log path
   - `last_verify`: `passed` or `failed`
   - `evidence_required`: false on pass
6. Update journal **Evidence files** field.
7. On failure: set `blockers`, `last_failure`, do not advance next_action.
