# Hierarchy expansion — one item per wake

**One unified queue for the entire hierarchy** — branches A through J, intro, and meta sections all live in a **single** `items[]` list. The loop walks FIFO across branch boundaries until **every** item is done.

## Single unified queue (required)

- **ONE** queue file per hierarchy (e.g. `vision-expansion-queue.json`).
- **Never** split branches into separate queues (no `queue-A.json`, `queue-B.json`, …).
- Process the **first pending item** regardless of branch — after `A6` comes `B1` automatically.
- Append new child items to the **same** queue's `items[]` end.
- **Complete** only when checker prints `EMPTY` (all branches done).

Initialize a fresh unified queue:

```bash
python scripts/automation/init-hierarchy-queue.py --mode full
```

## Each wake (process exactly ONE queue item)

1. Run `python scripts/automation/check-hierarchy-queue.py --queue docs/automation/vision-expansion-queue.json`   - If output is `EMPTY` → reply **HIERARCHY_EXPANSION_COMPLETE** (or legacy `VISION_EXPANSION_COMPLETE`) and **do not** schedule further work.
2. Read `docs/automation/vision-expansion-queue.json`.
3. Take the **first** item with `"status": "pending"` (queue order matters).
4. Read the matching section in `documents/full-automation-vision-and-hierarchy.md` (use `source_section` / `id` / `title`).
5. Perform the item's `"action"`:

### action: `expand`

The node is not fully broken down yet.

- Decide if this node needs **child nodes** in the hierarchy (deeper breakdown).
- If yes: append new items to the **end** of `items[]` with unique ids (e.g. `A1.1`, `A1.2`), `"action": "expand"` or `"document"` as appropriate, `"status": "pending"`, `"parent": "<current id>"`.
- If the node is now fully decomposed (all future work is in child queue items): set this item `"status": "done"`.
- Optionally write a short index stub at `documents/plans/full-automation/<id>-index.md` listing children (links only).

### action: `document`

The node is a **leaf** — write the full design doc.

- Write `documents/plans/full-automation/<id>-<slug>.md` (use `output` path if set, else derive from id + title).
- Include: purpose, scope, behavior/step logic, data/state fields, artifacts to create, dependencies on other nodes, acceptance criteria, open questions (deferred — do not block).
- Cross-link to parent and related nodes.
- Set item `"status": "done"` and `"completed_at": "<ISO date>"`.

6. Save the updated queue JSON.
7. End turn. **Do not** process a second item in the same wake (the `/loop` timer fires the next wake).

## Stop conditions

| Condition | Action |
|-----------|--------|
| No pending items | Reply `HIERARCHY_EXPANSION_COMPLETE` |
| Need external fact/access only user can provide | Set item `"status": "blocked"`, `"blocker": "..."`, stop |
| Unrecoverable error on one item | Set `"status": "failed"`, `"error": "..."`, continue on next wake unless user says stop |

## Do NOT

- Touch `journal/state.json` or consumer SDLC pipeline
- Ask the user to say "continue" between items
- Process multiple queue items in one wake
- Remove or reorder pending items (only append children, mark done/blocked/failed)
- **Create separate queues per branch** — one queue holds the full hierarchy

## Output directory

All leaf docs: `documents/plans/full-automation/`

When complete, append a row to `documents/plans/full-automation/INDEX.md` for each finished doc.
