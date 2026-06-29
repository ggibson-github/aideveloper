# 04 — Release Roadmap (v2.14 → v2.28)

Each release is **additive**, dependency-ordered, and has an **exit gate** that must be green before the next begins. Detailed checkboxes live in [06-MASTER-CHECKLIST.md](06-MASTER-CHECKLIST.md); this file is the sequencing + intent overview.

Standing rule for **every** release: update plans/journal, add `validate-workflow.py` checks for new schema, add unit tests for new scripts, run the full test suite, then tag. (Honors `test-before-push`, `evidence-required`, `deterministic-first`.)

---

## Phase 1 — Autonomy core (v2.14–v2.18)

### v2.14 — Goal model + goal_verify
**Intent:** distinguish *task done* from *goal achieved*.
**Deliver:** `state.goal` block; `scripts/goal-verify.py`; `goal-keeper` skill; `check-pipeline-blocked.py` extended to read goal fields and route scope-complete → goal_verify; meta-test that `goal.state=achieved` is impossible without a recorded `goal_verify` exit code.
**Exit gate:** `goal-verify.py` runs on a sample goal; `validate-workflow.py` validates the goal block; unit test `test_goal_verify.py` + `test_goal_keeper` green.
**Leaves:** A1.1–A1.5, A2.4, A4.4, G1.1–G1.3, G2.1–G2.4, G3.1–G3.3, C3.4, C5.1–C5.3, H1.2, H4, INTRO-1.3, APP-B, SEC-15-v2.14.

### v2.15 — Pursuit loop hardening
**Intent:** run until verified; collapse mid-pipeline gates to self-gate.
**Deliver:** `state.pursuit` + `state.hitl`; `goal_autopilot` mode (uncapped option) in autopilot skill + `run-local-pipeline.py`; self-gate for HLD/DD (`strict_hitl=false` default, override in `model-policy.json`/J3); full stop-reason taxonomy in `check-pipeline-blocked.py`; redefined continue semantics in rules.
**Exit gate:** a seeded goal advances multiple phases unattended until a real blocker/H3; stop_reason recorded; strict_hitl toggles gate behavior; tests green.
**Leaves:** A2.1–A2.3, A2.5–A2.7, A3.1–A3.2, A3.4, A4.1–A4.3, A4.5, A5.1–A5.3, B1.1–B1.5, G6.1–G6.3, H1.4–H1.5, H5, H6, I1.1–I1.4, I2.1–I2.2, J1, J3, SEC-13, SEC-15-v2.15.

### v2.16 — Platform queue + scheduler
**Intent:** self-improvement that never starves and never blocks product.
**Deliver:** `state.platform.promotion_queue` + `drain_policy`; enqueue triggers (repeated command 2×, worker flag, verify pattern in N cards, post-mortem); scheduler in autopilot (1 platform turn per K product turns, boost/cut/idle-drain/max-age); task-card **Components** + **Promotion note** fields; promotion ladder L1–L5 wired; platform DoD; populate `docs/playbooks/INDEX.md`.
**Exit gate:** scheduler interleaves a platform turn; a promotion item flows enqueue→drain→catalog row; tests green.
**Leaves:** D1.1–D1.6, D2.1.1–D2.1.4, D2.2–D2.3, D3.1–D3.5, D4.1–D4.6, D5.1–D5.3, D6.1–D6.4, B2.6, B4.1–B4.4, B3.4, C3.1, H1.3, J2, J6, SEC-15-v2.16.

### v2.17 — Catalog & compose-first (L1 of compose stack)
**Intent:** catalog discovery as **sub-step** of future workflow-compose; mandatory component binding before S1+ during bridge mode.
**Deliver:** `scripts/list-components.py` → `docs/platform/CATALOG.md`; librarian `suggested_components`; compose-first rule; rank order; compose-miss → enqueue promotion; **`goal.workflow_policy: bridge`** default until v2.25.
**Exit gate:** `CATALOG.md` regenerates from real repo contents; librarian returns components; a task card shows a Components section sourced from the catalog; tests green.
**Leaves:** E1.1–E1.7, E2.1–E2.5, E3.1–E3.3, E4.1–E4.3, B4.3.

### v2.18 — Staleness graph extension (platform nodes)
**Intent:** traceability across the new platform artifacts.
**Deliver:** extend `staleness.json` + `update-staleness.py` to track playbooks, scripts, skills, pack nodes; `reconcile-stale`/`reconcile-artifact-graph` cover platform nodes.
**Exit gate:** editing a script marks dependent catalog/playbook nodes stale; reconcile plans a re-run; tests green.
**Leaves:** E5.1–E5.3, D6.4, G4.4, G5.5, I3.1–I3.3, I2.3, H3-artifact-graphs, SEC-15-v2.18.

---

## Phase 2 — Organization / company packs (v2.19–v2.23)

### v2.19 — Company pack schema v1
**Deliver:** `company.yaml`, `roles/*.yaml`, `pipelines/*.yaml`, `verify/`, `tasks/` schema + JSON-schema validators; `state.company.active_role` + role_queue; `program-scoper` selects pack; role→pipeline/skill/tool-permission mapping; role-scoped `allowed_reads`; per-role evidence requirements.
**Exit gate:** a pack validates against schema; instantiating it sets `active_role` and routes to the role pipeline; tests green.
**Leaves:** F1.1–F1.8, F2.1–F2.4, F6.1–F6.4, B5.1–B5.4, H1.6, SEC-17-5.

### v2.20 — Game studio pack reference + e2e demo
**Deliver:** full `game-asset-pipeline` pack … end-to-end demo run with **only H1/H3** human interaction; first `tests/e2e/` entries.
**Capability debt window (v2.20–v2.23):** reference packs ship in **bridge mode** — compose-first task cards + phase skills until v2.24–26 transistor layer back-fills domain transistors (SEC-18 §K). Weak initial `goal_verify` allowed with adversarial tightening ADR (F3.4). **Not** an exemption from generator-first after v2.26.
**Exit gate:** demo completes a role-to-role handoff producing evidence; e2e test passes (mock external tools where needed).
**Leaves:** F3.1–F3.4, I4.1–I4.3.

### v2.21 — Data platform pack reference
**Deliver:** full `data-platform` pack (roles: analyst, engineer, DBA, SRE, governance; pipeline ingest→model→deploy→monitor).
**Exit gate:** pack validates + instantiates; representative pipeline runs to evidence; tests green.
**Leaves:** F4.1–F4.2.

### v2.22 — Cross-pack `_shared` library
**Deliver:** `template-packs/_shared/` micro-packs (e.g. HR/onboarding); pack import mechanism; "no repo outside ceiling" enforcement.
**Exit gate:** a pack imports a `_shared` micro-pack and resolves; tests green.
**Leaves:** F5.1–F5.3.

### v2.23 — Operator polish
**Deliver:** H2 notification digests; self-gate audit trail; dashboard shows goal + queue depth; observe-without-unblocking; **`pursuit-trace.jsonl`** trace correlation (ADR-V2-011); webhook payloads include `trace_id`.
**Exit gate:** dashboard renders goal/queue; H2 emits a single digest; audit records waivers; tests green.
**Leaves:** A6.1–A6.3, I5.1–I5.2, G4.1–G4.3, J4, SEC-15-v2.23.

---

## Phase 3 — Transistor & generator workflows (v2.24–v2.28)

### v2.24 — Transistor schema + registry + L6
**Deliver:** `docs/platform/schemas/transistor.v1.json`; `docs/platform/transistors/` + bootstrap transistors; `scripts/automation/list-transistors.py` (incl. `--check-duplicates`, I/O compatibility query); `TRANSISTORS.md`; L6 in ladder; platform work = transistor extraction (D4.7); transistor registry in platform DoD (D6.5); rank update (hard_transistor first).
**Exit gate:** registry validates against schema; `list-transistors.py` lists + detects duplicates; `validate-workflow.py` validates manifests on commit; tests green.
**Leaves:** E6.1–E6.5, D1.7, D4.7, D6.5, SEC-17-7, SEC-17-10, SEC-18, INTRO-2, SEC-15-v2.24.

### v2.25 — Workflow DAG schema + validator + compose phase (L2)
**Intent:** **no implement/build/scaffold until DAG validates** — agents plan generators before executing.
**Deliver:** `workflow-dag.v1.json`; `validate-workflow-dag.py`; `docs/workflows/`; workflow-compose phase **mandatory (default `goal.workflow_policy=required`)**; staleness E5.4; pack pipeline phases become DAG node templates.
**Exit gate:** a sample DAG validates; an invalid wiring (missing typed input) fails closed at compose time; tests green.
**Leaves:** C6.1–C6.2, E7.1–E7.4, E5.4, SEC-17-9, SEC-15-v2.25.

### v2.26 — Workflow composer + active_workflow + one-node-per-turn (L3)
**Intent:** **deliverables only via transistor nodes** — code, docs, diagrams, assets; soft transistors for bounded doc/design generation; fuzzy-chain guard blocks direct implement.
**Deliver:** `workflow-composer` skill; `pursuit.active_workflow`; `run-soft-transistor.py`; conductor approves DAG at H1; one node/turn; gate edges; task binds `workflow_node_id`; evidence rollup; checkpoint replay; export-contract + redaction profiles.
**Exit gate:** a goal runs its DAG one node per turn with active_workflow advancing; a failed node replays from checkpoint; fuzzy-chain guard blocks implement without a node binding; tests green.
**Leaves:** B6.1–B6.4, C6.3, C6.5, H1.7, G2.5, G5.8, G6.4, I4.4, J5, SEC-17-8, SEC-15-v2.26.

### v2.27 — Pack workflow templates + _shared transistors + parallel branches
**Deliver:** pack `workflows/` + `transistors/` overlays inheriting templates (E7.5, F1.9); `_shared` transistors library (F5.4); parallel workflow branches via work orders (C6.4).
**Exit gate:** a pack workflow template instantiates for a goal; a `_shared` transistor resolves via overlay; a parallel branch runs across two lanes; tests green.
**Leaves:** E7.5, F1.9, F5.4, C6.4, SEC-15-v2.27.

### v2.28 — Transistor maturity dashboard + metrics
**Deliver:** transistor maturity dashboard (class mix vs ~70/20/10 target); `platform.metrics` (fuzzy-chain incidents, promotion debt by capability, workflow coverage % per pack); promotion-debt SLA alerts; optional DAG viewer.
**Exit gate:** dashboard reports maturity + fuzzy-chain rate + workflow coverage from real registry/workflows; SEC-18 §Q complete; tests green.
**Leaves:** E6.5 (metrics view), G5.8 (metrics), SEC-15-v2.28.

---

## Release exit-gate template (apply to all)

```
[ ] Schema additions validated by validate-workflow.py
[ ] New scripts have unit tests (tests/unit/) — green
[ ] Cross-phase behavior has integration/e2e tests where applicable — green
[ ] Owning leaves' acceptance criteria all checked in 06-MASTER-CHECKLIST.md
[ ] documents/plans/v2-full-evolution.md + vision §15 row reflect "shipped"
[ ] journal/progress.md + state.json dual-written
[ ] Full test suite green (test-before-push) → tag v2.N
```
