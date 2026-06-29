# V2 Evolution Policy ADRs (SEC-17 + compose precedence)

**Status:** Accepted defaults — operator may override at H1 with journal record.
**Authority:** [V2_Implementation_Plan/00-vision-and-scope.md](../../V2_Implementation_Plan/00-vision-and-scope.md), [03-target-architecture.md](../../V2_Implementation_Plan/03-target-architecture.md) §5.

---

## ADR-V2-001 — Self-gate rigor (SEC-17-1)

**Decision:** `self_gate_mode` default = `checklist`. Escalate to `reviewer` (economy LLM reviewer subagent) when **any** trigger fires: large diff (>500 LOC), security-touch paths, new external dependency, or repeated verify fail on same task. `dual_reviewer` only when `strict_hitl=true` pack policy requires it.

**Rationale:** Checklist + auditable evidence paths keep S0 goal_verify honest; targeted reviewer avoids cost on every HLD/DD self-gate.

**Effective:** v2.15 · **State:** `self_gate_mode` · **Verify:** `tests/unit/test_strict_hitl_toggle.py`

---

## ADR-V2-002 — H3 scope (SEC-17-2)

**Decision:** Default H3 = **per milestone** (one H3 when `goal.type=milestone` or program milestone node completes). Pack `company.yaml` **`h3_scope`** overrides: `task | milestone | release | company_goal`. `goal-keeper` reads pack override at H1; if absent, use default.

**H3 transition rule:** `hitl.pending=H3` only after `goal_verify.passed=true` AND `platform_debt_clear_for_goal(goal.id)=true`. Reject at H3 → `goal.state=rejected` → re-enter pursuit from last good workflow checkpoint (or workflow-compose if graph stale).

**Effective:** v2.14 (transition), v2.15 (pack field) · **Verify:** `tests/unit/test_goal_keeper_state.py`, pack schema tests

---

## ADR-V2-003 — Platform K ratio (SEC-17-3)

**Decision:** **Adaptive K** with floor **K_min=5**. Each product turn after increment: log `platform.queue_depth` sample. Effective K:

```
K = max(K_min, drain_policy.product_steps_per_platform_turn - floor((depth - boost_queue_depth) / 2))
```

When `depth >= boost_queue_depth`, reduce K (more frequent platform turns). When queue empty, skip platform turn (D3.1). Samples stored in `platform.metrics.queue_depth_samples[]` (ring buffer, max 1000).

**Effective:** v2.16 · **Verify:** `tests/integration/test_platform_interleave.py`

---

## ADR-V2-004 — Budget caps precedence (SEC-17-4)

**Decision:** Three budget surfaces; **first violated wins** (fail-closed stop reason):

| Priority | Surface | Field | Stop reason |
|----------|---------|-------|-------------|
| 1 | Goal | `goal.deadline.max_wall_hours` | `resource.max_wall_hours` |
| 2 | Goal | `goal.deadline.max_steps` | `resource.max_steps` |
| 3 | Goal | `goal.deadline.max_tokens` | `resource.max_cost` |
| 4 | Session | `autopilot.max_steps_per_session` (when mode=`session_autopilot`) | `resource.session_cap` |
| 5 | Platform scheduler | same goal caps bound platform turns per drain (cannot extend goal budget) | same as 1–3 |

`pursuit.budget` mirrors goal caps for display only; **goal.deadline is authoritative**. Uncapped `goal_autopilot` sets `max_steps=null`, `max_tokens=null`; `max_wall_hours` defaults to 48 unless operator sets null at H1 with waiver.

**Effective:** v2.14–v2.15 · **Verify:** `tests/unit/test_budget_caps.py`

---

## ADR-V2-005 — Pack authority (SEC-17-5)

**Decision:** Roles with `role_class ∈ {legal, finance, compliance}` MUST have `automation_allowed: false` → **H2-always** for authority-of-record actions. Other roles default `automation_allowed: true`. Pack CI validator rejects legal/finance with `automation_allowed: true` unless `operator_override_waiver_id` references a row in `automation-waivers.md`.

**Effective:** v2.19 · **Verify:** `tests/unit/test_pack_schema_validate.py`

---

## ADR-V2-006 — Multi-goal preemption (SEC-17-6)

**Decision:** **Phase 1 (v2.15–v2.18):** single active goal; `pursuit.goal_queue` disabled. **Phase 2 (v2.19+):** `company_autopilot` flag enables queue; preemption rules:

1. Same `active_role` contention → higher `goal.priority` wins; tie → FIFO by `goal_queue[].enqueued_at`.
2. Preempted goal → `goal.state=blocked`, `stopped_reason=resource.preempted`, journal note with winner `goal_id`.
3. Role switch completes current workflow **node** before preemption (no mid-node tear-down); if node cannot finish → H2.
4. Lane lease holder finishing work order has **lease priority** over role-queue rotation for that lane only (C4.1).

**Effective:** v2.19 · **Verify:** `tests/integration/test_goal_queue_preemption.py` (add at v2.19)

---

## ADR-V2-007 — Generator-first compose precedence (workflow DAG maximized)

**Decision:** **Agents build generators, not deliverables directly.** Every material output (code, docs, diagrams, 3D assets, data models, configs, test suites) MUST be the typed output of a **workflow DAG terminal node** bound to a transistor (hard, soft, or gate edge). Direct inline implement / prose-only phase execution is forbidden when workflow policy applies.

**Three-layer compose stack (strict precedence — higher layer wins):**

| Layer | Name | When | Rule |
|-------|------|------|------|
| **L3** | Workflow DAG | v2.25+ | `active_workflow` bound; one node per product turn; task card MUST carry `workflow_node_id` + `transistor_id` |
| **L2** | Workflow-compose phase | v2.25+ | No implement/scaffold/build until `validate-workflow-dag.py` passes on `docs/workflows/<goal-id>.json` |
| **L1** | Catalog compose-first | v2.17+ | Each DAG node selects executor via catalog rank (`hard_transistor > script > soft_transistor > playbook > skill`); miss → L0 waiver + promotion enqueue |
| **L0** | Ephemeral waiver | Any | Allowed ONLY with `l0_waiver{rationale, expiry, promotion_queue_id}` on the node; second miss same capability → H2 (E7.4) |

**Catalog compose-first is a sub-step of L2/L3**, not an alternative. The workflow-composer queries the catalog when binding each node's transistor.

**Workflow policy (default `required`):**

| `goal.workflow_policy` | Meaning |
|------------------------|---------|
| `required` (default) | L2+L3 apply to all design/build/implement/test phases |
| `bridge` | v2.17–v2.24 only: L1 compose-first on task cards until v2.25 ships for this repo |
| `exempt` | Operator waiver only (`automation-waivers.md` row + expiry); for harness-evolution (J6) or observe-only |

**Narrow exemptions (no DAG required for this turn):**

- **S0 mechanical:** `route-tier`, `validate-workflow`, `check-pipeline-blocked`, `sync-state`, catalog regen — no LLM deliverable.
- **Coordination-only tasks:** task card `coordination_only: true` (lease acquire/release, manifest merge, journal dual-write) — no artifact output.
- **Operator observe:** A6.3 read-only — does not advance `next_action`.
- **Harness self-build:** J2 waiver-scoped `release-queue.json` items only.

**NOT exempt:** HLD, DD, diagrams, code, assets, pack deliverables, research docs with acceptance artifacts — these are soft or hard transistor nodes in the DAG.

**Innovation thesis:** Decomposing work into verified transistors forces problem breakdown and deep per-part implementation; the agent assembles **generators** (reusable blocks) rather than one-shot artifacts — improving quality and reuse simultaneously.

**Effective:** philosophy from v2.17; enforcement L2 v2.25, L3 v2.26 · **Verify:** `tests/integration/test_workflow_compose_phase.py`, `tests/unit/test_fuzzy_chain_guard.py`, `tests/unit/test_generator_only_deliverables.py` (v2.26)

---

## ADR-V2-008 — Platform debt at goal completion (INTRO-1.3 §5)

**Decision:** `platform_debt_clear_for_goal(goal_id)` returns true iff every promotion item where `source_workflow_id` matches a workflow tied to `goal_id` OR `goal_id` is in item metadata AND `status ∈ {promoted, waived}` AND any waived item has `expiry > now`. Items with `status=pending|draining` block achievement. Global queue items without goal linkage do NOT block (platform debt is goal-scoped).

**Implementation:** `scripts/platform-debt-clear.py --goal <id>` (S0); called from `goal-verify.py` gate 5.

**Effective:** v2.14 · **Verify:** `tests/unit/test_platform_debt_clear.py`

---

## ADR-V2-009 — Writer authority & concurrency

**Decision:** **Conductor is the sole writer** of `journal/state.json`, `journal/progress.md`, and `platform.promotion_queue[]`. Workers (IDE subagents, I2.3 worker-server, I3.3 headless lanes) return artifacts/summaries only. S0 scripts may append `evidence/`, `worker-runs.jsonl`, and lane files atomically with file locks.

**Lane lease:** `program/workstreams/<id>/lane.json` — holder writes via `complete-work-order.py` / `pull-ready-work-orders.py` only. Expired lease → `resource.lease_expired`; conductor may force-release after H2.

**Conflict resolution:** On concurrent edit detection (mtime/hash mismatch on reload): state.json wins over journal; journal wins over snapshot; promotion queue reload from state + journal note (D2.2).

**Effective:** v2.15 (worker audit), v2.18 (I2.3), v2.19 (lanes) · **Verify:** `tests/integration/test_writer_authority.py`, `tests/integration/test_lane_lease_conflict.py`

---

## ADR-V2-010 — Soft transistor runtime

**Decision:** Soft transistors execute via **`scripts/run-soft-transistor.py`** (S0 wrapper): loads `prompt_template_path`, invokes economy worker (`spawn_workers=true`, `capability_class=S1`), validates output against `output_schema` (JSON Schema). Failures: schema mismatch → retry up to `retry_max` → then H2 with evidence path. Soft transistors never dual-write state; conductor merges validated JSON output into workflow node `completed_nodes[]`. `max_tokens` enforced; exceed → `resource.max_cost`.

**Effective:** v2.26 · **Verify:** `tests/unit/test_soft_transistor_executor.py`

---

## ADR-V2-011 — Observability & trace correlation

**Decision:** Every product/platform turn emits a structured log line to `docs/operator/pursuit-trace.jsonl`: `{timestamp, goal_id, workflow_id, node_id, transistor_id, lane_id, stop_reason, evidence_paths[], trace_id}`. `trace_id` = `goal_id` + monotonic step. Dashboard (v2.23+) and v2.28 SLA alerts read from this file + `worker-runs.jsonl`. Webhook payload includes `trace_id` for H2/H3.

**Effective:** v2.23 · **Verify:** `tests/unit/test_pursuit_trace.py`

---

## ADR-V2-012 — Upgrade path (v2.13 → v2.14)

**Decision:** Repos without `goal` block: `check-pipeline-blocked` treats as **bridge mode** — existing task pipeline continues; conductor prompted to run goal-keeper at next H1. Missing blocks = inactive (no crash). First v2.14 session: goal-keeper backfills `goal` from journal TODOS + records `workflow_policy: bridge` until v2.25.

**Effective:** v2.14 pre-flight · **Verify:** `tests/integration/test_v213_upgrade_bridge.py`
