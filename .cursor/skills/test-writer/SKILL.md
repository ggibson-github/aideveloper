---
name: test-writer
description: >-
  Adds or runs tests for implemented code. Use when a feature is implemented and
  tests must pass before marking the task complete.
---

# Test Writer

## When to use

- A feature has been implemented and tests need to be run or added before marking the task complete
- Journal indicates current task requires test verification

## Instructions

1. Identify the current task from `journal/progress.md` and `TODOS.md`.
2. Run existing tests or add tests for the current task as appropriate.
3. If tests fail: do not mark the task complete; set **Blockers** in the journal (e.g. `build_failed: tests failing for task K`). Surface the failure to the user.
4. If tests pass: allow implement-feature or journal-keeper to mark the task complete and advance next action.
