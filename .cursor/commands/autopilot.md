# Autopilot (/autopilot)

**Local run-until-blocked** — run the pipeline in this session without clicking Continue for each step.

1. Select a **genius-tier** orchestration model in Composer ([`model-policy.json`](docs/operator/model-policy.json) — not a fixed model name).
2. Say **autopilot** or run this command.

The conductor will:

- Repeat **continue** steps until a gate, blocker, evidence wait, or max steps
- Spawn **local subagents** when `spawn_workers` is true
- Stop and set `autopilot.stopped_reason`

Pre-flight (no LLM):

```bash
python scripts/automation/check-pipeline-blocked.py
```

Optional SDK loop on your PC:

```bash
pip install cursor-sdk
# set CURSOR_API_KEY
python scripts/automation/run-local-pipeline.py
```

See `.cursor/skills/autopilot/SKILL.md` and `docs/automation/README.md`.
