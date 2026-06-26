---
name: orchestrate-subagents
description: >-
  Spawns role-based subagents (Librarian, phase worker, Verifier, Reviewer) with
  contracts. Use when the conductor needs bounded context or parallel readonly work.
---

# Orchestrate Subagents

## When to use

- Conductor needs codebase search without loading full design docs
- Implement task needs tests run in shell subagent
- Pre-PR review (bugbot / security-review subagents)

## Roles

| Role | Subagent type | readonly | Writes | Reads |
|------|---------------|----------|--------|-------|
| Librarian | explore | yes | nothing | `journal/state.json` only |
| Phase worker | generalPurpose | no | phase artifact only | `allowed_reads` from state |
| Verifier | shell | no | `evidence/*.log` only | task card test command |
| Reviewer | bugbot / security-review | yes | review notes file | git diff |

## Workflow

1. Read `journal/state.json`
2. Spawn **Librarian** first if `allowed_reads` is empty or scope unclear
3. Spawn worker with prompt: role + allowed_reads + "do not edit journal/state"
4. Merge worker output; **conductor** dual-writes journal + state
5. Never let workers update `next_action` or gates

See **librarian** and **verifier** skills for prompts.
