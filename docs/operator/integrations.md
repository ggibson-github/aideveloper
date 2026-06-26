# Runtime integrations (v2 bridge)

AIDeveloper v2 is **Cursor-first, local by default**. Use this doc to connect external runtimes without duplicating the SDLC harness.

## Local autopilot (v2.13)

Primary path on your PC — no Cloud Agents:

1. `/autopilot` or **autopilot** in Cursor (genius-tier conductor + local subagents until gate).
2. `python scripts/automation/check-pipeline-blocked.py` — S0 pre-flight.
3. Optional: `python scripts/automation/run-local-pipeline.py` (cursor-sdk local runtime).

See `docs/automation/README.md`.

## OpenClaw / ClawRecipes

1. Export `journal/state.json` as ticket context.
2. Map `next_action` to ClawRecipes lanes: backlog → in-progress → testing → done.
3. Run `python scripts/headless-verify.py` in **testing** lane.
4. Commit evidence logs; human gate approvals stay in journal `gates_pending`.

## Hermes cron

1. Schedule `python scripts/validate-workflow.py` on PR.
2. Schedule `python scripts/headless-verify.py` when `next_action` matches `implement-feature`.
3. Schedule `python scripts/pull-ready-work-orders.py` for program lane workers.
4. Hermes FTS memory is optional; prefer `docs/playbooks/` for repo-scoped patterns.

## One chat per workstream (v2.11)

1. Conductor sets `lane.current_task` and optional lease in `program/workstreams/<id>/lane.json`.
2. Open dedicated chat; `/lane <id>` loads lane + work order only.
3. Worker completes task; writes evidence; runs `complete-work-order.py`.
4. Conductor chat `/program` merges integration steps.

## GitHub Actions

See `.github/workflows/validate-workflow.yml` and `verify-on-schedule.yml`.

## Cursor Automations / SDK

See `docs/automation/README.md` for **local** autopilot. Cloud Agents are optional, not required.

## Do not

- Let headless workers edit `gates_pending` without human approval strings in journal.
- Replace `journal/state.json` with external DB without dual-write to `progress.md`.
- Let two workers hold the same lane lease.
