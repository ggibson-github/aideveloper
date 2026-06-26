---
name: iterative-feature
description: >-
  Drives the workflow for a new or modified feature after initial delivery:
  gather requirements, research, design, approval, branch, implement, test, commit/PR/push.
  Use when the user asks to add a feature, change a feature, or continue iterative development.
---

# Iterative Feature

## When to use

- User asks to add a new feature or modify an existing feature
- Journal mode is `iterative_feature` or user says "new feature", "add feature", "change feature"
- Continued development after initial project delivery

## Instructions

1. **Feature id**: Assign or use a stable feature-id (e.g. slug like `export-csv` or ticket number). Create `docs/features/<feature-id>/` if it does not exist.
2. **Gather requirements**: Capture the feature request in `docs/features/<feature-id>/spec.md`. Ask clarifying questions; record answers in journal Resolved Q&A or in the feature spec. Do not implement until blocking questions are answered.
3. **Research** (if needed): Document options or spikes in `docs/features/<feature-id>/research.md` or in decisions.
4. **Design**: Write feature-level design (and update project-level `docs/design/` if architecture is affected) in `docs/features/<feature-id>/design.md`. Follow same templates/approval discipline as greenfield (ask for templates, human gate).
5. **Approval**: Do not implement until the user approves the feature design (or waives). Record in journal or `docs/features/<feature-id>/approval.md`.
6. **Branch**: Invoke **git-workflow** to create a branch (e.g. `feature/<feature-id>`). If repo is not connected, run git-workflow to connect first.
7. **Implement**: Run **implement-feature** for this feature's tasks (or break into tasks in TODOS and implement). Add or update unit and integration tests; run **test-ui-automation** if the app has a UI and the feature is user-facing. Run full test suite (unit, integration, e2e) to prove previous features still work.
8. **Refactor if needed**: If the change would create duplication or tech debt, run **refactor** before or as part of the change.
9. **Commit and push**: Run **git-workflow** to add, commit, and open PR/push. Do not push until all tests pass.
10. Update journal: set current_feature_id, mode = iterative_feature, next action (e.g. "run git-workflow (commit)" or "done (feature complete)").
