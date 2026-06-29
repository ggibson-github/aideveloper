# Hierarchy expansion queue schema

## Top-level fields

| Field | Required | Description |
|-------|----------|-------------|
| `version` | yes | Schema version (1) |
| `description` | yes | Human summary |
| `unified` | yes | Must be `true` — one queue holds all branches |
| `source` | yes | Path to hierarchy markdown |
| `prompt` | yes | Path to wake prompt markdown |
| `output_dir` | yes | Leaf docs directory |
| `items` | yes | Ordered work list |
| `expansion_status` | no | `pending` \| `complete` — structural expand done |
| `depth_pass` | no | Last completed depth-loop pass number |
| `depth_audit` | no | `{ shallow_count, threshold }` from last audit |
| `signoff_ready` | no | `true` when audit clean and bundle written |
| `signoff_at` | no | ISO date when signoff_ready set |
| `hitl` | no | `{ pending: "H3", payload: "..." }` when awaiting human sign-off |

## Item fields

| Field | Required | Description |
|-------|----------|-------------|
| `id` | yes | Unique id (e.g. `A1.2`, `SEC-15-v2.14`) |
| `status` | yes | `pending` \| `done` \| `blocked` \| `failed` |
| `action` | yes | See actions below |
| `title` | yes | Short label |
| `parent` | no | Parent id for traceability |
| `source_section` | no | Section ref in hierarchy doc |
| `output` | no | Target path for leaf actions |
| `completed_at` | no | ISO date when done |
| `blocker` | no | User input needed (H2) |
| `error` | no | Failure message |
| `notes` | no | Rejection reason or deepen instructions |

## Actions

| Action | Phase | Purpose |
|--------|-------|---------|
| `expand` | 2 | Split branch node; append children to same queue |
| `document` | 2 | Write first-pass leaf doc |
| `deepen` | 3 | Add depth: mermaid, JSON, edge cases, concrete steps |
| `challenge` | 3 | Adversarial review; revise or flag remaining risks |

Phase 3 items are usually **appended by** `audit-hierarchy-depth.py --enqueue` when a leaf scores below threshold.

## Unified queue rule

- **One file** = entire hierarchy (A–J + meta).
- FIFO across branches; structural completion = zero pending expand/document items.
- Depth completion = audit `ready_for_signoff: true`.
- Child items append to the **same** `items[]` — never fork queues per branch.

## Ordering

- Process **first** `pending` in array order (FIFO)
- **Append** new items only; never insert at front or delete pending
- Child ids should extend parent id (`A1` → `A1.1`, `A1.2`)

## Completion signals

| Gate | Checker |
|------|---------|
| Structural expand | `check-hierarchy-queue.py` → `EMPTY` (no pending expand/document) |
| Coverage | `verify-hierarchy-expansion.py` → `ok: true` |
| Depth | `audit-hierarchy-depth.py` → `ready_for_signoff: true` |
| Human | H3 bundle reviewed; journal records accept/reject/waive |

Agent phrase (Phase 2 only): `HIERARCHY_EXPANSION_COMPLETE`

## Example

See `docs/automation/vision-expansion-queue.json` (completed + signoff_ready) or `docs/automation/templates/hierarchy-expansion/queue.template.json`.
