# Autopilot workflow (local)

1. Set `journal/state.json` autopilot:
   - `active: true`
   - `max_steps_per_session` (default 25, or from `model-policy.json` autopilot block)
   - `steps_this_session: 0`
   - `stopped_reason: null`
2. Loop until blocked:
   - Run `python scripts/automation/check-pipeline-blocked.py` — exit 1 → stop with reason.
   - Execute **one** continue step (same mapping as [continue/references/workflow.md](../../continue/references/workflow.md)).
   - If `spawn_workers`: **orchestrate-subagents** or **orchestrate-program** (local economy subagents).
   - `python scripts/route-tier.py --apply`
   - Dual-write journal + state; increment `autopilot.steps_this_session`.
3. On stop:
   - `autopilot.active: false`
   - `autopilot.stopped_reason` = blocker reason
   - `last_session_summary` with steps completed
   - `python scripts/generate-dashboard.py`

Autopilot does **not** clear gates or blocking questions without explicit user approval (AGENTS.md).
