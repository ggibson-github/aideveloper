# Vision hierarchy expansion (Cursor `/loop`)

**One-off / reusable:** flesh out a hierarchy into `documents/plans/<topic>/`. Skill: [hierarchy-expander](../../.cursor/skills/hierarchy-expander/SKILL.md).

## Why a queue (not one long chat)

Option 1 (single mega-prompt) **does** lose context as the tree deepens. The **queue JSON on disk** is the source of truth: each wake reads only the next item, the vision doc section, and writes one output. Nothing important lives only in chat memory.

## Files

| File | Role |
|------|------|
| [vision-expansion-queue.json](vision-expansion-queue.json) | Work list: `expand` (add children) or `document` (write leaf) |
| [vision-expansion-prompt.md](vision-expansion-prompt.md) | Rules for each wake |
| [check-vision-expansion-queue.py](../../scripts/automation/check-vision-expansion-queue.py) | S0: `READY` / `EMPTY` / `BLOCKED` |

## Start the loop (Cursor Agent, local IDE)

1. Genius-tier model recommended (deep design).
2. Enable auto-run for terminal if you want fewer clicks.
3. Run once immediately, then on a timer:

```
/loop 3m Follow docs/automation/vision-expansion-prompt.md exactly. One queue item per wake. Run check-vision-expansion-queue.py first each time.
```

Or shorter first message + loop:

```
/loop 3m Process one pending item from docs/automation/vision-expansion-queue.json per docs/automation/vision-expansion-prompt.md
```

4. **Stop the loop** when the agent replies `VISION_EXPANSION_COMPLETE` or `check-vision-expansion-queue.py` prints `EMPTY`.

## Queue behavior

- **`expand`** — break node into child queue items (deeper hierarchy); mark self done when children cover all work.
- **`document`** — write full leaf plan to `documents/plans/full-automation/<id>-<slug>.md`.
- New items are **appended** to the queue; order is FIFO among pending items.
- Initial seed: 56 branch sub-nodes (A1–J6) + intro/roadmap/decisions/taxonomy meta items.

## Preflight

```bash
python scripts/automation/check-vision-expansion-queue.py
# READY: pending=N next=A1 action=expand
# EMPTY: vision expansion queue complete
```

## Bootstrap (unified all-branch queue)

```bash
python scripts/automation/init-hierarchy-queue.py --mode full
# 292 items, branches A–J + meta, one items[] list
```

Legacy batch (already completed for full-automation):

```bash
python scripts/automation/init-hierarchy-queue.py --mode full
python scripts/automation/generate-vision-expansion-docs.py
python scripts/automation/enrich-hierarchy-docs.py      # full expansion (detailed plans)
python scripts/automation/verify-hierarchy-expansion.py # must report ok: true
```

**Status (2026-06-28):** full-automation hierarchy **complete** — 242 leaf docs expanded, 0 scaffolds, queue EMPTY.

## Not autopilot

This does **not** use `/autopilot` or `journal/state.json`. It is documentation-only brainstorming expansion.
