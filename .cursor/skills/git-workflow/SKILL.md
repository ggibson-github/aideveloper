---
name: git-workflow
description: >-
  Connects the project to a Git repo, creates branches, and handles add/commit/PR/push.
  Use when connecting a repo for the first time, creating a feature branch, committing,
  opening a PR, or pushing. Do not push until tests pass.
---

# Git Workflow

## When to use

- User asks to connect to GitHub (or another remote), create a branch, commit, open PR, or push
- Pipeline step is "run git-workflow (connect)" or "(branch)" or "(commit)" or "(push)"
- Before pushing: run full test suite (unit, integration, e2e) and do not push if tests fail

## Instructions

1. **Connect repo (first time)**: If no remote exists, ask the user for the repo URL (or instruct them to create one). Run `git init` if needed, then `git remote add origin <url>`. Optionally initial commit and push (e.g. main). Record **Repo URL** and **Current branch** in the journal.
2. **Branch**: Create a branch for the current feature or task (e.g. `feature/<feature-id>` or `feature/short-name`). Use `git checkout -b <branch>`. Update journal **Current branch**.
3. **Add and commit**: Stage changes (`git add`) and commit with a clear message (e.g. conventional commits: `feat(area): description`, `fix(area): description`). User may approve or edit the message. Update journal **Last commit**.
4. **PR and push**: Open a pull request (if the workflow uses PRs) or push the branch. **Do not push until the full test suite passes** (unit, integration, UI/e2e if present). Run tests first; if any fail, set Blockers in the journal and do not push until resolved. After push, record **PR URL** in the journal if applicable.

Journal fields to maintain: **Repo URL** (or "none"), **Current branch**, **Last commit**, **PR URL** (if opened).
