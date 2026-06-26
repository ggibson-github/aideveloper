# Task cards (v2)

One markdown file per implement task. Created by **task-breakdown** or `python scripts/new-task-card.py`.

## Template (`task-NNN.md`)

```markdown
# Task NNN: Title

## Workstream

(none — main pipeline) or workstream id

## Acceptance criteria

- ...

## Design pointers

- `docs/design/dd/api.md#section`

## Files to touch

- `src/...`

## Facts topics

- api, staging

## Test command

`pytest tests/unit/test_x.py` or `npm test` or `(none — document manual verify)`

## Tool command

(optional) `python scripts/validate-workflow.py`

## Artifact outputs

(optional) paths produced

## Capability class

(optional) S0–S4

## Integration checks

(optional) manifest section or import rule

## Evidence

- Log: `evidence/task-NNN-test.log`
```

## Paths

- Software pipeline: `docs/tasks/task-NNN.md`
- Program workstream: `program/workstreams/<id>/tasks/task-NNN.md`

## Usage

- `next_action`: `implement-feature (task N/Total)`
- `allowed_reads` should include this card only (+ playbooks/facts as needed)
- **verifier** or `python scripts/verify-router.py` runs Test/Tool command before task complete
