# 03 — Target Architecture

The end-state shapes that every release builds toward. Schemas are **additive to `state.json` version 2**. Sources: vision §10, §19, §20; SEC-18; H1.* and E6/E7 leaves.

---

## 1. `journal/state.json` — target shape (additive)

Existing fields stay. New blocks below are added incrementally by the named release. All blocks are optional until their release ships; tools must treat absence as "feature not yet active," never crash.

```jsonc
{
  "version": 2,

  // --- existing v2.13 fields (unchanged) ---
  "mode": "greenfield",
  "phase": "implement",
  "pipeline_id": "software-greenfield",
  "next_action": "implement-feature (task 3/12)",
  "capability_class": "S2",
  "model_tier": "economy",
  "spawn_workers": true,
  "evidence_required": true,
  "evidence_files": [],
  "last_verify": "passed",
  "program": null,
  "autopilot": { "active": true, "max_steps_per_session": null, "steps_this_session": 0, "stopped_reason": null },

  // --- v2.14: goal model (A1, G2) ---
  "goal": {
    "id": "goal-001",
    "parent_goal": null,
    "type": "app | feature | milestone | company_ops | program",
    "priority": 50,
    "workflow_policy": "bridge | required | exempt",
    "success_criteria": ["..."],
    "verify_command": "python scripts/goal-verify.py --goal goal-001",
    "deadline": { "max_steps": null, "max_tokens": null, "max_wall_hours": 48 },  // max_tokens → stop reason resource.max_cost (alias)
    "state": "pursuing | blocked | verifying | achieved | rejected",
    "verify": { "last_run": null, "passed": false, "exit_code": null, "evidence": [] }
  },

  // --- v2.15: pursuit loop (A2, A3, A4) ---
  "pursuit": {
    "mode": "session_autopilot | goal_autopilot | company_autopilot | sdk_daemon",
    "steps_total": 0,
    "budget": { "max_steps": null, "max_wall_hours": 48 },
    // stopped_reason — canonical dot notation (A4.*); leaf docs may use colons — implement dots only:
    //   human.H1 | human.H2 | human.H3
    //   verify.evidence_fail | verify.goal_verify_fail | verify.regression
    //   resource.max_steps | resource.max_cost (alias of goal.deadline.max_tokens) | resource.max_wall_hours | resource.session_cap | resource.lease_expired | resource.preempted
    //   integrity.validate_fail | integrity.state_corrupt | integrity.artifact_graph_missing | integrity.workflow_stale
    //   completion.goal_achieved | completion.program_done
    // check-pipeline-blocked.py: exit 0 = READY, exit 1 = BLOCKED (A2.1)
    // goal_scope_complete (A2.4): all task cards done + evidence present + promotion_queue drained for goal slice + no blocking_questions → set goal.state=verifying → run goal_verify
    "stopped_reason": null,
    "goal_queue": [],                        // multi-goal / company_autopilot (A3.3, SEC-17-6) — flag-gated
    "active_workflow": null                  // populated in v2.26 (see §3.4 for full shape)
  },

  // --- v2.16: platform queue (D2.2, D3) ---
  "platform": {
    "promotion_queue": [
      {
        "id": "promo-001",
        "source": "task-012 | divergence-log | post-mortem | compose-miss",
        "target_level": "L1..L6",
        "priority": 50,                    // numeric; higher overrides FIFO (D3.2/D3.5)
        "effort_class": "S | M | L",
        "reason": "repeated manual pytest invocation",   // D2.2
        "fingerprint": null,               // dedupe key (G5.6)
        "source_workflow_id": null,        // set when a workflow node misses (E7.4)
        "goal_id": null,                   // goal-scoped debt for platform_debt_clear (ADR-V2-008)
        "node_id": null,                   // missing transistor node (E7.4 / D2.1.5)
        "capability_id": null,             // compose-miss (D2.1.5)
        "suggested_io_schema": null,       // optional I/O hint on compose-miss (D2.1.5)
        "status": "pending | draining | promoted | waived"
      }
    ],
    "drain_policy": {
      "product_steps_per_platform_turn": 5,   // K — D3.1; D5.1 pack-configurable
      "verify_pattern_task_threshold": 3,     // N — D2.1.3; pack-configurable
      "max_backlog_age_steps": 50,            // D3.5 per-item age force-drain
      "boost_queue_depth": 10                 // D3.2
    },
    "composition": { "last_catalog_query": null, "class_mix": null },   // class_mix metrics v2.28
    "metrics": {                                                          // v2.28 dashboard (SEC-15-v2.28, G5.8)
      "fuzzy_chain_incidents": 0,
      "promotion_debt_by_capability": {},   // capability_id → count of pending L0/L1 waivers
      "workflow_coverage_by_pack": {}       // pack_id → % of pack deliverable types with bound workflow templates
    },
    "divergence_log": [   // B4.4 — each entry when compose-first misses:
      // { "timestamp", "searched": [], "compose_failure_reason", "invented_pattern", "promotion_candidate_id" }
      // silent invention without log → conformance fail (blocks pack maturity / SEC-14)
    ]
  },

  // --- v2.15+: minimal HITL state (INTRO-1.2, H1.5) ---
  // H3 pending: hitl.pending = "H3" (also gates_pending); do NOT use separate hitl.h3_pending (A2.5 leaf Behavior contaminated)
  "hitl": {
    "pending": null,                       // ∈ {H1,H2,H3,null}; H3 also reflected in gates_pending (A2.5)
    "since": null,
    "payload": null                        // { goal_id, missing_artifact, suggested_action } for H2 (H1.5)
  },

  // --- v2.15: self-gate mode (SEC-17-1, J3) ---
  "self_gate_mode": "checklist | reviewer | dual_reviewer",   // strict_hitl=true restores human HLD/DD gates

  // --- v2.19: company / pack roles (F1, F6, B5, H1.6) ---
  "company": {
    "pack_id": "game-asset-pipeline",
    "pack_version": "1.0.0",               // H1.6
    "active_role": "technical-artist",
    "role_queue": [],
    "role_forbidden_reads": []             // per-role deny list (F6.2 / F1.1)
  }
}
```

### Field ownership by release
| Block | Release | Skill that writes it | Validator | JSON Schema |
|-------|---------|----------------------|-----------|-------------|
| `goal` | v2.14 | `goal-keeper` | `validate-workflow.py` | [state-goal.v1.json](../docs/platform/schemas/state-goal.v1.json) |
| `pursuit` | v2.15 | `autopilot` / conductor | `check-pipeline-blocked.py` | [state-pursuit.v1.json](../docs/platform/schemas/state-pursuit.v1.json) |
| `hitl` | v2.15 | conductor | `validate-workflow.py` | [state-hitl.v1.json](../docs/platform/schemas/state-hitl.v1.json) |
| `self_gate_mode` (top-level) | v2.15 | conductor | `validate-workflow.py` | [state-self-gate.v1.json](../docs/platform/schemas/state-self-gate.v1.json) |
| `platform` | v2.16 | `playbook-keeper` / conductor | `validate-workflow.py` | [state-platform.v1.json](../docs/platform/schemas/state-platform.v1.json) |
| `program` | v2.19 | `program-scoper` / conductor | `validate-workflow.py` | [state-program.v1.json](../docs/platform/schemas/state-program.v1.json) |
| `company` | v2.19 | `program-scoper` / conductor | `validate-workflow.py` | [state-company.v1.json](../docs/platform/schemas/state-company.v1.json) |
| `pursuit.active_workflow` | v2.26 | `workflow-composer` | `validate-workflow-dag.py` | [state-active-workflow.v1.json](../docs/platform/schemas/state-active-workflow.v1.json) |
| `lane.json` (per workstream) | v2.19 | S0 lease scripts | `validate-workflow.py` | [lane.v1.json](../docs/platform/schemas/lane.v1.json) |

### Legacy top-level vs additive blocks (H1.1, H1.4)

These fields stay **top-level v2.13** — do **not** nest inside `pursuit` (H1.4 Reader is contaminated on placement):

| Field | Owner | Notes |
|-------|-------|-------|
| `next_action`, `phase`, `pipeline_id` | Legacy router (H1.1) | S0-first via `route-tier.py` |
| `capability_class`, `model_tier`, `spawn_workers` | Legacy routing (H1.1) | B1 tier contracts |
| `evidence_required`, `evidence_files`, `last_verify` | Evidence gate (G1, H1.1) | G1.3 latch before advance |
| `gates_pending` | Design gates + H3 (H1.1, H1.5) | `hitl.pending=H3` mirrors here |
| `program`, `autopilot` | Program + session control (H1.1) | `autopilot.active` in preCompact snapshot |

`pursuit` owns only: `mode` (`session_autopilot|goal_autopilot|company_autopilot|sdk_daemon` — **not** `"continue"`), `steps_total`, `budget`, `stopped_reason`, `goal_queue`, `active_workflow`.

### Persistence artifacts (H2–H6)

| Artifact | Role | Master contract |
|----------|------|-----------------|
| **H2** `journal/progress.md` | Human mirror; **state.json wins** on router conflict | Required sections: Goal, Pursuit, Platform, Company, Workflow (H1.7 repair), Evidence files, Resolved Q&A, Session summary |
| **H3** `docs/manifest/staleness.json` + pack `artifact-graph.json` | Design + program + **platform** staleness (v2.18) | `update-staleness.py`; reconcile-stale before merge |
| **H3-SIGNOFF-BUNDLE** | Hierarchy certification bundle (separate from runtime state) | `hierarchy-expander` certify; not part of `state.json` schema |
| **H4** `evidence/` | Immutable per-verify logs | Task evidence (G1) + per-node workflow evidence rollup (G2.5/C6.5 v2.26) |
| **H5** `docs/operator/worker-runs.jsonl` | Append-only subagent spawn audit | Fields: `timestamp, role, model_tier, allowed_reads[], task_id, goal_id, lane_id, outcome`; conductor-only writer; workers forbidden dual-write |
| **H6** preCompact snapshots via `sync-state.py` | Crash/compaction recovery | Fields: `next_action, evidence_files, last_verify, gates_pending, autopilot.active, active_workflow` (v2.26); repair order: **dual-write journal > snapshot > H2**; never chat memory |

**H1.3 queue SoT:** `platform.promotion_queue[]` lives in **`state.json`** (authoritative). `docs/automation/hierarchy-*-queue.json` is hierarchy-tooling only (J6 separation) — not the runtime promotion queue.

**H1.6 company block:** `pack_id`, `pack_version`, `active_role`, `role_queue[]`, `role_forbidden_reads[]` only. Manifest/graph refs live in pack files + `program` block; lane leases in `program/workstreams/<id>/lane.json` (C4.1) — not nested in `company`.

### 1.1 `program` block + lane schema (C4.1, v2.19+)

Top-level `program` (existing v2.13 key) extends additively when `mode=program` or `goal.type=program`:

```jsonc
"program": {
  "manifest_path": "docs/program/integration/manifest.md",
  "artifact_graph_path": "docs/program/integration/artifact-graph.json",
  "milestone_id": "M1",
  "workstreams": [
    {
      "id": "ws-game-art",
      "department": "art",
      "role_id": "technical-artist",
      "lane_path": "program/workstreams/ws-game-art/lane.json",
      "status": "active | blocked | done"
    }
  ],
  "integration_gate": "pending | approved | waived"
}
```

**`program/workstreams/<id>/lane.json`** (lease file — S0 scripts write with atomic replace):

```jsonc
{
  "holder": "conductor | worker-server-<id> | lane-worker-<id>",
  "expires_at": "2026-06-28T12:00:00Z",
  "work_order_path": "docs/program/workstreams/ws-game-art/task-003.md",
  "goal_id": "goal-001",
  "trace_id": "goal-001-step-042"
}
```

Stale or expired lease → `resource.lease_expired` (A4). Lease holder finishing work order has priority over `active_role` rotation for that lane (ADR-V2-006). Manifest/graph paths stay in `program` block — not duplicated in `company`.

**`company_autopilot` enable contract (A3.3, ADR-V2-006):** all three must be true before multi-goal preemption runs:

1. `docs/operator/model-policy.json` → `company_autopilot.enabled: true`
2. `pursuit.mode = company_autopilot`
3. Non-empty `pursuit.goal_queue[]`

Pre-flight at enable: ADR-V2-006 preemption rules acknowledged in journal Resolved Q&A. Preemption sets `stopped_reason=resource.preempted` on the displaced goal; resume when higher-priority goal clears or operator reorders queue at H2.

### 1.2 Writer authority & concurrency (ADR-V2-009)

| Writer | May write | Must not write |
|--------|-----------|----------------|
| **Conductor** | `state.json`, `progress.md`, `promotion_queue[]`, `active_workflow` advances, `hitl`, `goal.state` | — |
| **Workers** (subagents, worker-server) | Nothing in journal/state | Dual-write forbidden (H5 audit) |
| **S0 scripts** | `evidence/*` append, `worker-runs.jsonl` append, `lane.json` via lease APIs, `pursuit-trace.jsonl` append | `state.json` except `sync-state.py` repair path |
| **Operator manual edit** | Any file | Triggers reload + journal note on next S0 preflight; promotion queue reload from state |

**Conflict resolution:** router conflict → **`state.json` wins** over journal → journal wins over H6 snapshot → H2 if irreconcilable. Parallel workflow branches (C6.4): each branch has `lease_owner`; only conductor merges branch completion into `active_workflow.branches[]`.

### 1.3 Budget precedence (ADR-V2-004)

Authoritative caps live in **`goal.deadline`**. Evaluation order each post-step (A2.3): `max_wall_hours` → `max_steps` → `max_tokens` (`resource.max_cost`) → session cap (only in `session_autopilot`). Platform scheduler drains bounded by the **same goal caps** — a platform turn cannot extend goal budget. `pursuit.budget` is a display mirror only.

### 1.4 H3 scope binding (ADR-V2-002)

Pack `company.yaml` **`h3_scope`**: `task | milestone | release | company_goal` (default **`milestone`**). `goal-keeper` at H1 records effective scope in journal Goal section. Partial milestones may H3 per scope without achieving parent program goal.

### 1.5 H1 contract by era (ADR-V2-007, [10](10-implementation-readiness.md))

| Era | H1 must produce |
|-----|-----------------|
| v2.14–v2.24 | Goal + task breakdown + L1 Components plan; `workflow_policy=bridge` unless waiver |
| v2.25+ | + Validated workflow JSON at `docs/workflows/<goal-id>.json` |
| v2.26+ | + `active_workflow` execution binding; generator-only deliverables when `required` |

**Bridge migration:** v2.25 ships `scripts/migrate-bridge-to-workflow.py`; all active goals flip to `required` unless waiver. v2.26 disables bridge by default in state template.

---

## 2. Promotion / reuse-maturity ladder (L0–L6)

| Level | Artifact | Location | Release |
|-------|----------|----------|---------|
| L0 | Ephemeral one-off reasoning | (none — in turn) | exists |
| L1 | Playbook | `docs/playbooks/<slug>.md` + INDEX | v2.16 |
| L2 | Script (S0) | `scripts/<name>.py` | v2.16 |
| L3 | Skill / command | `.cursor/skills/`, `.cursor/commands/` | v2.16 |
| L4 | Ambient (hook, CI, scheduled) | `.cursor/hooks*`, CI workflows | v2.16 |
| L5 | Template-pack fragment | `template-packs/<pack>/...` | v2.19 |
| **L6** | **Transistor** (registered typed-I/O block) | `docs/platform/transistors/<id>.json` | **v2.24** |

**Ranking for compose-first** (E2.3 + E6.5): `hard_transistor > script > soft_transistor > playbook > skill > facts`.

---

## 3. Transistor & generator-workflow model (v2.24–v2.28)

Authority: [SEC-18](../documents/plans/full-automation/SEC-18-transistor-model-a-to-z-reference.md).

### 3.1 Directory layout (net-new)
```
docs/platform/
├── CATALOG.md                      # v2.17 generated umbrella (scripts/list-components.py)
├── TRANSISTORS.md                  # v2.24 generated (scripts/automation/regenerate-transistors-index.py)
├── transistors/<id>.json           # v2.24 transistor manifests (+ bootstrap set, SEC-18 §M)
└── schemas/
    ├── transistor.v1.json          # v2.24
    └── workflow-dag.v1.json        # v2.25
docs/workflows/<goal-id>.json       # v2.25 generator workflow DAGs
docs/automation/release-queue.json  # J6 harness-evolution queue (run-next-release.py, exists)
```

### 3.2 Transistor manifest (`transistor.v1.json`) — fields (E6.2, E6.3, SEC-18 §D)
Common: `id`, semver `version`, `capability_id`, `class` ∈ {`hard`,`soft`,`gate`}, typed `inputs[]`, typed `outputs[]`, S0-evaluable `preconditions[]`, `executor`, `verify` `{kind: "exit_code", expect: 0}` (one verify boundary per block — SEC-17-7), `maturity`, `tags`/`capability_tags`, `provenance` `{queue_id, pack_id}`.
- Typed slots: `string | path | json | artifact_ref | enum` with optional schema `$ref`.
- Breaking output change ⇒ semver fork (D5.3), never silent overwrite.

**Class-specific (E6.3):**
| Class | `executor.kind` | Extra fields | Rule |
|-------|-----------------|--------------|------|
| **hard** | `script` \| `tool` | — | No LLM in block; preferred for all control-adjacent work. |
| **soft** | `soft_template` | `prompt_template_path`, `output_schema`, `max_tokens`, `capability_class: S1` | Bounded LLM with schema-validated output. |
| **gate** | `gate` | `predicate_command` (S0 script **only**) | Edges defined in the DAG, not prose. **Soft gates forbidden.** |

- Steady-state target mix: ~70% hard, ~20% soft, ~10% gate (maturity report v2.28 flags soft-heavy workflows as promotion debt).
- Executor boundary (I4.4): `script | tool | mcp` dispatch is explicit per manifest.

#### 3.2.1 Soft transistor runtime (ADR-V2-010, v2.26)

Soft transistors are **bounded generators**, not free-form chat. Runtime path:

1. **`scripts/run-soft-transistor.py`** (S0) loads manifest + bound inputs from workflow node.
2. Spawns economy worker with `prompt_template_path`; `capability_class=S1`; `max_tokens` enforced.
3. Validates worker output against **`output_schema`** (JSON Schema). Pass → typed output written to evidence + node `completed_nodes[]` (conductor merge). Fail → retry up to `retry_max` → **`human.H2`** with schema diff in `hitl.payload`.
4. Soft transistors **never** dual-write state; **never** bypass `preToolUse` allowlist.
5. Promotion path: repeated soft use for same `capability_id` → enqueue L6 hard extraction (prefer hard executor wrapping the validated template).

Doc/design/3D brief generation uses soft transistors in the DAG — **not** unconstrained phase skills after v2.26.

### 3.3 Generator workflow DAG (`workflow-dag.v1.json`) (C6.2, B6.4, E7.3)
- DAG-level: `workflow_id`, `goal_id`, `template_ref`, `pack_id`, `terminal_nodes[]`, composer audit metadata.
- Node: binds `transistor_id` + `version`; typed `inputs`/`outputs` edges; `retry_max`; `evidence_path_template`; optional `l0_waiver: true` + `rationale` + `expiry` for an unpromoted block (E7.4).
- **Gate node kinds** (B6.4): `verify_result | file_exists | schema_match | budget_remaining | staleness_clear`, emitting pass/fail/retry/H2 edges.
- `validate-workflow-dag.py` (S0) checks **DAG acyclicity**, **gate edge completeness**, every node's `preconditions` **and** postconditions satisfiable from upstream `outputs` **before** implement starts (E7.3); missing typed input on a parallel-branch join fails closed at compose time; **re-run on any DAG edit** before resume.
- Authored by the **`workflow-composer`** S3 skill (SEC-17-8); approved by the conductor at **H1** (B6.2). JSON DAG is authoritative; viewer optional (SEC-17-9).
- Executed **one node per product turn** (B6.3). Compose miss ⇒ enqueue promotion (E7.4 / D2.1.5) + proceed L0 with divergence-log + waiver entry. Transistor version bump mid-pursuit ⇒ `validation_hash` mismatch ⇒ E5.4 re-validate before next node.

### 3.4 `pursuit.active_workflow` block (H1.7) — full shape
```jsonc
"active_workflow": {
  "workflow_id": "wf-goal-001",
  "path": "docs/workflows/goal-001.json",
  "current_node_id": "n3",
  "completed_nodes": [ { "node_id": "n1", "transistor_version": "1.2.0", "evidence": ["evidence/..."] } ],
  "failed_node_id": null,
  "retry_counts": { "n3": 1 },
  "branches": [ { "branch_id": "b1", "current_node_id": "n5", "lease_owner": "lane-2" } ],   // parallel lanes (C6.4); goal_verify waits for all branches to reach terminals
  "terminal_nodes": ["n9"],  // rollup checks (C6.5)
  "validation_hash": "sha256:..."   // last validate-workflow-dag pass
}
```
- Conductor-only dual-writes advances after node verify; product workers read-only. `validate-workflow.py` schema-validates on load; `sync-state.py` repairs partial writes from the journal **Workflow** section after crash.
- Null `active_workflow` allowed **only** before workflow-compose completes **or** for **narrow taxonomy-exempt turns** (S0 mechanical, coordination-only, observe-only, J2 harness waiver — see §5.2). Default for all deliverable-producing goals: **`goal.workflow_policy=required`**.
- Each node's evidence rolls into `goal_verify` (G2.5); failure ⇒ checkpoint replay from `failed_node_id` (G6.4).
- Must appear in `docs/operator/export-contract.md` for headless SDK consumers (J5).

---

## 4. Template-pack = company (target schema)

### 4.1 Pipeline resolution (C1.4)

When `state.company.pack_id` is set:

1. Pack `pipelines/*.yaml` **overrides** harness pipeline for phase order and skill bindings.
2. Phase name collision → **pack wins**; harness phase logged as `superseded_by_pack` in journal Pursuit section.
3. Verify-command conflict between pack and harness → **H2 at H1 (S3)** — not silent merge.

Harness `docs/manifest/pipelines/` remains fallback when no pack is bound.

```
template-packs/<pack>/
├── company.yaml          # see fields below                                  (v2.19)
├── roles/<role>.yaml     # see fields below                                  (v2.19)
├── pipelines/<p>.yaml    # see fields below                                  (v2.19)
├── manifest.md           # integration contracts: artifact types, verify commands, blocking deps   exists
├── artifact-graph.json   # cross-role dependencies                            exists
├── playbooks/            # role-specific procedures                           (v2.19+)
├── tasks/                # seed task cards: Components, Test commands, evidence types, promotion_note stubs, pack_id provenance  (v2.19)
├── verify/               # goal_verify suites per deliverable type (pytest profiles, validate-workflow hooks, checksum tools, meta-tests)  (v2.19)
├── transistors/<id>.json # pack-overlay transistors                          (v2.27)
└── workflows/<wf>.json   # pack generator-workflow templates                 (v2.27)

template-packs/_shared/
├── transistors/<id>.json # org-wide generic blocks (SEC-17-10)               (v2.27)
├── workflows/<wf>.json   # reusable subgraphs ("standard cells")             (v2.27)
└── <micro-pack>/         # cross-pack imports e.g. HR/onboarding              (v2.22)
```

**`company.yaml` fields (F1.1, F5.1, F1.9, SEC-17-2):** `name`, `industry`, `roles[]`, `departments[]`, `default_pipeline`, `pack_version`, `imports[]` (declared import list), `h3_scope` (SEC-17-2), `default_workflow_template` per `pipeline_id` (F1.9).

**`roles/*.yaml` fields (F1.2, F6.2–F6.4, SEC-17-5, B5.2):** `role_id`, `pipeline_id`, `tools`, `permissions`, `kpis`, `handoff_targets`, `allowed_reads`, `forbidden_reads` (deny list), `enabled_skills`, `mcp_allowlist`, `cli_patterns`, `write_scopes`, `pipeline_slice` (subgraph binding), `role_class` (e.g. legal/finance) + `automation_allowed` (SEC-17-5), per-`output_type` evidence rules (F6.4).

**`pipelines/*.yaml` fields (F1.3, C1.4):** `phases`, `phase_order`, `gates` (human gates), `pack_keywords` (program-scoper selection), `skill_bindings`/`default_skills` per phase, `verify_suites`.

- Company instantiation: `program-scoper` reads mega-spec → selects pack (records rationale; operator policy may require **H1 plan approval** before bind when pack-selection risk is high — F2.1) → spawns program with workstream = department/role lane.
- **`active_role` rotation:** switches on **ready unblocked lane work** (not round-robin); complete-work-order + release lease before switch; persists in `state.json` across turns — not a new chat session (F2.3, F6.1).
- **Handoffs:** manifest + artifact-graph prereqs are **S0 mechanical**; ambiguous cross-role merges are **conductor S3** (F2.4).
- Role context switch = `state.company.active_role`; `allowed_reads` scoped to role playbooks + lane tasks; tool permissions per role; **per-`output_type` evidence fail-closed** even if generic task `last_verify` passed (F6.4).
- Reference packs: **game-asset-pipeline** (v2.20) — roles may be **optional/deferred lanes** until milestone (F3.1); **data-platform** (v2.21) — governance role uses **strict_hitl**; deploy **maintenance windows** in pipeline policy (F4.2).
- Cross-pack reuse via `_shared` + pack imports; no repo outside the template-packs ceiling (F5.3); **hotfix** only via pack version bump / import / journal-recorded override — no shadow forks outside ceiling.
- **`_shared` blast radius:** edits to imported micro-packs mark importers stale; extend/fork or H2 when importer goal_verify fails (F5.2).
- **v2.27 overlays:** `default_workflow_template` per pipeline; role `pipeline_slice` binds workflow subgraph; seed cards carry `workflow_node_id` + `transistor_id`; pack CI pre-publish validates `workflows/` + `transistors/` (F1.9, E7.5).

---

## 5. Generator-first composition (workflow DAG maximized)

**North star:** the agent **builds generators and assembles them** — not deliverables directly. Code, documents, diagrams, 3D assets, data models, and configs are **terminal-node outputs** of a verified workflow DAG. This forces decomposition, deep per-part thinking, and reusable transistors — scaling quality and reuse together (ADR-V2-007).

### 5.1 Compose stack (precedence — higher layer overrides lower)

```
L3 Workflow execution (v2.26+)  — one transistor node per product turn; task binds workflow_node_id
L2 Workflow-compose (v2.25+)  — validate-workflow-dag.py PASS before any implement/build/scaffold
L1 Catalog compose (v2.17+)   — per-node executor pick from catalog rank (sub-step of L2/L3, NOT alternative)
L0 Ephemeral waiver           — l0_waiver + promotion_queue_id + expiry; second miss → H2
```

**Catalog compose-first (L1)** runs **inside** workflow-composer when binding each node — resolve capability → `list-components.py` / `list-transistors.py` → rank → bind transistor → on miss, L0 waiver + enqueue. It does **not** authorize skipping the DAG.

### 5.2 Workflow policy & exemptions

| `goal.workflow_policy` | When |
|------------------------|------|
| **`required`** (default at H1) | L2+L3 for all design/build/implement/test phases |
| **`bridge`** | v2.17–v2.24 transitional: L1 on task cards until v2.25 enables L2 for this goal |
| **`exempt`** | Operator waiver in `automation-waivers.md` only (harness J6, observe-only) |

**Narrow turn exemptions (no active_workflow advance required):**

- S0 mechanical (`route-tier`, `validate-workflow`, `check-pipeline-blocked`, `sync-state`, catalog regen)
- Task card **`coordination_only: true`** (lease, manifest merge, journal — no artifact)
- Operator observe (A6.3) — no `next_action` advance
- J2 waiver-scoped harness self-build items

**Never exempt:** HLD, DD, diagrams, implement, external tool outputs, pack deliverables, research with acceptance artifacts — each is a DAG node (hard or soft transistor).

### 5.3 Catalog surface (L1 detail)

- `list-components.py` (S0) scans scripts, playbooks, skills, facts, pipelines, packs, transistors → emits per-source INDEXes + umbrella `docs/platform/CATALOG.md` (E1.7) with **bidirectional cross-links**.
- Query output includes **component type**, **maturity tier**, and path (E1.3, E2.2).
- **Ranking** (E2.3 + E6.5): `hard_transistor > script > soft_transistor > playbook > skill > facts`; gate transistors are **edges**, not rank substitutes. Tie-break: **pack-authored + higher maturity**; skipped ranked choice without divergence log → **H2**.
- **Repeated L0** same capability → promotion priority over re-improvisation (E2.5).
- Librarian returns `suggested_components` + optional `suggested_worker_role` (B4.3/B4.4).

### 5.4 Context layers (E4)

Layer order: **AGENTS.md + always-on rules** (incl. pack rule fragments) → **hooks** inject journal summary + **Context files** on continue/start → session **allowed_reads cap 5** (scope-bleed = G5.2 failure class). AGENTS/rules changes mark dependent playbook/skill nodes stale (E5.2). Corrupt `state.json` on hook read → H2 (A4.4).

### 5.5 Facts, decisions, remember (E3)

- `docs/facts/` = external truth; stale external facts → journal note + optional reconcile-stale (E3.1).
- `docs/decisions/` ADRs; S3 ambiguity → ADR (B1.4); **supersede propagates staleness** to downstream design (E3.2).
- **remember** skill appends to `docs/facts/captured.md`; **no global FTS/vector store**; repeated captures → promotion candidates (E3.3); distinct from journal Resolved Q&A.

### 5.6 Staleness graph (E5)

- Base graph in `docs/manifest/staleness.json`; vision § changes enqueue **hierarchy deepen** items (E5.1).
- Extended nodes: playbooks, scripts, skills/commands, pack nodes, AGENTS (E5.2); **catalog regen reconciles graph**.
- Reconcile outcomes: rerun / waive / **deepen hierarchy queue** — silent implement on stale = contract violation (E5.3).
- Workflow + transistor nodes + `validation_hash`; version bump mid-pursuit → re-validate before next node (E5.4).

---

## 6. Verification immune system (target)

| Layer | Mechanism | Release |
|-------|-----------|---------|
| Task evidence | `verify-router.py` + `evidence_required` + **`last_verify` latch** before advance (G1.3); headless-verify/CI same path (G5.4) | exists |
| Goal verification | `goal-verify.py` aggregates unit+integration+e2e+tool; **regression every implement batch** (G2.4); blocks H3 until pass (G2.3); **dual rollup**: task evidence (C3.4) + per-node `completed_nodes[]` evidence when `active_workflow` bound (G2.5/C6.5) | v2.14, v2.26 |
| Conformance | `validate-workflow.py`, `route-tier --check`, `check-pipeline-blocked` — **scope-complete predicate** (all tasks + evidence) → `goal.state=verifying` → goal_verify, not silent done (G3.3) | v2.14+ |
| Workflow conformance | `validate-workflow-dag.py`; node verify boundary; **fuzzy-chain guard** — implement without `workflow_node_id` blocked at preflight when C6.1 applies; metric `platform.metrics.fuzzy_chain_incidents` (G5.8) | v2.25, v2.26, v2.28 |
| Automated review | security-review on **task-card declared files + diff stats** — default self-gate allows **waivable findings with expiry**; strict packs require pass before git-workflow (G4.1); bugbot on large diffs — supplemental, not evidence substitute; repeat pattern → promotion enqueue (G4.2); S4 escalation on repeated verify fail (G4.3) | v2.23 |
| Mistake→control map | G5.1–G5.8: hallucinated done (evidence gate + **hierarchy audit re-enqueue** on artifactless close), scope creep (allowed_reads + H2 on repeat), wrong arch (self_gate + goal_verify), skipped tests (verify-router mandatory), stale design (reconcile), duplicate tooling (platform queue), unsafe command (**preToolUse deny = fail-closed + journal note**), fuzzy chain (workflow binding) | spread |
| Rollback/recovery | git branch per goal slice (**branch name in journal**); structured H2 digest (G6.2); preCompact snapshot (`next_action, evidence_files, last_verify, gates_pending, autopilot.active, active_workflow`); **checkpoint replay from `failed_node_id`** — graph change forces full restart (G6.4) | v2.15, v2.26 |

### 6.1 Platform debt predicate (ADR-V2-008, INTRO-1.3 §5)

Goal **`achieved`** requires `platform_debt_clear_for_goal(goal_id) == true`:

```python
# scripts/platform-debt-clear.py — S0
def platform_debt_clear_for_goal(goal_id: str) -> bool:
    """True iff no promotion_queue item scoped to goal_id has status pending|draining,
    and every waived item scoped to goal_id has expiry > now."""
```

**Scope:** item matches if `item.goal_id == goal_id` OR `item.source_workflow_id` belongs to `docs/workflows/<goal-id>.json`. Global unscoped queue items do **not** block unrelated goals. Called from `goal-verify.py` as gate 5 of INTRO-1.3.

### 6.2 Production deploy guardrail (APP-A-release, F4.2)

Irreversible production deploy requires a **hard gate transistor** node (`class=gate`, `predicate_command` checks maintenance window + rollback path). Data-platform `pipelines/*.yaml` **`deploy.maintenance_windows`** feeds the predicate. Deploy without gate pass → `integrity.validate_fail`. Pack CI validates deploy pipelines include gate node before publish (v2.21+).

---

## 7. Runtime targets

### I1 — IDE (v2.15+)
- **Genius conductor** (I1.1): model-policy per session; S0-first routing; no inline large implement when `spawn_workers=true` (B3.1).
- **Economy subagents** (I1.2): orchestrate-subagents; parallel spawn only when integration manifest declares independent lanes (C4.2); H5 worker-runs audit.
- **Slash commands** (I1.3): `/continue`, `/autopilot`, `/status`, `/gate`, `/task`, `/verify`, `/lane`, `/program`, `/research`, `/model` — operator control surface; **commands cannot substitute H2 answers or H3 approval** (A5.2, approval-gates).
- **Hooks** (I1.4): `beforeSubmitPrompt`, `subagentStart`, `preToolUse`, `preCompact`, `postToolUse`, `sessionStart` — inject journal + Context files; preCompact snapshot (H6); preToolUse role allowlist (G5.7).

### I2 — SDK daemon (v2.15; I2.3 v2.18)
- **`run-local-pipeline.py`** as 24/7 `goal_autopilot` (I2.1); auth/SDK failure → typed stop, not silent spin.
- **Credentials** (I2.2): `CURSOR_API_KEY`, `AUTOPILOT_MODEL` via env/facts INDEX — never in repo; missing creds → structured H2; model override still obeys `model-policy.json` tiers.
- **Operator PC worker-server** (I2.3): dedicated machine drains lane work orders (C4.1 leases); runs verify/GPU/tool workloads; network partition → H2 with last-known lease; evidence/logs to shared `evidence/` or sync-back; workers do not dual-write journal.

### I3 — Headless/CI (v2.18)
- **`headless-verify.py`** (I3.1): S0/disk-first — no pursuit-router LLM by default; failures set `last_verify` for IDE resume.
- **GitHub Actions** (I3.2): `validate-workflow.py` + verify suite; CI pass is necessary but **not sufficient** for `goal_verify`; CI does not clear H3/design gates.
- **Lane workers** (I3.3): pull-ready / complete-work-order; headless lanes dual-write via S0 scripts only; LLM workers return artifacts for conductor merge.

### I4 — External tools (v2.20; I4.4 v2.26)
- **MCP** (I4.1): per-pack, per-role allowlist (F6.3); browser lock → navigate → unlock discipline; MCP is integration runtime — state transitions remain conductor-owned; auth/rate-limit → H2.
- **tool-operator** (I4.2): Tool command on task cards; cannot edit product source; ad-hoc tool invocation forbidden during evidence-gated implement.
- **Evidence types** (I4.3): checksum, screenshot, manifest, linter logs per `docs/operator/evidence-types.md`; S0 validation when extending types.
- **Transistor executors** (I4.4): `script | tool | mcp` dispatch; soft transistors via bounded workers; executors never bypass `preToolUse` hooks; artifact handoff via typed I/O.

### I5 — Notifications (v2.23)
- **Dashboard** (I5.1): `generate-dashboard.py` → `STATUS.md` + `docs/operator/dashboard.md`; inputs include goal, queue depth, staleness manifest; journal-keeper regen on phase complete.
- **Webhooks/email** (I5.2): H2 digest + H3 pending + milestones; non-blocking (pursuit continues on notify failure); strict environments may disable outbound (dashboard-only); observe-without-unblock (A6.3).

---

## 8. Governance & operator (Plane J)

| Artifact | Role | Key rules |
|----------|------|-----------|
| **J1** `docs/operator/model-policy.json` | Genius/economy tiers, autopilot defaults, `strict_hitl` flag, capability routing | Shared by IDE + SDK (I2.2); `validate-workflow.py` after policy edits before unattended resume |
| **J2** `docs/decisions/automation-waivers.md` | Time-bounded exceptions (verify skip, deferred gates, template self-build) | Fields: operator, rationale, expiry, affected_goal_ids; expired → strict; H3 not permanently waived |
| **J3** `strict_hitl` + `self_gate_mode` | `strict_hitl` in model-policy (default false); `self_gate_mode` in state | Restores HLD/DD human gates; does not disable H1/H2/H3 contract — only self-gate middle approvals |
| **J4** Audit plane | `worker-runs.jsonl`, waiver log, evidence/ immutability | Tamper-evident; retention in operator pack; J4 queries for cost/scope/waiver review |
| **J5** `docs/operator/export-contract.md` | SDK/headless export schema + redaction profiles | Pack may extend profiles; H3 export packages include goal_verify rollup; violation → H2 before egress |
| **J6** `docs/automation/release-queue.json` | Harness evolution backlog (v2.14–v2.28) | **Not** `platform.promotion_queue` (state.json) or hierarchy `*-queue.json`; `run-next-release.py` + `unattended-prompt.md` |

---

## 9. Observability & trace correlation (ADR-V2-011, v2.23+)

| Artifact | Purpose |
|----------|---------|
| **`docs/operator/pursuit-trace.jsonl`** | Append-only per-turn trace: `{timestamp, trace_id, goal_id, workflow_id, node_id, transistor_id, lane_id, phase, stop_reason, evidence_paths[]}` |
| **`docs/operator/worker-runs.jsonl`** | Subagent spawn audit (H5) — correlate via shared `trace_id` |
| **Dashboard / webhooks** | H2/H3 payloads include `trace_id`; v2.28 SLA alerts on `platform.metrics.promotion_debt_by_capability` threshold → webhook (non-blocking) |

**Retention (J4, v2.23+):**

| Artifact | Policy |
|----------|--------|
| `evidence/` | Immutable — no auto-delete |
| `worker-runs.jsonl` | 1 year rotate/archive |
| `pursuit-trace.jsonl` | Rotate at **50 MB or 90 days** (whichever first); **redact secrets at write** |
| Waiver audit rows | Same retention as worker-runs |

`trace_id` = `{goal_id}-step-{pursuit.steps_total}`. Export redaction (J5): strip `payload` secrets; profiles in `export-contract.md`.
