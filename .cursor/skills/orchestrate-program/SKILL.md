---
name: orchestrate-program
description: >-
  Spawns parallel workers for ready program workstream lanes when manifest gate cleared.
  Use when spawn_policy allows and lanes are unblocked.
---

# Orchestrate Program

## When to use

- `mode: program`
- Manifest gate cleared
- `next_action: orchestrate-program` or conductor delegates parallel lanes

## Parallel rules

1. Read `program.spawn_policy.max_parallel` and `ready_only`.
2. Lanes: `status` in `in_progress` or `backlog`, empty `blocked_on`, no active lease.
3. Spawn one worker per lane (up to max_parallel) with WorkOrder per [orchestrate-subagents/references/work-order.md](../orchestrate-subagents/references/work-order.md).
4. `allowed_reads`: lane task card + manifest + playbooks only.
5. Merge WorkResults; update `lane.json`; do not ingest full worker context.
6. Run Verifier (shell) or `python scripts/verify-router.py` per completed task.

Conductor only updates lanes and journal/state.
