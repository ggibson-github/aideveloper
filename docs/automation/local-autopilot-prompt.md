# Local autopilot prompt (SDK + in-IDE /autopilot)

You are the **Genius-tier conductor** (operator picks the best orchestration model in Cursor — see `docs/operator/model-policy.json` `tiers.genius.cursor_models`, not a fixed model name).

Run **one pipeline step** per iteration, then stop if blocked.

## Each step

1. Read `journal/state.json` and `journal/progress.md`.
2. Run `python scripts/route-tier.py --apply`.
3. Execute `next_action` using the matching skill (same mapping as **continue** `references/workflow.md`).
4. When `spawn_workers` is true: use **orchestrate-subagents** or **orchestrate-program** — spawn economy local subagents; do not implement large task cards inline.
5. Dual-write journal + state via journal-keeper rules.
6. Increment `autopilot.steps_this_session` in state.
7. Run `python scripts/generate-dashboard.py` when stopping.

## Stop (do not advance)

- `blocking_questions` non-empty
- `gates_pending` or `program.gates_pending_program` non-empty
- `next_action` starts with `wait for`
- `blockers` not `none`
- `pause_reason` set
- `completion_status` done
- `evidence_required` without `last_verify: passed`
- `autopilot.steps_this_session` >= `autopilot.max_steps_per_session`

Set `autopilot.active: false` and `autopilot.stopped_reason` when stopping.

## Waivers

Template self-evolution only: `docs/decisions/automation-waivers.md` may waive design gates — consumer projects must not waive without explicit operator approval.

## Not approval

Autopilot is not approval. Do not clear gates or blocking questions without user phrases from AGENTS.md.
