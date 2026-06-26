# Cursor Developer Expert System (v2.13)

Verified delivery orchestration for AI developers: gated SDLC pipeline, genius-tier conductor + local subagents, **local autopilot** (run-until-blocked), program mode, evidence-backed tasks.

A **journal** (`journal/progress.md` + `journal/state.json`) gives memory across sessions. **Rules** and **commands** steer the conductor; workers stay bounded.

## How to use

1. **Copy this folder** for a new project.
2. Put your specification in `spec.md`.
3. Open in Cursor. Select a **genius-tier** model from [`model-policy.json`](docs/operator/model-policy.json).
4. **`/autopilot`** — run pipeline locally until gate/blocker (no repeated Continue). Or **`/continue`** for one step.
5. Use **`/status`**, **`/model`**, **`/program`**, **`/lane <id>`**.
6. **Software pipeline:** spec → HLD → DD → diagrams → task cards → scaffold → implement with **evidence** → done.
7. **Program mode:** mega-spec → milestone + workstreams → manifest gates → parallel lanes.

## Local autopilot (v2.13)

```bash
python scripts/automation/check-pipeline-blocked.py   # pre-flight
```

Say **autopilot** or `/autopilot` in Cursor. Optional SDK loop: `python scripts/automation/run-local-pipeline.py` (local runtime, `cursor-sdk` + `CURSOR_API_KEY`). See [`docs/automation/README.md`](docs/automation/README.md).

## v2 harness

| Piece | Location |
|-------|----------|
| Machine state | `journal/state.json` (v2, `autopilot`, optional `program`) |
| Model routing | `docs/operator/model-policy.json`, `scripts/route-tier.py` |
| Commands | `.cursor/commands/` (+ **autopilot**) |
| Autopilot | `autopilot` skill, `check-pipeline-blocked.py`, `run-local-pipeline.py` |
| Conductor + workers | `orchestrate-subagents`, `orchestrate-program`, `librarian`, `verifier`, `tool-operator` |
| Program | `program/`, `program-scoper`, `integration-manifest-keeper` |
| Task cards | `docs/tasks/` and `program/workstreams/*/tasks/` |
| Evidence | `evidence/` — see `docs/operator/evidence-types.md` |
| Staleness | `docs/manifest/staleness.json`, `program/manifest/artifact-graph.json` |
| Pipelines | `docs/manifest/pipelines/*.yaml` |
| Template packs | `template-packs/game-asset-pipeline/`, `data-platform/` |
| Dashboard | `docs/operator/dashboard.md` |
| Validate | `python scripts/validate-workflow.py` |
| Verify | `python scripts/verify-router.py` |
| Unattended | `docs/automation/` |

**Hooks:** Python 3 required for `.cursor/hooks/`. See `.cursor/hooks/README.md`.

**Integrations:** `docs/operator/integrations.md` (local autopilot, OpenClaw/Hermes bridge).

## Genius-tier conductor (v2.4+)

Operator selects best **genius-tier** orchestration model once per session (`model-policy.json`); economy **local** subagents for implement/explore/verify. See `documents/genius-conductor-tiered-routing.md`.

## Context retrieval (v1 baseline)

Rules in `.cursor/rules/`, facts in `docs/facts/INDEX.md`, hooks inject on continue/journal read.

## Reference

- `documents/spec-to-artifacts-agent-skills-system.md` (§7–§10)
- `documents/genius-conductor-tiered-routing.md`
- `documents/plans/v2-full-evolution.md`
