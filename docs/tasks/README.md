# Task cards (v2)

One markdown file per implement task. Created by **task-breakdown**.

## Template (`task-NNN.md`)

```markdown
# Task NNN: Title

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

## Evidence

- Log: `evidence/task-NNN-test.log`
```

## Usage

- `next_action`: `implement-feature (task N/Total)`
- `allowed_reads` should include this card only (+ playbooks/facts as needed)
- **verifier** runs Test command before task complete
