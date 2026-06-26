---
name: scaffold-project
description: >-
  Creates repo layout, config, tooling, and CI skeleton from the design. Use when
  task breakdown is done and before implementation.
---

# Scaffold Project

## When to use

- Journal says next action is "run scaffold-project" (after task-breakdown)
- User asks to scaffold or set up the project structure

## Instructions

1. Read the journal. If the scaffold phase is already complete and the expected artifacts (e.g. src/, config) exist, skip scaffolding: set next action to "implement-feature (task 1/N)" (using the total task count from TODOS.md) and update the journal.
2. Otherwise read `docs/design/dd.md` and `TODOS.md` and create the project structure: directory layout, config files, tooling, and CI skeleton as implied by the design.
3. **If the agent needs a library, package URL, or other resource**: Ask the user for the URL (e.g. GitHub repo or other download location) if not known or if the default fails. Do not skip the step.
4. **If scaffold fails or the agent needs anything to unblock** (e.g. package install fails, clone fails, download fails, missing URL): do **not** skip. Explain the situation to the user and ask for help. Describe what failed or what is needed, record in the journal (Blockers / Last failure), and ask the user for the URL or other input. Only continue when the user provides what is needed or agrees on next steps.
5. Update the journal: set phase to scaffold done, Artifacts to include the created paths, next action to "implement-feature (task 1/N)".
