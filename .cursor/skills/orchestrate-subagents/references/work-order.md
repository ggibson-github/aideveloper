# Work order schema (v2.4+)

Conductor issues work orders to subagents. Workers return **work results** only.

## WorkOrder

| Field | Required | Description |
|-------|----------|-------------|
| `id` | yes | Unique id (e.g. `wo-2026-001`) |
| `role` | yes | `librarian`, `phase_worker`, `verifier`, `reviewer`, `tool_operator` |
| `task_ref` | no | `docs/tasks/task-NNN.md` or program lane task path |
| `allowed_reads` | yes | Max ~8 paths from `state.json`; workers must not expand |
| `forbidden_reads` | no | From `state.json` |
| `instructions` | yes | Bounded task; cite manifest section if program mode |
| `model_tier` | no | From `subagent_models` in policy |
| `writes` | yes | Explicit write allowlist (e.g. `evidence/*.log`, `src/...`) |

## WorkResult

| Field | Required | Description |
|-------|----------|-------------|
| `work_order_id` | yes | Matches WorkOrder.id |
| `status` | yes | `completed`, `failed`, `blocked` |
| `summary` | yes | Short merge text for conductor (not full file dumps) |
| `artifacts` | no | Paths created or modified |
| `evidence` | no | Paths under `evidence/` |
| `blocked_reason` | no | If status is blocked |

Workers **must not** update `journal/state.json`, `next_action`, `gates_pending`, or lane files.

Conductor appends optional audit line to `program/worker-runs.jsonl`:

```json
{"ts":"ISO8601","work_order_id":"...","role":"...","status":"completed"}
```
