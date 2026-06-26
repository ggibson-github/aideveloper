---
name: hld-writer
description: >-
  Produces the high-level design document from requirements. Use when the pipeline
  is at HLD phase or when the user asks for high-level design.
---

# HLD Writer

## When to use

- Journal says next action is "run hld-writer" or current phase is after spec-parser
- User explicitly asks for high-level design

## Instructions

1. **Ask the user** if they have an existing template or a completed HLD document to use as a template to copy from for the new HLD, so the output follows company policies on HLD formatting. If they provide a path or document, read it and use its structure, section headings, and style for the new HLD.
2. Read `docs/design/requirements-summary.md` and `journal/progress.md` (Resolved Q&A, open questions).
3. **Anticipate possible blockers** during design: external dependencies (e.g. libraries from GitHub, models from Hugging Face), APIs, network access, credentials, downloads. Ask the user follow-up questions about these so the agent and user are in agreement about important decisions before implementation (e.g. "Will the app need to download models at runtime? Do you have access to X?"). Surface uncertainties as open questions in the journal if they affect the design.
4. Produce the high-level design: system context, main components, tech choices, risks. **Always capture run-environment and setup requirements** (e.g. portable Python, venv, Visual Studio solution or other dev environment, runtimes, GitHub repos or other sources to clone/download, SDKs, assets) so the task-breakdown phase can add explicit tasks to install and set them up. The agent is expected to perform those setup tasks; requirements must be installed in the correct order for the generated code to work. Write to `docs/design/hld.md`.
5. Update the journal: set phase to HLD done, next action to **wait for HLD approval** (human gate). Do not proceed to DD until the user approves the HLD or explicitly waives the gate.
6. Record approval or waiver in the journal when the user responds (e.g. "HLD approved on …" or "HLD gate waived").
