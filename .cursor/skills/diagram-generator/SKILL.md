---
name: diagram-generator
description: >-
  Generates architecture, sequence, ER, and C4-style diagrams from design docs.
  Use when the pipeline is at design-artifacts phase after DD approval.
---

# Diagram Generator

## When to use

- Journal says DD is approved and next action is "run diagram-generator"
- Pipeline is at design-artifacts phase

## Instructions

1. Use **Mermaid** by default for all diagrams (architecture, sequence, ER, C4-style).
2. Read `docs/design/hld.md` and `docs/design/dd.md`.
3. Produce diagrams (e.g. architecture, sequence, ER) and save under `docs/diagrams/` with clear names (e.g. `architecture.mmd`, `sequence.mmd`).
4. **Generate an HTML page** (e.g. `docs/diagrams/index.html`) that is used to view the diagrams in a browser. The page should load Mermaid.js (e.g. from a CDN) and render each diagram (e.g. by embedding the Mermaid source in `<pre class="mermaid">` blocks or by loading the `.mmd` files). Include a simple list or nav so users can open the page and see all diagrams. Reference this page from the design docs or README if helpful.
5. Reference the diagrams from the design docs where relevant.
6. Update the journal: set phase to diagrams done, next action to "run task-breakdown".
