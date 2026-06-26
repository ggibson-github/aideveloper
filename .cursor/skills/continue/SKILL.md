---
name: continue
description: >-
  Resumes the pipeline from journal/state.json. Use when the user says continue,
  start, resume, or runs /continue.
---

# Continue

## When to use

- User says "continue", "start", or "resume" or `/continue`
- User asks to pick up where the project left off

## Instructions

See [references/workflow.md](references/workflow.md).

**Read `journal/state.json` and `journal/progress.md`** and Context files. Hooks may inject summary; still read state yourself.

"Continue" is not approval or an answer to open questions.

Special next actions:

- `reconcile-stale` → **reconcile-stale** skill
- `wait for … approval` → re-prompt; do not advance

After one step: dual-write journal + state (journal-keeper).
