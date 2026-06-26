---
name: spec-parser
description: >-
  Parses the project specification, extracts requirements, validates, and lists
  assumptions and open questions. Use when starting the project, when the user
  points to a spec file, or when the spec has changed and must be re-parsed.
---

# Spec Parser

## When to use

- User says "start", "implement from spec", or points to a requirements/spec file
- Pipeline is at spec phase or journal says next action is "run spec-parser"
- User indicates the spec has changed and must be re-parsed

## Instructions

1. Read the spec: default path is `spec.md`, or use the path from the journal or user.
2. Emit a requirements summary and write it to `docs/design/requirements-summary.md`.
3. Emit assumptions and open questions; classify each as **blocking** (major/high-risk) or **deferred** (resolve when reaching the task that needs the answer). **Flag possible blockers** the user should be aware of: external dependencies (e.g. downloads from GitHub, Hugging Face), APIs, access or credentials, so these can be discussed early and the agent and user stay in agreement.
4. Write open questions into `journal/progress.md` under Open questions (blocking) and Open questions (deferred). Do not proceed past this phase until all blocking questions are answered by the user.
5. If the user has answered any question in this turn, record the question and answer in Resolved Q&A in the journal in the **same response** and remove it from open questions.
6. Optionally record spec file path and last-modified (or a version) in the journal for spec-change detection.
7. After completion (and only when blocking questions are empty), set next action to "run hld-writer" and update the journal (or rely on journal-keeper).
