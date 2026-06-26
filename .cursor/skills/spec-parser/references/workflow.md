# Spec parser workflow

1. Read spec (default `spec.md`).
2. Write `docs/design/requirements-summary.md`.
3. Classify open questions: blocking vs deferred → state `blocking_questions` / `deferred_questions`.
4. Do not proceed until blocking empty.
5. Record answers in archive + journal pointers (same turn).
6. Update staleness manifest if spec version changed.
7. `next_action` → `run hld-writer`; `allowed_reads` → requirements-summary, spec, journal, facts INDEX.
