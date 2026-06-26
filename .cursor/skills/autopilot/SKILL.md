---
name: autopilot
description: >-
  Run the pipeline locally until blocked: repeated continue steps in one session
  with Genius-tier conductor spawning subagents. Use for /autopilot or run until gate.
---

# Autopilot (local run-until-blocked)

## When to use

- User says **autopilot**, **run until blocked**, or `/autopilot`
- Local full pipeline without clicking Continue for each phase
- **Not** Cloud Agents — runs in this Cursor session (or local SDK script)

## Operator setup

1. Select a **genius-tier** orchestration model in Composer (`docs/operator/model-policy.json` → `tiers.genius.cursor_models`; update as better models ship).
2. Enable auto-run for terminal/tools if you want fewer approval clicks.

## Instructions

See [references/workflow.md](references/workflow.md).

While `autopilot.active` is true, **override** one-step-per-turn from conductor rule.

## SDK alternative

```bash
python scripts/automation/run-local-pipeline.py
```

Requires `cursor-sdk` + `CURSOR_API_KEY`, local runtime on this PC.
