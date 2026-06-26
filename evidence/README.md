# Evidence (v2)

Test and verify outputs for task completion. Written by **verifier** skill or `scripts/headless-verify.py`.

| Pattern | Purpose |
|---------|---------|
| `task-NNN-test.log` | Shell output from task card test command |
| `full-suite.log` | Full regression run before push |

Referenced in journal **Evidence files** and `journal/state.json` `evidence_files`.

Do not mark tasks complete or push without evidence when `evidence_required` is true.
