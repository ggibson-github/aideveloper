# Evidence types (v2.10+)

| Type | Path pattern | Producer |
|------|--------------|----------|
| Software test log | `evidence/task-NNN-test.log` | Verifier, `verify-router.py` |
| Tool CLI log | `evidence/task-NNN-test.log` | tool-operator, `verify-router.py` |
| Visual | `evidence/task-NNN-screenshot.png` (referenced in task card) | manual or tool |
| Binary checksum | `evidence/task-NNN-checksum.txt` | script |
| Human gate | `program/gates/<gate-id>/approval.md` | user + conductor |

`evidence_required` in state blocks task/lane advance until `evidence_files` populated and `last_verify: passed`.
