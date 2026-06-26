---
name: continue
description: >-
  Resumes the project pipeline from the journal. Use when the user says "continue",
  "start", or "resume" so the agent reads the journal and performs the next step.
---

# Continue

## When to use

- User says "continue", "start", or "resume"
- User asks to pick up where the project left off
- When the pipeline is waiting for an answer or approval, "continue" means re-prompt, not "user answered" or "user approved"

## Instructions

**Do not** treat the user saying "continue" as an answer to a question or as approval/waiver of a gate. "Continue" means only: read the journal and perform the next step. If that step is waiting for an answer or for approval, re-prompt and do **not** advance until the user gives a substantive answer or explicitly approves/waives (e.g. "I approve the HLD" or "Skip HLD approval"). The word "continue" by itself is not an answer and is not approval.

1. **Read `journal/progress.md`.** If the file is missing or empty, set next action to "run spec-parser", create the journal with the full schema (see journal-keeper or the template in `journal/progress.md`), and run the spec-parser workflow.
2. **Blocking questions:** If Open questions (blocking) is non-empty, ask the user those questions and do not advance until they are answered. **The word "continue" is not an answer.** If the user only said "continue", re-ask the blocking questions and do not advance. Only when the user provides a substantive answer (and you record it in Resolved Q&A) may you proceed. When the user answers, record each question and answer in Resolved Q&A in the **same turn** and remove from open questions, then re-evaluate.
3. **Blockers / Last failure:** If Blockers or Last failure is set, **communicate with the user**: describe the block clearly, explain what failed or what is needed, and **discuss how to proceed**. Do not skip the blocked step or assume a workaround without the user's agreement. Wait for the user to agree on next steps (e.g. retry, alternative approach, manual action). Only then clear the blocker and update the journal.
4. **Wait for approval:** If next action is "wait for HLD approval", "wait for DD approval", "wait for feature approval" (or similar), do **not** advance. Re-surface the item: e.g. "The HLD is ready at docs/design/hld.md. Please review and reply with 'I approve the HLD' or 'Skip HLD approval' to proceed. Saying 'continue' does not count as approval." Do not record approval in the journal and do not set next action to the following step until the user explicitly approves or waives. Only then update the journal (e.g. "HLD approved on …") and set next action to the next pipeline step (e.g. "run dd-writer" for HLD approval; "run diagram-generator" for DD approval).
5. **Done or empty:** If next action is empty or "done", stop and optionally ask the user what they want to do next.
6. **Otherwise perform the single next step:**
   - "run spec-parser" → run the spec-parser workflow (read spec, write to docs/design/requirements-summary.md, open questions, update journal).
   - "run hld-writer" → run the hld-writer workflow (docs/design/).
   - "run dd-writer" → run the dd-writer workflow (docs/design/).
   - "run diagram-generator" → run the diagram-generator workflow.
   - "run task-breakdown" → run the task-breakdown workflow.
   - "run scaffold-project" → run the scaffold-project workflow.
   - "implement-feature (task K/N)" → run the implement-feature workflow for task K.
   - "run iterative-feature" (or with step) → run the iterative-feature workflow (gather requirements, design, approval, branch, implement, test, commit/push).
   - "run refactor" → run the refactor workflow; run full test suite after.
   - "run git-workflow (connect|branch|commit|push)" → run the git-workflow step; do not push until tests pass.
   - "run test-ui-automation" → add or run UI/E2E tests (tests/e2e/); navigate, trigger, capture logs, assert.
   (Do not run any of the above when next action is a "wait for … approval" value; step 4 handles those.)
7. After the step, update the journal (journal-keeper behavior): phase completed, next action set, artifacts updated. For iterative mode, update Mode, Current feature id, Current branch, Repo URL as needed.
8. At session end, write **Last session summary** in the journal and optionally refresh `STATUS.md`.

Always follow the phase order. Do not skip phases unless the journal says the phase is already complete and the artifact exists.
