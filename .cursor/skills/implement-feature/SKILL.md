---
name: implement-feature
description: >-
  Implements one task from TODOS using task cards and evidence (v2). Use when
  next action is implement-feature (task K/N).
---

# Implement Feature

## When to use

- Journal/state `next_action` is `implement-feature (task K/N)`
- Pipeline is in implementation phase

## Instructions

See [references/workflow.md](references/workflow.md) for full steps.

**Read first:** `journal/state.json`, `docs/tasks/task-K.md` only—not full DD.

1. Run **verifier** before marking task complete (`evidence_required` → evidence log).
2. Conductor dual-writes journal + state; set `evidence_required: true` when starting task.
3. On success: `last_verify: passed`, advance to next task or `done`.
4. Optional: **playbook-keeper** after repeatable patterns.
