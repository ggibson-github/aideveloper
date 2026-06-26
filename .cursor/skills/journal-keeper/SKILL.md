---
name: journal-keeper
description: >-
  Updates the project progress journal after each phase or when the user answers
  a question. Use after every phase completion and whenever a decision is recorded.
---

# Journal Keeper

## When to use

- After every phase completion (spec-parser, hld-writer, dd-writer, diagram-generator, task-breakdown, scaffold-project, implement-feature)
- Whenever the user answers a blocking or deferred question (record in same response)
- At session end (write Last session summary)

## Instructions

1. Maintain the full journal schema in `journal/progress.md`: Spec file, Spec version / last modified, Mode (greenfield | iterative_feature), Current phase, Current feature id, Repo URL, Current branch, Last completed, Next action, Artifacts, Open questions (blocking), Open questions (deferred), Resolved Q&A / Decisions, Blockers, Pause reason / Delay, Last failure / Retry state, Completion status, Last session summary. Artifacts use paths: docs/design/, docs/diagrams/, docs/decisions/, docs/features/<id>/, tests/unit/, tests/integration/, tests/e2e/.
2. After each phase: write the phase completed, artifacts produced, and next action. Do not mark a phase complete if blocking questions remain unanswered.
3. When the user answers a question: in the **same response**, add the question and answer to Resolved Q&A and remove the question from Open questions (blocking or deferred).
4. At session end: write **Last session summary** (one short paragraph: what was done, what is next, what is needed from the user). Optionally refresh `STATUS.md` with the same summary.
