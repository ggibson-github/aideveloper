# Cursor Developer Expert System

This folder is an **expert system** that agents such as Cursor use to simulate the behavior of a software developer. A **journal** (`journal/progress.md`) gives the system memory across sessions—recording phase, decisions, open questions, and next steps so work can resume without starting over. **Rules for the agent** (in `AGENTS.md` and related skills) steer the expert toward talking with the operator: clarifying requirements, resolving blockers, and seeking approval at review gates—rather than guessing or making rash decisions on its own.

The pipeline turns a specification into design docs, diagrams, tasks, and implementation. It also supports **continued development**: new features, changes to existing features, refactoring to reduce tech debt, and a professional Git workflow (branch, commit, PR, push) with tests run before push.

## How to use

1. **Copy this folder** for a new project.
2. **Put your specification** in `spec.md` (or tell the agent which file is the spec).
3. **Open the folder in Cursor** and say **"Start"** or **"Implement from spec.md"** to begin. Say **"Continue"** to resume from where the agent left off (e.g. after restarting).
4. The agent will parse the spec, ask any blocking questions, tell the user if you need them to stop the app so you can build or start the app and test or to gather logs or any other help you need, produce HLD and DD (with your approval gates), generate diagrams, break down tasks, scaffold the project, and implement features—updating `journal/progress.md` and optionally `STATUS.md` so you can resume anytime.
5. **After initial delivery**, say **"Add a feature"** or **"I want to change X"** to enter iterative mode: the agent will gather requirements, design, get your approval, create a branch, implement, run tests (unit, integration, UI automation), and help with commit/PR/push. Tests are run before push to prove previous features still work. Artifacts are organized in `docs/design/`, `docs/features/<feature-id>/`, `docs/decisions/`, and `tests/` (unit, integration, e2e).
6. **Store fact snippets** (Slack excerpts, URLs, SQL, team contacts, etc.): say **"Remember this"** or **"Note this down"** and paste the text. The agent saves it to `docs/facts/captured.md` so you and the agent can find it later.

## Reference

Full design: see `documents/spec-to-artifacts-agent-skills-system.md`.

When setting up a python service prefer installing portable python within the project folder instead of venv.
When installing torch as a requirement use GPU with CUDA torch not CPU torch unless asked for explicitly.
Assume environment is Windows unless specified otherwise.
