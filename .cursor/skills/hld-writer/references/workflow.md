# HLD writer workflow

1. Read `journal/state.json`, `docs/design/requirements-summary.md`.
2. Write `docs/design/hld.md` (components, tech, risks, **setup/run requirements**).
3. Update staleness manifest.
4. `next_action` → `wait for HLD approval`; add `gates_pending: ["hld"]`.
5. After approval: `run dd-writer`; update `allowed_reads` for DD phase.
