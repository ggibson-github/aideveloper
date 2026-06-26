# Export contract (v2)

Headless workers (GitHub Actions, OpenClaw, Hermes cron) read **machine state** from the repo—not full markdown forests.

## Canonical files

| File | Role |
|------|------|
| `journal/state.json` | Router: `next_action`, `allowed_reads`, gates, evidence, tier fields, `program` |
| `journal/progress.md` | Human-readable mirror |
| `evidence/*.log` | Verify output |
| `docs/tasks/task-NNN.md` | Task test commands |
| `program/workstreams/*/lane.json` | Per-stream lane + lease (v2.11) |

## state.json schema (v2)

Required keys: `version` (2), `next_action`, `phase`, `mode`, `completion_status`, `allowed_reads`, `evidence_required`, `last_verify`.

Optional (v2.4+): `capability_class`, `model_tier`, `spawn_workers`, `subagent_models`, `model_escalation`, `genius_session_recommended`, `pipeline_id`, `program`, `autopilot`.

## Local autopilot (v2.13)

```bash
python scripts/automation/check-pipeline-blocked.py
python scripts/automation/run-local-pipeline.py --dry-run
```

In-IDE: `/autopilot`. See `docs/automation/README.md`.

## Headless verify

```bash
python scripts/headless-verify.py
# or
python scripts/verify-router.py [task-card-path]
```

## Lane protocol (v2.11)

```bash
python scripts/pull-ready-work-orders.py
python scripts/complete-work-order.py <workstream> --evidence evidence/task-NNN-test.log --status verify
```

Lane `lease`: `{ "holder", "expires_at", "work_order_path" }` — external chats must release via complete-work-order.

## Environment

- `WORKSPACE_ROOT`: project root (default: cwd)
- Python 3 on PATH for scripts and hooks

## Push gate

External automation should not push if `last_verify` is not `passed` unless journal documents an exception.

## Model routing

```bash
python scripts/route-tier.py --apply
python scripts/route-tier.py --check
```

Policy: [model-policy.json](model-policy.json). Design: [genius-conductor-tiered-routing.md](../../documents/genius-conductor-tiered-routing.md).
