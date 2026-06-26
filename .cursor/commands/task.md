---
description: Scoped implement for task N from task card
---

Read `journal/state.json`. If `next_action` is implement-feature, read only `docs/tasks/task-{N}.md` and paths in `allowed_reads`. Spawn **verifier** after implementation. Update evidence before marking complete.

Replace `{N}` with the task number from user message or current next_action.
