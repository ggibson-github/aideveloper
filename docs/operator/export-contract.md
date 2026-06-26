# Export contract (v2)

Headless workers (GitHub Actions, OpenClaw, Hermes cron) read **machine state** from the repo—not full markdown forests.

## Canonical files

| File | Role |
|------|------|
| `journal/state.json` | Router: `next_action`, `allowed_reads`, gates, evidence |
| `journal/progress.md` | Human-readable mirror |
| `evidence/*.log` | Verify output |
| `docs/tasks/task-NNN.md` | Task test commands |

## state.json schema (v2)

Required keys: `version` (2), `next_action`, `phase`, `mode`, `completion_status`, `allowed_reads`, `evidence_required`, `last_verify`.

See [journal/state.json](../../journal/state.json) for live example.

## Headless verify

```bash
python scripts/headless-verify.py
```

Reads current implement task card, runs Test command, writes `evidence/`.

## Environment

- `WORKSPACE_ROOT`: project root (default: cwd)
- Python 3 on PATH for scripts and hooks

## Push gate

External automation should not push if `last_verify` is not `passed` unless journal documents an exception.
