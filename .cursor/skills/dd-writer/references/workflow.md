# DD writer workflow

1. Read `journal/state.json`, `docs/design/hld.md`.
2. Write `docs/design/dd/api.md`, `dd/data.md`, `dd/ops.md`; update `dd.md` index.
3. Update staleness manifest.
4. `next_action` → `wait for DD approval`; `gates_pending: ["dd"]`.
5. After approval: `run diagram-generator`.
