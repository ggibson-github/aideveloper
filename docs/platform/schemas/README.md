# Platform JSON Schema Registry

Authoritative schemas for `journal/state.json` additive blocks, lane leases, and platform artifacts.

**Validator:** `scripts/validate-workflow.py` loads this registry. Use `--strict` to fail on unknown keys in registered blocks.

| Schema file | Validates | Release |
|-------------|-----------|---------|
| [state-goal.v1.json](state-goal.v1.json) | `state.goal` | v2.14 |
| [state-pursuit.v1.json](state-pursuit.v1.json) | `state.pursuit` (excl. nested `active_workflow` shape — see active-workflow) | v2.15 |
| [state-hitl.v1.json](state-hitl.v1.json) | `state.hitl` | v2.15 |
| [state-self-gate.v1.json](state-self-gate.v1.json) | top-level `self_gate_mode` | v2.15 |
| [state-platform.v1.json](state-platform.v1.json) | `state.platform` | v2.16 |
| [state-program.v1.json](state-program.v1.json) | top-level `program` object | v2.19 |
| [state-company.v1.json](state-company.v1.json) | `state.company` | v2.19 |
| [lane.v1.json](lane.v1.json) | `program/workstreams/<id>/lane.json` | v2.19 |
| [state-active-workflow.v1.json](state-active-workflow.v1.json) | `state.pursuit.active_workflow` | v2.26 |
| [transistor.v1.json](transistor.v1.json) | `docs/platform/transistors/*.json` | v2.24 (placeholder) |
| [workflow-dag.v1.json](workflow-dag.v1.json) | `docs/workflows/*.json` | v2.25 (placeholder) |

## Strict mode

When `--strict` is set and a block is present, validation uses `additionalProperties: false` on that block's schema. Missing blocks are skipped (additive releases).

## Registry dict (implement in validate-workflow.py)

```python
STATE_SCHEMA_REGISTRY = {
    "goal": "docs/platform/schemas/state-goal.v1.json",
    "pursuit": "docs/platform/schemas/state-pursuit.v1.json",
    "hitl": "docs/platform/schemas/state-hitl.v1.json",
    "self_gate_mode": "docs/platform/schemas/state-self-gate.v1.json",
    "platform": "docs/platform/schemas/state-platform.v1.json",
    "program": "docs/platform/schemas/state-program.v1.json",
    "company": "docs/platform/schemas/state-company.v1.json",
}
ACTIVE_WORKFLOW_SCHEMA = "docs/platform/schemas/state-active-workflow.v1.json"
LANE_SCHEMA = "docs/platform/schemas/lane.v1.json"
```

## Related manifests

- [bootstrap-transistors.manifest.json](../bootstrap-transistors.manifest.json) — minimum transistor set (SEC-18 §M, v2.24)
