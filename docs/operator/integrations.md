# Runtime integrations (v2 bridge)

AIDeveloper v2 is **Cursor-first**. Use this doc to connect external runtimes without duplicating the SDLC harness.

## OpenClaw / ClawRecipes

1. Export `journal/state.json` as ticket context.
2. Map `next_action` to ClawRecipes lanes: backlog → in-progress → testing → done.
3. Run `python scripts/headless-verify.py` in **testing** lane.
4. Commit evidence logs; human gate approvals stay in journal `gates_pending`.

## Hermes cron

1. Schedule `python scripts/validate-workflow.py` on PR.
2. Schedule `python scripts/headless-verify.py` when `next_action` matches `implement-feature`.
3. Hermes FTS memory is optional; prefer `docs/playbooks/` for repo-scoped patterns.

## GitHub Actions

See `.github/workflows/validate-workflow.yml` and `verify-on-schedule.yml`.

## Do not

- Let headless workers edit `gates_pending` without human approval strings in journal.
- Replace `journal/state.json` with external DB without dual-write to `progress.md`.
