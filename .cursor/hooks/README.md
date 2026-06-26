# Cursor context hooks (v2)

Project hooks inject pipeline state and enforce read guards. They **supplement** `.cursor/rules/` and `journal/state.json`—not replace them.

## Requirements

- **Python 3** on PATH (`python` or `py` on Windows)
- Stdlib only (`context_builder.py`, `state_io.py`, `cursor_context_hook.py`)

## Events (v2)

| Event | Behavior |
|-------|----------|
| `beforeSubmitPrompt` | Inject context on continue/start/resume and slash commands |
| `postToolUse` | Inject after Read of `journal/progress.md` or `state.json` |
| `sessionStart` | Best-effort inject (may be flaky in Cursor) |
| `subagentStart` | Inject subagent contract + state snapshot (`user_message`) |
| `preToolUse` (Read) | **Ask** when reading `docs/design/` outside `allowed_reads` |
| `preCompact` | Write `journal/snapshot-YYYY-MM-DD.md` |

## state.json

Hooks read `journal/state.json` first via `state_io.py`. Regenerate from journal: `python scripts/sync-state.py`.

## Verification

```bash
python scripts/validate-workflow.py
python scripts/generate-dashboard.py
```

Say **continue** in Agent chat; check Hooks output channel.

## sessionStart caveat

See [forum thread](https://forum.cursor.com/t/sessionstart-hook-additional-context-is-never-injected-into-agents-initial-system-context/158452). Prefer commands + `beforeSubmitPrompt` + rules.
