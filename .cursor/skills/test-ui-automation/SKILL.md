---
name: test-ui-automation
description: >-
  Adds or runs UI/E2E tests that navigate the application, trigger features, and
  capture logs to verify results. Use when the app has a UI and features need
  regression coverage via automated UI flows.
---

# Test UI Automation

## When to use

- Application has a user interface and the user or pipeline requests UI/E2E coverage
- After implementing a user-facing feature that should be covered by automated UI tests
- To prove previous UI features still work when making changes (regression)

## Instructions

1. **Location**: Place UI automation tests in `tests/e2e/` (or `tests/ui-automation/`). Use a framework appropriate to the stack (e.g. Playwright, Cypress, Selenium).
2. **Structure**: Each test or suite should (a) **navigate** the UI to the area where the feature under test lives (e.g. open app, go to screen or route), (b) **trigger** the feature (e.g. click, fill form, submit), (c) **capture logs** and outputs (e.g. network, console, screenshot) to verify results, and (d) **assert** expected behavior (e.g. success message, data persisted, no errors).
3. **Add tests**: When adding a new user-facing feature, add or update E2E tests that cover the happy path and critical failures. Ensure tests are stable (e.g. use stable selectors, wait for conditions).
4. **Run**: Execute the E2E suite as part of the full test run before commit/push. If tests fail, record in journal (Blockers or Last failure) and do not push until fixed.
5. **Journal**: When adding or updating UI tests, note in the journal (e.g. Artifacts or Last session summary) so the pipeline knows to run them.

Tests in this folder should be runnable by the project's test runner or a dedicated E2E command (e.g. `npm run test:e2e`).
