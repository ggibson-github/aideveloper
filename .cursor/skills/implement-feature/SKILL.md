---
name: implement-feature
description: >-
  Implements one feature or task from TODOS in order. Use when the pipeline is in
  implementation phase and next action is implement-feature (task K/N).
---

# Implement Feature

## When to use

- Journal says next action is "implement-feature (task K/N)" for some task index K
- Pipeline is in implementation phase

## Instructions

1. Read `TODOS.md` and `journal/progress.md` to identify the current task (the one indicated by next action).
2. Implement only that task. Do not skip ahead or implement multiple tasks in one go.
3. **If the agent needs a library or dependency**: Ask the user for the URL to the GitHub repo or other download location if it is not known or if the default source fails. Do not skip the step or assume a different source without asking.
4. **If a step fails or the agent needs anything to unblock** (e.g. download fails, missing URL, credentials, API key, manual step): do **not** skip the step. **Explain the situation** to the user and **ask for help**. Describe what is needed or what failed, write **Last failure / Retry state** and **Blockers** in the journal, and ask the user for the URL, credentials, or other input (e.g. retry, user provides URL, alternative source, manual download, change approach). Only proceed when the user provides what is needed or agrees on next steps. Do not assume a workaround or skip without user agreement. Do not mark the task complete until the blocker is resolved with the user's input.
5. Do not mark the task complete until tests pass or an exception is documented. If tests are handled by test-writer, coordinate: run or add tests, then update journal only on success.
6. After success: update journal (last completed = this task, next action = "implement-feature (task K+1/N)" or, if this was the last task, set Completion status to done and next action to "done"). If all tasks are complete, add a final handoff note if desired.
