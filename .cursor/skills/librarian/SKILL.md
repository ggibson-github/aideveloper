---
name: librarian
description: >-
  Readonly briefing from journal/state.json only — returns allowed_reads (max 5),
  forbidden paths, and suggested worker. Use before opening design docs or code search.
---

# Librarian

## When to use

- Before reading `docs/design/` or large code areas
- Conductor needs routing for current `next_action`
- User runs `/research` or implement scope is unclear

## Instructions

Spawn **explore** subagent with `readonly: true`. Worker prompt:

```
You are the Librarian. Read ONLY journal/state.json (and STATUS.md if needed).
Do NOT read docs/design/ or src/ unless listed in allowed_reads.

Return markdown:
1. allowed_reads (max 5 paths) for the current next_action
2. forbidden_reads (what to skip)
3. suggested_worker: librarian | phase_worker | verifier | reviewer | none
4. one-paragraph briefing for the conductor
```

Conductor updates `allowed_reads` in state.json to match Librarian output (max 5), then proceeds.
