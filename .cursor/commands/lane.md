# Lane focus (/lane)

Focus one program workstream lane.

Usage: `/lane <workstream-id>` (e.g. `character`, `equipment`, `pipeline`)

Read:

- `program/workstreams/<id>/lane.json`
- `program/workstreams/<id>/workstream.md`
- Current task in `program/workstreams/<id>/tasks/` if `lane.current_task` set
- `program/integration/manifest.md`

External lane chats: complete task, write evidence, then:

```bash
python scripts/complete-work-order.py <workstream> --evidence evidence/task-NNN-test.log --status verify
```

Conductor merges integration steps in separate chat.
