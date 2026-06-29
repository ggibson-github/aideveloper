# Hierarchy expansion — one item per wake

**One unified queue for the entire hierarchy.** All branches (A–J + meta) live in a **single** `items[]` list—not separate queues per branch.

## Single unified queue (required)

- ONE queue file; never `queue-A.json` / `queue-B.json`.
- Process the **first pending** item regardless of branch.
- Append new children to the **same** queue.
- **Complete** only when checker prints `EMPTY` (all branches done).

Initialize: `python scripts/automation/hierarchy-expander-run.py --topic <TOPIC> init`

Or legacy: `python scripts/automation/init-hierarchy-queue.py --queue <QUEUE_PATH> --mode full`

## Each wake (process exactly ONE queue item)

1. Run `python scripts/automation/check-hierarchy-queue.py --queue <QUEUE_PATH>`
   - If output is `EMPTY` → reply **HIERARCHY_EXPANSION_COMPLETE** and stop.
2. Read the queue JSON at `<QUEUE_PATH>`.
3. Take the **first** item with `"status": "pending"`.
4. Read the matching section in the hierarchy doc (`source` field in queue).
5. Perform the item `"action"`:

### action: `expand`

- Append child items to the **end** of `items[]` with unique ids, `"parent": "<current id>"`.
- Use `"action": "expand"` for nodes that need further breakdown; `"document"` for leaves.
- Mark current item `"status": "done"` and `"completed_at": "<ISO date>"` when children cover all work.
- Optionally write `<output_dir>/<id>-index.md` linking children.

### action: `document`

- Write the leaf doc (use `output` path or `<output_dir>/<id>-<slug>.md`).
- Include: purpose, scope, behavior/step logic, data fields, artifacts, dependencies, acceptance criteria, deferred open questions.
- Mark `"status": "done"` and update `<output_dir>/INDEX.md`.

6. Save queue JSON. **One item per wake** when using Cursor `/loop`.

## Stop conditions

| Condition | Action |
|-----------|--------|
| No pending items | `HIERARCHY_EXPANSION_COMPLETE` |
| User-only blocker | `"status": "blocked"`, `"blocker": "..."` |
| Recoverable error | `"status": "failed"`, `"error": "..."` |

## Do NOT

- Use `journal/state.json` or SDLC `/autopilot` unless explicitly scoped
- Ask the user to say "continue" between items in loop mode
- Process multiple queue items in one wake (loop mode)
- **Create separate queues per branch**
