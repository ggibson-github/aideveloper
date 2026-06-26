# Cursor Developer Expert System (v2)

Verified delivery orchestration for AI developers: gated SDLC pipeline, deterministic routing via `journal/state.json`, evidence-backed tasks, and conductor + subagent roles.

A **journal** (`journal/progress.md` + `journal/state.json`) gives memory across sessions. **Rules** and **commands** steer the conductor; workers (Librarian, Verifier) stay bounded.

## How to use

1. **Copy this folder** for a new project.
2. Put your specification in `spec.md`.
3. Open in Cursor. Use **`/continue`** or say **Start** / **Continue**.
4. Use **`/status`** for operator view without opening design docs.
5. Pipeline: spec → HLD → DD (split `docs/design/dd/`) → diagrams → task cards → scaffold → implement with **evidence** → done.
6. **Remember facts** via `docs/facts/INDEX.md`. **Playbooks** capture repo patterns in `docs/playbooks/`.

## v2 harness

| Piece | Location |
|-------|----------|
| Machine state | `journal/state.json` |
| Commands | `.cursor/commands/` |
| Conductor + workers | `orchestrate-subagents`, `librarian`, `verifier` skills |
| Task cards | `docs/tasks/task-NNN.md` |
| Evidence | `evidence/task-NNN-test.log` |
| Staleness | `docs/manifest/staleness.json` |
| Dashboard | `docs/operator/dashboard.md` |
| Validate | `python scripts/validate-workflow.py` |
| Headless verify | `python scripts/headless-verify.py` |

**Hooks:** Python 3 required for `.cursor/hooks/`. See `.cursor/hooks/README.md`.

**Integrations:** `docs/operator/integrations.md` (OpenClaw/Hermes bridge, no full gateway in v2).

## Context retrieval (v1 baseline)

Rules in `.cursor/rules/`, facts in `docs/facts/INDEX.md`, hooks inject on continue/journal read.

## Reference

Full design: `documents/spec-to-artifacts-agent-skills-system.md` (§7 context, §8 v2 harness).
