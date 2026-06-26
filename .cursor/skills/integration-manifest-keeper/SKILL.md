---
name: integration-manifest-keeper
description: >-
  Drafts and updates program/integration/manifest.md; human gate before parallel work.
  Use after milestone approved in program mode.
---

# Integration Manifest Keeper

## When to use

- After milestone gate cleared
- `next_action: run integration-manifest-keeper`

## Instructions

1. Read workstream scopes and spec; draft `program/integration/manifest.md`.
2. Cite template pack manifest sections if `template-packs/<pack>/manifest.md` exists.
3. Set `next_action: wait for manifest approval` until user approves or waives.
4. On approval: clear `manifest_approved` from `gates_pending_program`; unblock lanes that depended on manifest.
5. Run `python scripts/update-staleness.py` on program artifact graph if needed.

Workers implementing tasks must cite manifest section in work results.
