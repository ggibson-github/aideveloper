# Task breakdown workflow (full)

1. Read `docs/design/dd.md` or split files (`dd/api.md`, `dd/data.md`, `dd/ops.md`), `docs/design/hld.md`, `journal/state.json`.

2. **Setup tasks (required):** portable Python/venv/VS solution, clone repos, SDKs—**before** pip/NuGet installs.

3. **Task cards** (`docs/tasks/task-NNN.md`):
   - Title, acceptance criteria (bullets)
   - Design pointers (section links into DD)
   - Files to touch
   - Facts topics (for INDEX)
   - Test command
   - Evidence path: `evidence/task-NNN-test.log`

4. Write `TODOS.md` with task numbers matching card filenames.

5. Update staleness manifest: link tasks to DD nodes.

6. journal-keeper: dual-write; `allowed_reads` for scaffold step.
