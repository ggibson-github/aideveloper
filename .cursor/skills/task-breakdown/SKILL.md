---
name: task-breakdown
description: >-
  Breaks the design into a phased task list with dependencies and milestones.
  Use when diagrams are done and before scaffolding.
---

# Task Breakdown

## When to use

- Journal says next action is "run task-breakdown" (after diagram-generator)
- User asks for a task list or backlog from the design

## Instructions

1. Read `docs/design/dd.md`, `docs/design/hld.md`, and `journal/progress.md`.
2. **Always add tasks for setting up requirements** as part of creating the application. The agent is expected to perform these tasks—they are not optional or left to the user. For the generated code to work, all requirements must be installed and in the correct order. **Identify all setup/install requirements** needed to run the app locally: portable Python or other runtimes, GitHub repos (or other sources) to clone or download, package registries, model files, credentials or config that must be in place. Do not assume the user will do these manually—they must become explicit tasks.
3. **Add setup/install tasks to the task list** so the app can run locally when implementation is complete. For each requirement, add one or more concrete tasks, for example:
   - **Portable Python, venv, or other development environment**: Add tasks for runtime or IDE/project setup (e.g. "Download portable Python", "Set up portable Python / create venv", "Create Visual Studio solution" or other dev-environment setup). **These environment-setup tasks must be ordered before any task that installs libraries or packages** so that package installs (pip, NuGet, etc.) run inside or against the correct environment.
   - **GitHub or other repo**: Add tasks such as "Obtain repo from GitHub (clone or download; URL from design or user if needed)" and "Integrate or place repo as required by design." If the URL is unknown, the task can state "Obtain repo from GitHub—ask user for URL if not in design."
   - **Other runtimes, SDKs, or assets**: Add tasks to download, install, or configure them so they are ready before features that depend on them.
4. Produce an ordered task list (TODOs) with dependencies and milestones: **environment setup first** (portable Python, venv, Visual Studio solution, or other development/runtime environment)—then any library/package install tasks so they run inside or against that environment—then scaffold, then feature implementation. Do not order library or package installs before environment setup when the app uses a venv, portable runtime, or IDE solution. **Requirements must be installed in this correct order for the generated code to work; the agent is expected to do all of these tasks.** Derive the rest from the design.
5. Write the task list to `TODOS.md`.
6. Update the journal: set phase to task-breakdown done, next action to "run scaffold-project".
