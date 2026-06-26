---
name: program-scoper
description: >-
  Decomposes mega-spec into program milestone, workstreams, and blocking questions.
  Use when mode is program or mega-spec detected.
---

# Program Scoper

## When to use

- `mode: program` or user mega-spec (game studio, multi-domain build-out)
- `next_action: run program-scoper`

## Instructions

1. Read `spec.md` (or user path) and `docs/manifest/pipelines/`.
2. Select `pipeline_id` (default `multi-domain-program`); match `pack_keywords` to `template-packs/` if applicable.
3. Produce:
   - `program_id`, `milestone` (bounded north star—not "entire company")
   - 3–6 `workstreams` with `program/workstreams/<id>/workstream.md` + `lane.json`
   - `blocking_questions` for high-risk unknowns
4. Select template pack: match spec keywords to `docs/manifest/pipelines/*.yaml` `pack_keywords`; copy stubs from `template-packs/<pack_id>/` into `program/` when starting fresh.
4. Set `program` in state (manifest path, artifact_graph path, `gates_pending_program`).
5. Set `next_action: wait for milestone approval` until user approves or waives.
6. Do **not** spawn parallel workers yet (serial program foundation).

See [references/workflow.md](references/workflow.md).
