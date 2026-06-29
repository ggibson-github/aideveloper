# Contract tests (v2.20+)

Recorded MCP and tool fixtures for boundary verification. Contract tier sits between integration and e2e:

| Tier | When | What |
|------|------|------|
| unit | all releases | mocks |
| integration | v2.14+ | state + scripts |
| **contract** | **v2.20+** | fixtures under `tests/contract/` |
| e2e | v2.20+ | full role handoff; externals mocked at boundary only |

## Layout

```
tests/contract/
├── README.md           # this file
├── fixtures/           # recorded request/response pairs (redacted)
│   └── <tool-id>/
└── test_<tool-id>_contract.py
```

## Rules

- Fixtures must redact secrets and credentials before commit.
- Contract tests assert schema and status codes — not live external availability.
- CI matrix: see [09-architectural-supplements.md](../../V2_Implementation_Plan/09-architectural-supplements.md).
