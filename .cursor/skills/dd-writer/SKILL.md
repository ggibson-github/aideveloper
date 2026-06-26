---
name: dd-writer
description: >-
  Produces the detailed design document from HLD and requirements. Use when HLD
  is approved and the pipeline is at DD phase.
---

# DD Writer

## When to use

- Journal says HLD is approved (or gate waived) and next action is "run dd-writer"
- User explicitly asks for detailed design

## Instructions

1. **Ask the user** if they have an existing template or a completed DD document to use as a template to copy from for the new DD, so the output follows company policies on detailed design formatting. If they provide a path or document, read it and use its structure, section headings, and style for the new DD.
2. Read `docs/design/hld.md`, `docs/design/requirements-summary.md`, and `journal/progress.md`.
3. **Anticipate possible blockers** during detailed design: external dependencies (GitHub, Hugging Face, package registries), APIs, network access, credentials, runtime downloads. Ask the user follow-up questions so the agent and user are in agreement about how these will be handled (e.g. "The design assumes model files from Hugging Face—do you have network access and credentials, or should we plan for offline/bundled assets?"). Add open questions to the journal if needed.
4. Produce the detailed design: APIs, data models, interfaces, sequencing. **Always capture run-environment and setup requirements** (e.g. portable Python, venv, Visual Studio solution or other dev environment, runtimes, GitHub repos or other sources to clone/download, SDKs, assets) so the task-breakdown phase can add explicit tasks to install and set them up. Task-breakdown will add these setup tasks as part of creating the application; the agent is expected to perform them, and requirements must be installed in the correct order for the generated code to work. Write to `docs/design/dd.md`.
5. Update the journal: set phase to DD done, next action to **wait for DD approval** (human gate). Do not proceed to diagrams or scaffold until the user approves the DD or waives the gate.
6. Record approval or waiver in the journal when the user responds (e.g. "DD approved on …" or "DD gate waived").
