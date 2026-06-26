# Local automation (v2.13)

Run the SDLC pipeline on **your PC** without clicking Continue for every phase.

## Primary: in-IDE autopilot

1. Open project in Cursor.
2. Select a **genius-tier** orchestration model ([`model-policy.json`](../operator/model-policy.json) → `tiers.genius.cursor_models`).
3. Say **autopilot** or run **`/autopilot`**.

The conductor loops **continue** steps until a gate, blocker, evidence wait, or max steps. It spawns **local subagents** when `spawn_workers` is true.

Pre-flight (no LLM):

```bash
python scripts/automation/check-pipeline-blocked.py
```

## Optional: SDK loop (local runtime)

Same machine, terminal-driven loop — **not** Cloud Agents:

```bash
pip install cursor-sdk
# set CURSOR_API_KEY and optional AUTOPILOT_MODEL (genius-tier id from policy)
python scripts/automation/run-local-pipeline.py
python scripts/automation/run-local-pipeline.py --dry-run
```

Prompt: [`local-autopilot-prompt.md`](local-autopilot-prompt.md)

## Files

| File | Role |
|------|------|
| [`local-autopilot-prompt.md`](local-autopilot-prompt.md) | Stable prompt for SDK + skill |
| [`check-pipeline-blocked.py`](../../scripts/automation/check-pipeline-blocked.py) | S0 ready/blocked check |
| [`run-local-pipeline.py`](../../scripts/automation/run-local-pipeline.py) | Local SDK loop |
| [`release-queue.json`](release-queue.json) | Template **release** evolution only (not consumer pipeline) |
| [`unattended-prompt.md`](unattended-prompt.md) | Release-queue slice prompt |
| [`../decisions/automation-waivers.md`](../decisions/automation-waivers.md) | Gate waiver for template self-build only |

## Release queue (separate)

`run-next-release.py` lists the next pending **template release** from `release-queue.json`. For day-to-day project pipeline, use autopilot above.

## CI

`.github/workflows/validate-workflow.yml` runs `validate-workflow.py`, `route-tier --check`, `check-pipeline-blocked.py`, and unit tests.

## Cloud Agents (optional, not default)

Cursor Cloud Agents or Automations can run remotely if you choose; this template defaults to **local** Composer + subagents. See Cursor docs if you want that path.
