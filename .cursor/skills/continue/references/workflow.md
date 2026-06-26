# Continue workflow (v2)

1. Read `journal/state.json` + `progress.md` + Context files.
2. Blocking questions in state → ask user; "continue" is not an answer.
3. Blockers / last_failure → discuss with user before clearing.
4. Gates pending → re-prompt explicit approval.
5. `next_action` empty or `done` → stop or ask user.
6. Otherwise run **one** step:
   - `run spec-parser` → spec-parser skill
   - `run hld-writer` → hld-writer
   - `run dd-writer` → dd-writer (split dd/api, data, ops)
   - `run diagram-generator` → diagram-generator
   - `run task-breakdown` → task-breakdown (creates task cards)
   - `run scaffold-project` → scaffold-project
   - `implement-feature (task K/N)` → implement-feature
   - `reconcile-stale` → reconcile-stale
   - `reconcile-artifact-graph` → reconcile-artifact-graph
   - `run program-scoper` → program-scoper
   - `run integration-manifest-keeper` → integration-manifest-keeper
   - `orchestrate-program` → orchestrate-program
   - `run iterative-feature` → iterative-feature
   - `run git-workflow (...)` → only if `last_verify` passed or exception documented
7. Run `python scripts/route-tier.py --apply` after changing `next_action`.
8. Dual-write journal + state; run generate-dashboard at session end.
