---
name: playbook-keeper
description: >-
  Distills repo-scoped playbooks after features complete. Updates docs/playbooks/
  INDEX.md. Use when a feature or task pattern should be reused.
---

# Playbook Keeper

## When to use

- Feature or implement task completed successfully
- User asks to capture "how we do X in this repo"
- Librarian should prefer playbooks over raw DD for implement tasks

## Instructions

1. Review what was done (task card, diff, evidence log).
2. Write `docs/playbooks/<slug>.md`: context, steps, files touched, test command, pitfalls.
3. Update `docs/playbooks/INDEX.md` with topic, file, keywords.
4. Optionally add playbook path to default `allowed_reads` for similar future tasks.

Human-reviewable learning—not silent global memory.
