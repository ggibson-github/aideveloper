---
name: generate-dashboard
description: >-
  Regenerates docs/operator/dashboard.md and STATUS.md from state.json and
  staleness manifest. Use at session end with journal-keeper.
---

# Generate Dashboard

## When to use

- Session end (with journal-keeper)
- After gate/blocker/stale status changes
- User runs `/status`

## Instructions

Run `python scripts/generate-dashboard.py` from project root.

Or manually refresh `docs/operator/dashboard.md` from `journal/state.json`, `docs/manifest/staleness.json`, and journal blockers.
