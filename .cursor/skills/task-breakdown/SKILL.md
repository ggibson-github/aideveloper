---
name: task-breakdown
description: >-
  Breaks the design into phased tasks, task cards, and TODOS. Use when diagrams
  are done and before scaffolding.
---

# Task Breakdown

## When to use

- Journal says next action is "run task-breakdown" (after diagram-generator)
- User asks for a task list or backlog from the design

## Instructions

See [references/workflow.md](references/workflow.md) for the full workflow.

**Read first:** `journal/state.json`, `docs/design/dd/` (or split files), `docs/design/hld.md`.

**v2 outputs:**

1. `TODOS.md` — ordered list with dependencies
2. `docs/tasks/task-001.md` … one card per implement task (template in `docs/tasks/README.md`)
3. Update `docs/manifest/staleness.json` task nodes
4. Dual-write journal + state; `next_action` → `run scaffold-project`
5. Set `allowed_reads` for scaffold phase

Always include environment-setup tasks before package installs (see workflow reference).
