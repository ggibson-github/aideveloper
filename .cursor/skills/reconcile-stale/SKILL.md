---
name: reconcile-stale
description: >-
  When docs/manifest/staleness.json marks artifacts stale, plans re-run or user
  approval. Use when next_action is reconcile-stale or spec/design changed.
---

# Reconcile Stale

## When to use

- `next_action` is `reconcile-stale` or `run reconcile-stale`
- `docs/manifest/staleness.json` has entries with `stale: true`
- User changed spec or design upstream artifacts

## Instructions

1. Read `docs/manifest/staleness.json` and `journal/state.json`.
2. Run `python scripts/update-staleness.py` to refresh stale flags from mtimes.
2. List stale nodes (spec → requirements → hld → dd → tasks → src/tests).
3. Ask user: re-run from first stale phase (e.g. hld-writer) or waive and mark fresh.
4. Set `next_action` to the appropriate phase skill; update `allowed_reads`.
5. Clear stale flags only after re-run or explicit user waiver recorded in journal.
