# 02 — Gap Analysis (v2.13 → v2.28)

Vision − [baseline](01-current-state-baseline.md) = the work in this plan. Cross-checked against vision §14 and **281 spec leaves** (+ indexes, H3-SIGNOFF — 348 ledger files).

---

## Gap by capability area

| Area | Today (v2.13) | Target (v2.28) | Owning release(s) | Leaves |
|------|---------------|----------------|-------------------|--------|
| **Pursuit loop** | Autopilot capped 25 steps; default 1 step/turn; design gates hard-stop | `goal_autopilot` until verified; uncapped option; self-gate middle | v2.14, v2.15 | A1–A6, SEC-13 |
| **Goal model** | None — task evidence only | `state.goal` + `goal_verify` meta-test; task→goal rollup | v2.14 | A1, G2, C3.4 |
| **Human gates** | HLD/DD/manifest approvals block | H1 + H3 only; self-gate middle; `strict_hitl` override | v2.15 | A5, J3, INTRO-1.2 |
| **Platform queue** | Optional `playbook-keeper`; empty INDEX | `state.platform.promotion_queue` + scheduler (1/K) + drain policy | v2.16 | D2, D3, B2.6, B4 |
| **Promotion ladder** | Informal L0–L5 in prose | L0–L6 explicit; enqueue triggers; platform DoD | v2.16, v2.24 | D1, D4, D5, D6 |
| **Catalog / compose-first** | Scattered; no discovery surface | `list-components.py` → `CATALOG.md`; compose-first mandatory before S1+ | v2.17 | E1, E2, B4.3 |
| **Staleness graph** | Design nodes only | Extended to playbooks, scripts, pack, workflow, transistor nodes | v2.18, v2.25 | E5, D6.4 |
| **Company packs** | 2 stubs (manifest+graph) | `company.yaml`, `roles/*.yaml`, `pipelines/*.yaml`, `verify/`; `state.company.active_role` | v2.19 | F1, F2, F6, B5, H1.6 |
| **Game studio pack** | Stub | Full role/pipeline reference + e2e demo (H1/H3 only) | v2.20 | F3 |
| **Data platform pack** | Stub | Full role/pipeline reference | v2.21 | F4 |
| **Cross-pack reuse** | None | `template-packs/_shared/` library + pack imports | v2.22 | F5 |
| **Operator polish** | Dashboard greenfield | H2 notifications, self-gate audit, dashboard goal + queue depth | v2.23 | A6, I5, J4 |
| **Transistor registry** | None | `docs/platform/transistors/`, `transistor.v1.json`, `list-transistors.py`, L6 | v2.24 | E6, D1.7, D4.7, D6.5 |
| **Workflow DAG** | None | **Generator-first:** every deliverable = terminal DAG node; compose stack L3→L0; narrow exemptions only | v2.25–v2.28 | C6, E7, ADR-V2-007 |
| **Workflow composer** | None | `workflow-composer` skill, `pursuit.active_workflow`, one-node-per-turn; **no direct deliverable implement** when policy=required | v2.26 | B6, C6.3–C6.5, H1.7, G2.5, G6.4 |
| **Pack workflows** | None | Pack workflow templates inherit; `_shared` transistors; parallel branches | v2.27 | E7.5, F1.9, F5.4, C6.4 |
| **Maturity metrics** | None | Transistor maturity dashboard, fuzzy-chain metrics, optional DAG viewer | v2.28 | G5.8, E6.5 |
| **Tests** | unit only | unit + integration + e2e (pack demos, pursuit loop) | every release | C5.1 |

---

## Gap by plane (what is net-new)

- **A — Pursuit & control:** goal model, pursuit loop semantics, autopilot modes (`goal_autopilot`, `company_autopilot`, `sdk_daemon`), full stop-reason taxonomy, redefined continue, non-blocking notifications. *Mostly new behavior + state, some script extension.*
- **B — Cognition & routing:** keep S0–S4; add platform worker role (B2.6), dual-stack cognition every turn (B4), company role switching (B5), and the S3 workflow-composer (B6). *Rules + skills + state.*
- **C — Product execution:** keep pipelines/phases/tasks; add task→goal rollup (C3.4), and the workflow-compose phase + node binding (C6). *Skills + schema.*
- **D — Platform evolution:** entirely new operational layer — promotion ladder L0–L6, promotion queue, scheduler, work types, extend/fork/configure policy, platform DoD. *State + scripts + scheduler in autopilot.*
- **E — Knowledge & composition:** catalog generation + compose-first protocol; facts/decisions wiring (mostly exists); staleness extension; **transistor registry (E6) + generator-workflow composition (E7)**. *Scripts + docs + schemas.*
- **F — Organization:** full pack schema, company instantiation, two reference packs, cross-pack `_shared`, role→agent mapping. *YAML/JSON schemas + 2 reference packs + state.company.*
- **G — Verification & quality:** keep evidence gates; add **goal-level verification (G2)**, automated review triggers (G4), mistake→control mapping (G5 incl. fuzzy-chain G5.8), rollback/recovery (G6 incl. checkpoint replay). *Scripts + skills + hooks.*
- **H — Persistence & state:** additive state blocks (`goal`, `platform`, `pursuit`, `hitl`, `company`, `active_workflow`); artifact graphs; snapshots/preCompact. *Schema + sync-state.*
- **I — Runtime & integration:** IDE (mostly exists), SDK daemon as first-class, headless/CI, external-tool executors + evidence types, notifications. *Scripts + CI + docs.*
- **J — Governance & operator:** model-policy (exists), automation-waivers (exists), `strict_hitl` flag, audit trail, export-contract (exists), release-queue. *Config + audit.*

---

## What is explicitly NOT changing

- `state.json.version` stays **2** (additive only). No breaking migrations.
- The existing conductor / worker / journal dual-write discipline stays.
- Existing skills keep their contracts; new behavior is added via new skills + state fields, not rewrites.
- The hierarchy/HTML brainstorming toolchain in `scripts/automation/` is left intact.

---

## Sequencing constraints (hard dependencies)

```
v2.14 goal model ──► v2.15 pursuit loop ──► v2.16 platform queue ──► v2.17 catalog/compose-first
                                                          │
v2.17 ──► v2.18 staleness ext ──► v2.19 company packs ──► v2.20 game pack ──► v2.21 data pack ──► v2.22 _shared ──► v2.23 operator polish
                                                                                                                         │
v2.24 transistor registry ──► v2.25 workflow DAG ──► v2.26 composer/active_workflow ──► v2.27 pack workflows ──► v2.28 maturity metrics
```

- v2.24 depends on the catalog/compose-first surface (v2.17) and the platform queue/ladder (v2.16).
- v2.26 depends on the goal model (v2.14) and pursuit loop (v2.15) because workflow nodes roll up to `goal_verify`; **generator-first enforcement** (ADR-V2-007) lands here.
- Company packs (v2.19) depend on the catalog (v2.17); pack workflows (v2.27) depend on both packs (v2.19–v2.21) and the workflow layer (v2.25–v2.26).
