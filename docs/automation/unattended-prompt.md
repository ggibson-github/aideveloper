# Unattended template **release** evolution prompt

**Not** for consumer project SDLC. For pipeline autopilot on your PC, use [`local-autopilot-prompt.md`](local-autopilot-prompt.md) and `/autopilot`.

This prompt is for **one** row in `release-queue.json` (template v2.x release slices).

## Inputs

1. `docs/automation/release-queue.json` — pick the first `status: pending` release (if all done, stop).
2. Plan todo id in that release row — implement deliverables from `documents/plans/v2-full-evolution.md` for that slice only.
3. `docs/decisions/automation-waivers.md` — human design gates waived for plan-driven template work.

## Rules

- Do **not** change `journal/state.json` `version` away from `2`.
- Do **not** implement multiple releases in one run.
- Run `python scripts/validate-workflow.py` before finishing.
- Update release queue: `status: done` or `failed` with `last_error`.
- Open PR on `release/v2.x` branch or document branch in queue.

## Definition of done

- Files from plan table for that release exist.
- `validate-workflow.py` passes.
- Queue row updated.

## On failure

Set `status: failed`, `last_error` message; stop; do not start next release.
