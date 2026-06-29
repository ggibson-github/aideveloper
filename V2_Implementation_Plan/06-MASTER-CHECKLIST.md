# 06 — MASTER CHECKLIST (Work Manifest)

**This is the manifest the agent follows.** Implement releases in order. For each item: build it, run its verification, capture evidence, then tick the box. An item is **not done** until its acceptance command passes. Nothing in a release is complete until its **Exit gate** is green and the full test suite passes (`test-before-push`).

Conventions:
- `[ ]` not started · `[~]` in progress · `[x]` done & verified.
- Each item names the **artifact** and the **leaf ID(s)** it satisfies (traceable to `documents/plans/full-automation/`).
- "Schema additive" = `state.json` stays `version: 2`; tools treat missing blocks as inactive.

---

## Pre-flight (do once, before v2.14)

- [ ] Create `tests/integration/` and `tests/e2e/` directories with `__init__.py` and a README. *(C5.1)*
- [ ] Add a `docs/platform/` directory placeholder + decide schema location `docs/platform/schemas/`.
- [ ] Publish [docs/decisions/v2-evolution-policy-adrs.md](../docs/decisions/v2-evolution-policy-adrs.md) (ADR-V2-001..012); link from [decisions.md](../docs/decisions/decisions.md). *(SEC-17-1..6, architect review)*
- [ ] Record ADR defaults in `journal/state.json` `deferred_questions[]` with `{id, adr_ref, default, override:null, needed_by_release}` — operator H1 override fills `override`. *(SEC-17)*
- [ ] Confirm `validate-workflow.py` has an extension point for new state blocks (add a schema-registry dict if not).
- [ ] Treat [`APP-B-state-json-sketch.md`](../documents/plans/full-automation/APP-B-state-json-sketch.md) as fulfilled by [03-target-architecture.md](03-target-architecture.md) §1 (additive `goal`, `pursuit`, `platform`, `hitl`, `self_gate_mode`, `company`, `active_workflow`); cross-link in `validate-workflow.py` schema registry comments. *(APP-B, H1.*)*
- [ ] **Upgrade path (ADR-V2-012):** document v2.13→v2.14 bridge — missing `goal` block → existing task pipeline continues; goal-keeper backfills at next H1; `goal.workflow_policy: bridge` until v2.25. *(ADR-V2-012)*
- [ ] **CI test matrix** — add `.github/workflows/v2-conformance.yml` (or extend existing): per-release gates — always `validate-workflow.py` + unit; from v2.14 add integration; from v2.18 add headless-verify + lane scripts; from v2.20 add e2e (mock externals); from v2.25 add `validate-workflow-dag.py`. Tag `v2.N` only when matrix green. *(C5.1, architect review)*
- [ ] `tests/integration/test_v213_upgrade_bridge.py` — repo without goal block still runs check-pipeline-blocked. *(ADR-V2-012)*

---

## v2.14 — Goal model + goal_verify

**State schema**
- [ ] Add additive `goal` block to `state.json` template (`id, parent_goal, type, success_criteria[], verify_command, deadline{}, state, verify{}, workflow_policy`). *(A1.1–A1.5, H1.2, ADR-V2-007)*
- [ ] `goal.workflow_policy` enum = `required | bridge | exempt` — default **`bridge`** at v2.14 H1; auto-flip to **`required`** when v2.25 ships unless operator waiver. *(ADR-V2-007)*
- [ ] `goal.state` enum = `pursuing|blocked|verifying|achieved|rejected`. *(A1.5)*
- [ ] `goal.type` enum = `app|feature|milestone|company_ops|program`. *(A1.1)* — type drives preflight routing: milestone→manifest gates, feature→task cards, company_ops→ops queue, program→workstreams.
- [ ] Preflight rejects duplicate `goal.id`, invalid `parent_goal`, and **non-machine-checkable** `success_criteria` (subjective prose) → H2. *(A1.1, A1.2)*
- [ ] goal-keeper at H1 binds each `success_criteria[]` entry to a task-card verify command or script path. *(A1.2)*

**Scripts**
- [ ] `scripts/goal-verify.py` — aggregates unit+integration+e2e+tool results; writes evidence; returns exit code. *(A1.3, G2.1, G2.2)*
- [ ] `scripts/platform-debt-clear.py` — S0 predicate `platform_debt_clear_for_goal(goal_id)` per [03 §6.1](03-target-architecture.md) / ADR-V2-008; called as INTRO-1.3 gate 5 from goal-verify. *(INTRO-1.3, ADR-V2-008)*
- [ ] Extend `scripts/automation/check-pipeline-blocked.py`: exit **0=READY / 1=BLOCKED**; read goal fields; missing goal → H2; **scope-complete predicate** (all tasks done + evidence + no blocking_questions) → set `goal.state=verifying` and route to goal_verify, not another implement step. *(A2.1, A2.4)*
- [ ] Extend `scripts/validate-workflow.py` to validate the `goal` block shape. *(G3.1)*

- [ ] `goal.deadline` budget accounting: pursuit increments steps/tokens/wall-clock via A2.3 post-step; **precedence:** wall_hours → max_steps → max_tokens (`resource.max_cost`) per ADR-V2-004; exceeding caps emits typed resource stop. Plane D scheduler bounded by same goal caps. *(A1.4, A4.3, D3, ADR-V2-004)*
- [ ] `A2.5` transition: when scope-complete, set `goal.state=verifying`; on goal_verify **pass** (incl. platform debt clear), set `hitl.pending=H3` per **`h3_scope`** (ADR-V2-002: default milestone); H3 accept→`achieved`, reject→`rejected`→re-enter pursuit. *(A2.5, ADR-V2-002)* — use `hitl.pending`, not `hitl.h3_pending`.
- [ ] `A4.4` integrity stop: `validate-workflow` fail / corrupt state → `integrity.*` stop reason (not silent continue). *(A4.4)*
- [ ] **INTRO-1.3 completion gate** in `goal-verify.py`/`goal-keeper`: `achieved` requires all 5 — acceptance artifacts, goal_verify pass, staleness consistent, no unresolved blocking_questions, platform debt promoted-or-waived-with-expiry. *(INTRO-1.3)*

**Skills / rules**
- [ ] `.cursor/skills/goal-keeper/SKILL.md` — populates `state.goal` during H1 dual-write; transitions `goal.state`; forbids `achieved` without recorded `goal_verify` exit code. *(A1.*, G2.3)*
- [ ] Add task→goal rollup (% toward goal_verify) to `task-breakdown`/journal-keeper. *(C3.4)*
- [ ] **C5.2 env-setup-first:** task-breakdown orders portable Python/venv/VS solution/repo clone before package-install tasks; validate-workflow or audit flags violations. *(C5.2, AGENTS.md rule 17)*
- [ ] **C5.3 goal-slice DoD:** task-done ≠ goal-done; slice satisfied = tasks complete + evidence + scope-complete predicate ready for goal_verify (INTRO-1.3 five-part gate at goal level). *(C5.3, INTRO-1.3)*
- [ ] `G2.4` regression: `goal-verify.py` runs the regression suite on every implement batch (not just at goal end). *(G2.4)*

**Verification / tests**
- [ ] `tests/unit/test_goal_verify.py` — passes/fails on sample suites; bypass attempt fails. *(G2.3, SEC-15-v2.14)*
- [ ] `tests/unit/test_goal_keeper_state.py` — `achieved` blocked without verify exit code + 5-part gate enforced. *(INTRO-1.3)*
- [ ] `tests/integration/test_goal_scope_complete.py` — scope-complete routes to goal_verify, not "done". *(A2.4)*
- [ ] `tests/unit/test_platform_debt_clear.py` — pending goal-scoped queue item blocks; waived-with-expiry passes; global items don't block unrelated goals. *(ADR-V2-008)*
- [ ] `tests/unit/test_budget_caps.py` — wall→steps→tokens precedence; session cap only in session_autopilot. *(A1.4, A4.3, ADR-V2-004)*

**Exit gate**
- [ ] `python scripts/goal-verify.py --goal <sample>` runs and records exit code in state.
- [ ] `python scripts/validate-workflow.py` green; full unit+integration suite green.
- [ ] Vision §15 v2.14 row + `documents/plans/v2-full-evolution.md` marked shipped; journal dual-written.

---

## v2.15 — Pursuit loop hardening

**State schema**
- [ ] Add `pursuit` block (`mode, steps_total, budget{}, stopped_reason, goal_queue[], active_workflow:null`); **validate legacy fields stay top-level** (`capability_class`, `last_verify`, `evidence_files`, `gates_pending` — not inside pursuit). *(A3, A4, H1.4)*
- [ ] Add `hitl` block (`pending∈{H1,H2,H3,null}, since, payload`). *(INTRO-1.2, H1.5)*
- [ ] Allow `autopilot.max_steps_per_session: null` (uncapped) under goal_autopilot. *(A3.1, A3.2)*

**Scripts**
- [ ] `check-pipeline-blocked.py` emits full **stop-reason taxonomy** (canonical **dot** notation; leaf A4.* colons are aliases only): `human.H1|H2|H3`, `verify.evidence_fail|goal_verify_fail|regression`, `resource.max_steps|max_cost|max_wall_hours|session_cap|lease_expired`, `integrity.validate_fail|state_corrupt|artifact_graph_missing`, `completion.goal_achieved|program_done`. *(A4.1–A4.5)*
- [ ] `run-local-pipeline.py` supports `goal_autopilot` (loop until goal_verify or hard block, no session cap); auth/SDK failure → typed stop (not silent spin). *(A3.2, A3.4, I2.1)*
- [ ] **I2.2** `CURSOR_API_KEY` + `AUTOPILOT_MODEL` via env/facts INDEX (never in repo); missing creds → structured H2; model override obeys tier policy. *(I2.2)*
- [ ] `session_autopilot`: when `autopilot.steps_this_session >= max_steps_per_session`, stop with `resource.session_cap` (A3.1); counter lives on `autopilot.steps_this_session`, not `pursuit.session_step_count`. *(A3.1)*

**Skills / rules / hooks**
- [ ] **I1.1** genius conductor session: model-policy per session; S0-first; orchestrate-only when `spawn_workers=true`. *(I1.1, B3.1)*
- [ ] **I1.2** economy subagents via orchestrate-subagents; parallel spawn gated by C4.2 independent lanes; H5 worker-runs audit. *(I1.2, B1.2)*
- [ ] **I1.3** slash commands (`/continue /autopilot /status /gate /task /verify /lane /program`) ↔ `.cursor/commands/` ↔ skills; **commands ≠ H2/H3 approval**. *(I1.3, A5.2)*
- [ ] `autopilot` skill: add `goal_autopilot` mode; default to it after H1; one skill-phase per iteration. *(A3.2, A5.3)*
- [ ] Update `pipeline-continue.mdc` + `approval-gates.mdc`: "continue" = resume pursuit if not blocked; ≠ approval. *(A5.1, A5.2)*
- [ ] Self-gate for HLD/DD when `strict_hitl=false` (default); strict mode restores human gates. *(A5.2, J3, SEC-17-1)*
- [ ] Add `self_gate_mode` to state (`checklist|reviewer|dual_reviewer`) per ADR-V2-001; risk triggers escalate to reviewer. *(SEC-17-1, G5.3, ADR-V2-001)*
- [ ] **Writer authority:** document in AGENTS.md + conductor rule — workers forbidden dual-write; S0-only lane/evidence append; conflict resolution per ADR-V2-009. *(ADR-V2-009, H5)*
- [ ] **Full hook set (I1.4)** — hooks already exist in `.cursor/hooks.json` (beforeSubmitPrompt, postToolUse, sessionStart, subagentStart, preToolUse, preCompact). Extend behavior:
  - [ ] preCompact → `sync-state.py` snapshot to **`journal/snapshots/`** (fields: `next_action, evidence_files, last_verify, gates_pending, autopilot.active, active_workflow` v2.26); resume from last good dual-write, **never chat memory**; repair order: dual-write journal > snapshot > H2; corrupt → `validate-workflow` fail → H2. *(G6.3, H6)*
  - [ ] **preToolUse allowlist** — block unsafe commands per role tool-permission allowlist; **deny = fail-closed + journal note** (not silent strip). *(G5.7)*
  - [ ] beforeSubmitPrompt/subagentStart → inject journal + allowed_reads context on continue/start. *(E4.2)*
- [ ] `G6.1` git branch per goal slice (**branch name recorded in journal**); `G6.2` structured `last_failure` packaged for H2 digest. *(G6.1, G6.2)*

**Cognition & routing (Plane B — v2.15 foundation)**
- [ ] **B1.1 S0 mandatory-first:** `route-tier.py` → `check-pipeline-blocked.py` → `validate-workflow.py` before any S1–S4 model turn; BLOCKED exit stops routing; script/journal disagreement → H2.
- [ ] **B1.2 S1 economy workers:** catalog picks worker role; `spawn_workers` + economy tier from `model-policy.json`; workers forbidden dual-write; mis-route sets `model_escalation` → H2.
- [ ] **B1.3 S2 templated artifacts:** route `hld-writer`, `dd-writer`, `task-breakdown`, `diagram-generator` at S2; S0 validation after template output; pack templates extend S2 set.
- [ ] **B1.4 S3 genius-only:** trade-offs, merge, ADR/journal closure; one-fact/one-script tasks are NOT S3; external authority of record → S4.
- [ ] **B1.5 S4 H2 packaging:** structured blocker (`goal_id`, missing artifact, operator action); legal/finance pack authority; multi-goal conflict; pairs A4.1 stop taxonomy + A6.2 digest; S4 ≠ “use biggest model”.
- [ ] **B3.1 genius thin turns:** conductor orchestrates only when `spawn_workers=true`; inline large implement = conformance violation.
- [ ] **B3.2 economy bulk scope:** multi-file search, scoped refactors, test fixes on economy tier; escalate to S3 on architecture conflict or missing facts.
- [ ] **B3.3 verify-fail escalation:** classify failure (test/tool/environment/design); retry vs H2 vs refactor task; repeated fail on same task → S4 H2 with evidence paths (see G4.3 v2.23).

**Governance**
- [ ] **J1** extend `docs/operator/model-policy.json`: genius/economy tiers, autopilot defaults, `capability_classes`, routing table; `validate-workflow.py` after policy edits before unattended resume. *(J1, B1.2, I1.1)*
- [ ] Add `strict_hitl` flag to `docs/operator/model-policy.json` (default false) + document in J3; interacts with `self_gate_mode` in state — restores HLD/DD gates, not H1/H2/H3 contract. *(J3)*
- [ ] Map ADR defaults to state slots: SEC-17-2 → pack `h3_scope` + journal; SEC-17-3 → `platform.drain_policy` + adaptive K; SEC-17-4 → `goal.deadline`; SEC-17-6 → `pursuit.goal_queue` (disabled until v2.19). *(SEC-17-2,3,4,6, ADR-V2-003,006)*

**Verification / tests**
- [ ] `tests/unit/test_stop_reasons.py` — every taxonomy branch reachable. *(A4)*
- [ ] `tests/integration/test_goal_autopilot_loop.py` — seeded goal advances ≥3 phases unattended, stops only on real blocker/H3. *(A2.2, A2.3, A2.6, A2.7)*
- [ ] `tests/unit/test_strict_hitl_toggle.py` — toggling re-enables HLD/DD gates. *(J3)*
- [ ] `tests/unit/test_pretooluse_allowlist.py` — unsafe command blocked; allowed command passes. *(G5.7)*
- [ ] `tests/integration/test_precompact_resume.py` — resume from snapshot after simulated crash. *(G6.3, H6)*
- [ ] **`worker-runs.jsonl` audit contract:** conductor logs each spawn (`role, model_tier, allowed_reads, task_id, goal_id, lane_id, outcome`); workers forbidden dual-write; retention in operator pack. *(H5, J4)*

> **Multi-goal / `company_autopilot` (A3.3, SEC-17-6):** ships single pursuit stack now; `pursuit.goal_queue` + `company_autopilot` are flag-gated and land with v2.19 packs. Confirm SEC-17-6 at H1 before enabling.

**Exit gate**
- [ ] Unattended multi-phase advance demonstrated; stop_reason recorded; strict_hitl verified; suite green; docs/journal updated.

---

## v2.16 — Platform queue + scheduler

**State schema**
- [ ] Add `platform` block: `promotion_queue[]` (**authoritative in state.json** — not hierarchy queue JSON; J6 separation), `drain_policy{product_steps_per_platform_turn, verify_pattern_task_threshold, max_backlog_age_steps, boost_queue_depth}`, `composition{}`, `divergence_log[]`, `metrics{}` (v2.28). *(D2.2, H1.3)*
- [ ] Promotion item schema `{id, source, target_level(L1–L6), priority(numeric), effort_class(S|M|L), reason, fingerprint, source_workflow_id, goal_id, node_id, capability_id, suggested_io_schema, status(pending|draining|promoted|waived), waiver_expiry}`; malformed items must not dequeue (S0-validatable). Conductor sole writer; concurrent manual JSON edit → reload + journal note. *(D2.2, E7.4, D2.1.5, ADR-V2-008)*

**Scripts**
- [ ] Scheduler logic in autopilot/`run-local-pipeline.py`: **adaptive K** per ADR-V2-003 (`K = max(K_min, base - floor((depth-boost)/2))`, K_min=5); log `platform.metrics.queue_depth_samples[]`; boost on depth (D3.2); **cut jumps platform ahead** when product blocked on missing tool (D3.3); idle-drain on H2 wait (D3.4); force-drain when oldest item age > max (D3.5); **skip platform turn when queue empty**. *(D3.1–D3.5, ADR-V2-003)*
- [ ] `K` is pack-configurable via task-level params (D5.1); record deferrals in state, never silently skip self-improvement forever. *(D5.1, MASTER-D)*
- [ ] Enqueue triggers: repeated manual command 2× → often L2 (D2.1.1); worker flags repetition with fingerprint dedupe — defer false positive until 2nd flag (D2.1.2); verify pattern on N task cards with sample task ids — N in `drain_policy.verify_pattern_task_threshold` (D2.1.3); conductor post-mortem after escalation (D2.1.4). *(D2.1.*)*
- [ ] `new-task-card.py` adds **Components used** + **Promotion note** fields; v2.26 also adds **workflow_node_id** + **transistor_id** (see C6.3). *(C3.1, C6.3)*

**Promotion ladder & DoD**
- [ ] Document ladder **L0–L6** with locations + promotion rules (L6 capstone deferred detail to v2.24). *(D1.1–D1.7)*
- [ ] Dequeue on platform turn only; product `next_action` untouched; partial promotion → re-enqueue (not false done); optional parallel platform worker slots (B2.6). *(D2.3)*
- [ ] Extend/fork/configure policy: **configure**=task-level params only, **no staleness bump** (D5.1); **extend**=back-compat + staleness bump + parent catalog id + compatibility proof (D5.2); **fork**=new catalog id + provenance, **silent alias forbidden**, explicit task-card migration (D5.3). *(D5.1–D5.3)*
- [ ] Platform DoD checklist: D6.1 INDEX row (maturity + verify ref + promotion id trace); D6.2 verify script (L1 manual OK until scripted, L2+ automated); D6.3 ≥1 task-card ref; D6.4 staleness node wired. *(D6.1–D6.4)*
- [ ] Platform work types via `playbook-keeper` + script extraction (D4.2) + skill/command wrapper (D4.3) + hook+validate ext (D4.4) + **catalog/index regeneration (D4.5)** + pack export (D4.6). *(D4.1–D4.6)*
- [ ] Populate `docs/playbooks/INDEX.md` with the 2 existing playbooks; add platform worker role to orchestration. *(D4.1, B2.6)*

**Dual-stack cognition**
- [ ] Every turn peeks promotion_queue + drain decision; **divergence_log entry schema** `{timestamp, searched[], compose_failure_reason, invented_pattern, promotion_candidate_id}` when compose-first misses; silent invention without log → conformance fail. *(B4.1, B4.2, B4.4)*
- [ ] Platform turns may use economy + S0 (model-policy). *(B3.4)*
- [ ] `docs/automation/release-queue.json` schema wired to existing `scripts/automation/run-next-release.py`. Row fields: `status, branch, plan_todo_id, tag, auto_tag, last_error` + deliverables/verify commands. Tag `v2.x.0` only when `auto_tag: true`. *(J6)*
- [ ] `docs/automation/unattended-prompt.md` — stable instructions for unattended/Cloud harness self-evolution (one release per run, PR/merge chaining). *(J6, existing .cursor/plans recipe)*
- [ ] Harness self-build runs under `mode: iterative_feature` with empty blockers; gate waivers recorded in `docs/decisions/automation-waivers.md` (**template self-build** + structured rows: operator, rationale, expiry, goal_ids; H3 never permanently waived). *(J2, J6)*
- [ ] SEC-17-3 interim: scheduler logs queue-depth samples so K (fixed vs adaptive) can be decided from data. *(SEC-17-3)*

**Verification / tests**
- [ ] `tests/unit/test_platform_queue.py` — enqueue/dequeue/priority + malformed item rejected. *(D2)*
- [ ] `tests/unit/test_drain_scheduler.py` — 1/K, boost, cut, idle, max-age, skip-when-empty. *(D3)*
- [ ] `tests/integration/test_promotion_flow.py` — enqueue→drain→catalog row→staleness node. *(D6)*
- [ ] `tests/integration/test_platform_interleave.py` — **SEC-13 end-to-end**: pursuit step → K-scheduled platform drain → product never starved. *(SEC-13)*

**Exit gate**
- [ ] A promotion item completes the full ladder loop; scheduler interleaves correctly; SEC-13 interleave proven; suite green; docs/journal updated.

---

## v2.17 — Catalog & compose-first

**Scripts / docs**
- [ ] `scripts/list-components.py` (S0) scans + emits per-source indexes: scripts manifest (E1.1), playbooks INDEX (E1.2), skills index (E1.3), facts INDEX (E1.4), pipelines manifest (E1.5), packs README (E1.6) → umbrella `docs/platform/CATALOG.md` (E1.7). *(E1.1–E1.7)*
- [ ] CATALOG.md is generated (regenerable, deterministic) with **bidirectional INDEX cross-links**; Plane D maturity claims require umbrella completeness + staleness coverage. *(E1.7)*
- [ ] Each phase skill declares **front-matter contract**: inputs[], outputs[], verify command, catalog refs[]; missing catalog refs → B4.4 divergence log. Phase verify ≠ goal_verify. *(C2.5)*
- [ ] **E4.1** layer-0 context: AGENTS.md + always-on rules (+ pack rule fragments); AGENTS change → dependent playbook/skill staleness nodes. *(E4.1, E5.2)*
- [ ] Confirm hooks inject journal + **Context files** on continue/start (E4.2); corrupt state → H2; allowed_reads cap 5 retained + scope-bleed class (E4.3). *(E4.2, E4.3, G5.2)*
- [ ] ADR template for unresolved SEC-17 decisions; S3 ambiguity → ADR (B1.4); **supersede → downstream staleness**. *(E3.2)*
- [ ] **E3.3** remember skill: no global FTS/vector store; repeated captures → promotion candidates; distinct from journal Q&A. *(E3.3)*
- [ ] **E3.1** stale external facts → journal note + optional reconcile-stale. *(E3.1)*

**Composition protocol (L1 — sub-step of future L2/L3 per ADR-V2-007)**
- [ ] Compose-first rule (`.cursor/rules/compose-first.mdc`): mandatory before S1+ during **bridge** mode; becomes **per-node binding step** inside workflow-composer at v2.25+. *(E2.1–E2.5, B4.3, ADR-V2-007)*
- [ ] Rule text states: **catalog compose does NOT substitute for workflow DAG** after v2.25; it selects transistors for each DAG node.
- [ ] Rank order `script > playbook > skill > facts` (transistor prepended in v2.24); **tie-break: pack-authored + higher maturity**; rank failure or skipped choice without divergence → H2. *(E2.3)*
- [ ] `list-components` returns **component type + maturity tier** metadata (E2.2); Librarian returns `suggested_components` + optional `suggested_worker_role`. *(E2.2, B2.2)*
- [ ] Compose miss → proceed L0 + enqueue promotion; **repeated L0 same capability → elevate promotion priority**. *(E2.5)*
- [ ] Facts/decisions/remember wiring confirmed (E3); allowed_reads cap 5 retained (E4.3).

**Verification / tests**
- [ ] `tests/unit/test_list_components.py` — catalog reflects real repo contents. *(E1)*
- [ ] `tests/integration/test_compose_first.py` — task card gets Components from catalog; miss enqueues promotion. *(E2)*

**Exit gate**
- [ ] CATALOG.md regenerates; compose-first produces a Components section; miss enqueues; suite green; docs/journal updated.

---

## v2.18 — Staleness graph extension (platform nodes)

- [ ] Extend `docs/manifest/staleness.json` + `update-staleness.py` to track playbooks, scripts, **skills/commands**, pack nodes, **AGENTS/rules**. *(E5.1, E5.2)*
- [ ] Vision § changes enqueue **hierarchy deepen** items; implement blocked on stale design until reconcile. *(E5.1)*
- [ ] **Catalog regen reconciles staleness graph**; optional pack verify asserts graph completeness. *(E5.2)*
- [ ] `reconcile-stale` + `reconcile-artifact-graph` cover platform nodes; outcomes: rerun / waive / **deepen hierarchy queue**; reconcile before merge. *(E5.3, G4.4, G5.5)*
- [ ] CI step (GitHub Actions) runs `validate-workflow.py` + `headless-verify.py` + lane pull/complete work-order checks. *(I3.1, I3.2, I3.3, G3.1)*
- [ ] **I3.1** headless-verify is S0/disk-first (no LLM by default); failures set `last_verify` for IDE resume.
- [ ] **I3.2** CI validates conformance — pass ≠ `goal_verify`; does not clear H3/design gates.
- [ ] **I3.3** headless lane workers: S0-only dual-write; conductor merge path; C4.1 lease semantics.
- [ ] **I2.3 operator PC worker-server:** dedicated machine drains lane work orders; GPU/tool offload; network partition → H2; evidence sync-back to shared `evidence/`. *(I2.3, C4.1)*
- [ ] `tests/unit/test_staleness_platform.py` — editing a script marks dependent nodes stale; reconcile plans re-run.

**Exit gate**
- [ ] Stale propagation + reconcile demonstrated; CI conformance green; suite green; docs/journal updated.

---

## v2.19 — Company pack schema v1

**Schemas / docs**
- [ ] `docs/platform/schemas/company.schema.json` — fields `name, industry, roles[], departments[], default_pipeline, pack_version, imports[], h3_scope, default_workflow_template`. *(F1.1, SEC-17-2, F1.9)*
- [ ] `docs/platform/schemas/role.schema.json` — fields `role_id, pipeline_id, tools, permissions, kpis, handoff_targets, allowed_reads, forbidden_reads, enabled_skills, mcp_allowlist, cli_patterns, write_scopes, pipeline_slice, role_class, automation_allowed, output_type evidence rows`. *(F1.2, F6.2–F6.4, SEC-17-5)*
- [ ] `docs/platform/schemas/pipeline.schema.json` — fields `phases, phase_order, gates, pack_keywords, skill_bindings/default_skills, verify_suites`. *(F1.3, C1.4)*
- [ ] Pack target structure documented: `company.yaml`, `roles/*.yaml`, `pipelines/*.yaml`, `manifest.md`, `artifact-graph.json`, `playbooks/`, `tasks/` (seed cards w/ Components+promotion_note+pack_id+**workflow_node_id/transistor_id** v2.26), `verify/` (goal_verify incl. **C6.5 dual rollup**), `workflows/`+`transistors/` (F1.9 v2.27). *(F1.1–F1.9)*
- [ ] **C1.4 pipeline resolution:** consumer goals inherit pack `pipelines/*.yaml` at instantiation (`program-scoper` + `state.company.pack_id`); harness evolution uses separate `release-queue.json`. Core repo pipelines remain under `docs/manifest/pipelines/`. *(C1.4)*
- [ ] **C4.1 lane lease schema:** `{holder, expires_at, work_order_path}`; stale lease → `resource.lease_expired` stop (A4.3); lanes under `program/workstreams/<id>/lane.json`. *(C4.1)*

**State / routing**
- [ ] Add `company` block (`pack_id, pack_version, active_role, role_queue[], role_forbidden_reads[]`). *(H1.6, B5.1)*
- [ ] role → pipeline_id + skill set + tool permissions (MCP/CLI allowlist) mapping. *(B5.2, F6.1, F6.3)*
- [ ] role-scoped `allowed_reads` **and** `forbidden_reads` deny list (role playbooks + lane tasks). *(F6.2, F1.1)*
- [ ] per-role evidence requirements by output type; **output_type evidence fail-closed** even when generic task verify passed. *(F6.4)*
- [ ] **active_role persists in state.json** across turns (session continuity); mis-mapping role→pipeline = conformance fail. *(F6.1)*
- [ ] complete-work-order before role switch; lease + active_role + workflow-branch ordering. *(F6.3, C6.4)*
- [ ] `program-scoper` selects pack from mega-spec (records rationale); optional **H1 pack-selection gate** when `policy.pack_selection_requires_h1` (F2.1); spawn workstream = department/role lane; **active_role rotates by ready unblocked work** (not round-robin); conductor handoffs: **S0 manifest+graph prereqs vs S3 ambiguous merge** (F2.4). *(F2.1–F2.4, B5.3, B5.4)*
- [ ] Pack authority policy: legal/finance roles `H2-always` unless operator overrides (`role_class`+`automation_allowed`). *(SEC-17-5)*
- [ ] **C4.1 program block schema** in `validate-workflow.py`: `program.workstreams[]`, `lane.json` lease fields; document in [03 §1.1](03-target-architecture.md). *(C4.1, ADR-V2-009)*
- [ ] If `company_autopilot`/multi-goal enabled: ADR-V2-006 preemption rules implemented (not ad-hoc). *(SEC-17-6, A3.3)*

**APP-A work taxonomy → pack authoring**
- [ ] Pack authoring guide maps every APP-A slice to pipeline phases + verify commands + playbooks (not chat-only policy):
  - [ ] **discover** — H1 requirements/research/milestones before design/implement. *(APP-A-discover)*
  - [ ] **design** — machine-checkable UX/API/data/integration/security artifacts linked to catalog. *(APP-A-design)*
  - [ ] **build** — implement/integrate/refactor with evidence; S0/S1 routing; advance only on verify or H2. *(APP-A-build)*
  - [ ] **verify** — unit/integration/E2E/tool/goal_verify/conformance; packs name explicit goal_verify commands. *(APP-A-verify)*
  - [ ] **release** — deploy prep, release-queue, dashboards; irreversible prod requires verify+rollback. *(APP-A-release)*
  - [ ] **organize** — pack instantiation, role queues, `active_role` switching, org-chart simulation. *(APP-A-organize)*
  - [ ] **improve** — platform queue / catalog / harness self-evolution work types. *(APP-A-improve)*

**Verification / tests**
- [ ] `tests/unit/test_pack_schema_validate.py` — valid pack passes, malformed fails. *(F1)*
- [ ] `tests/integration/test_active_role_routing.py` — instantiation sets active_role + routes to role pipeline. *(F2, B5)*
- [ ] `tests/unit/test_role_permission_matrix.py` — tool allowlist + forbidden_reads enforced per role. *(F6.2, F6.3)*
- [ ] `tests/unit/test_output_type_fail_closed.py` — task blocked without role output_type evidence despite generic verify pass. *(F6.4)*
- [ ] `tests/integration/test_goal_queue_preemption.py` — higher priority goal preempts; lease priority respected. *(ADR-V2-006)*
- [ ] `tests/integration/test_writer_authority.py` + `tests/integration/test_lane_lease_conflict.py` — worker cannot dual-write; expired lease stops. *(ADR-V2-009)*
- [ ] `tests/integration/test_handoff_s0_vs_s3.py` — S0 graph prereq vs S3 ambiguous merge paths. *(F2.4)*

**Exit gate**
- [ ] A pack validates + instantiates + routes by role; suite green; docs/journal updated.

---

## v2.20 — Game studio pack reference + e2e demo

- [ ] Build full `template-packs/game-asset-pipeline/`: `company.yaml`, roles (designer, TA, animator, programmer, QA, build, release — **optional/deferred lanes** until milestone OK), pipelines (concept→mesh→rig→anim→UE import→QA→build; **parallel asset lanes** where manifest allows), `verify/`, `tasks/`, role playbooks. *(F3.1, F3.2)*
- [ ] External-tool wiring: Blender, UE, Perforce/Git, CI via `tool-operator` + Tool command + evidence-types. *(F3.3, I4.1–I4.3)*
- [ ] **I4.1** MCP per-role allowlist; browser lock/navigate/unlock; MCP ≠ pursuit router; auth/rate-limit → H2.
- [ ] **I4.2** tool-operator cannot edit product source; ad-hoc tools forbidden during evidence-gated implement.
- [ ] **I4.3** non-pytest evidence types (checksum, screenshot, manifest, linter); S0 validation when extending evidence-types.md.
- [ ] goal_verify suite = asset in engine + tests + performance budget; **initial weak suite acceptable** with adversarial-review tightening schedule (ADR). *(F3.4)*
- [ ] Domain transistors (deferred until v2.24 schema, then back-fill): e.g. `mesh-import`, `rig-humanoid`, `ue-validate`. *(SEC-18 §K)*
- [ ] `tests/e2e/test_game_studio_demo.py` — role-to-role handoff produces evidence with only H1/H3 (mock DCC tools). *(F3, A1.2)*

**Exit gate**
- [ ] e2e demo completes a handoff with evidence; only H1/H3 human points; suite green; docs/journal updated.

---

## v2.21 — Data platform pack reference

- [ ] Build full `template-packs/data-platform/`: roles (analyst, engineer, DBA, SRE, **governance w/ strict_hitl**), pipelines (ingest→model→deploy→monitor; **deploy.maintenance_windows** policy field), verify/tasks/playbooks. *(F4.1, F4.2)*
- [ ] **Deploy gate (bridge until v2.25):** deploy pipeline phase includes task-card checklist for maintenance window + rollback path; v2.25+ becomes hard **gate transistor** node per [03 §6.2](03-target-architecture.md). *(APP-A-release, F4.2)*
- [ ] Domain transistors (back-fill after v2.24): e.g. `ingest`, `dbt-run`, `deploy-check`. *(SEC-18 §K)*
- [ ] `tests/integration/test_data_platform_pipeline.py` — representative pipeline runs to evidence.

**Exit gate**
- [ ] Pack validates + instantiates + runs a pipeline to evidence; suite green; docs/journal updated.

---

## v2.22 — Cross-pack `_shared` library

- [ ] Create `template-packs/_shared/` with ≥1 micro-pack (e.g. HR/onboarding). *(F5.2)*
- [ ] Pack import mechanism (a pack imports a `_shared` micro-pack). *(F5.1)*
- [ ] Enforce "no repo outside template-packs ceiling" (validator/check); **hotfix path**: version bump / import / journal-recorded override only — reject shadow forks. *(F5.3)*
- [ ] **`_shared` blast radius:** importer staleness on _shared edit; extend/fork or H2 when importer goal_verify fails. *(F5.2)*
- [ ] `tests/unit/test_pack_imports.py` — import resolves; missing import fails closed.

**Exit gate**
- [ ] Import resolves end-to-end; ceiling enforced; suite green; docs/journal updated.

---

## v2.23 — Operator polish

- [ ] `generate-dashboard.py` → `docs/operator/dashboard.md` + `STATUS.md` (staleness-aware inputs); optional webhook on milestones (phase complete, H3 pending, goal achieved). Non-blocking — pursuit continues if webhook fails. *(A6.1, I5.1)*
- [ ] H2 notification digest (single digest on blocker with goal_id + stop_reason + suggested action — not per-step). *(A6.2, I5.2)*
- [ ] **I5.2** strict environments may disable outbound notify (dashboard-only); observe-without-unblock (A6.3).
- [ ] **Observe-without-unblock:** reading dashboard/journal/evidence does not clear H2 or gates; explicit operator answer in Resolved Q&A required. *(A6.3)*
- [ ] Self-gate audit trail (who waived what, when) in `docs/decisions/automation-waivers.md` + audit log; evidence/ immutability; retention policy documented. *(J4)*
- [ ] **`docs/operator/pursuit-trace.jsonl`** — append per turn `{timestamp, trace_id, goal_id, workflow_id, node_id, transistor_id, lane_id, phase, stop_reason, evidence_paths[]}`; webhooks include `trace_id` (ADR-V2-011). *(ADR-V2-011, I5.2)*
- [ ] Extend `export-contract.md` redaction profiles: strip secrets from `hitl.payload`, env vars, credentials paths (J5). *(J5)*
- [ ] Automated review triggers: security-review on **task-card declared files + diff stats** (default self-gate: **waivable findings with expiry**; strict packs require pass before git-workflow); bugbot on large diffs (**supplemental, ≠ verify-router**; repeat pattern → promotion enqueue D2.1); S4 escalation on repeated verify fail. *(G4.1–G4.3)*
- [ ] `tests/unit/test_dashboard_goal_queue.py` + `tests/unit/test_h2_digest.py` + `tests/unit/test_pursuit_trace.py`. *(ADR-V2-011)*

**Exit gate**
- [ ] Dashboard renders goal/queue; H2 emits one digest; audit records waivers; review triggers fire; suite green; docs/journal updated.

> **Phase 1+2 milestone:** the autonomous, company-scale delivery system (sans transistors) is now complete. Consider a human checkpoint here.

---

## v2.24 — Transistor schema + registry + L6

**Schemas / docs**
- [ ] `docs/platform/schemas/transistor.v1.json` — common: `id, version(semver), capability_id, class∈{hard,soft,gate}, inputs[], outputs[], preconditions[], executor, verify{kind:exit_code,expect:0}, maturity, tags/capability_tags, provenance{queue_id,pack_id}`. *(E6.2, SEC-18 §D)*
- [ ] Class-specific fields (E6.3): **hard** `executor.kind=script|tool`; **soft** `executor.kind=soft_template` + `prompt_template_path, output_schema, max_tokens, capability_class:S1`; **gate** `executor.kind=gate` + `predicate_command` (S0 script only, **soft gates forbidden**). *(E6.3)*
- [ ] Typed slots `string|path|json|artifact_ref|enum` (+ optional `$ref`). *(E6.2)*
- [ ] `docs/platform/transistors/` with **bootstrap transistor set** (enumerate per SEC-18 §M — e.g. `route-tier-preflight`, `check-pipeline-blocked`, `validate-workflow-run`, `verify-router-invoke`, `dual-write-journal-state`, `list-components-query`, `list-transistors-query`). *(E6.1, SEC-18 §M)*
- [ ] `docs/platform/TRANSISTORS.md` generated. *(E6.1)*

**Scripts**
- [ ] `scripts/automation/list-transistors.py` — list + I/O compatibility query + `--check-duplicates`. *(E6.4, G5.6)*
- [ ] `scripts/automation/regenerate-transistors-index.py` — regenerates `TRANSISTORS.md` from manifests. *(E6.1, SEC-18 §J)*
- [ ] `validate-workflow.py` validates transistor manifests against `transistor.v1.json` on commit; **empty/invalid registry blocks workflow-compose**. *(E6.2, E6.1)*

**Ladder / platform**
- [ ] Add **L6 transistor** as ladder capstone: subsumes L2–L5 executors; L0 must not remain steady state for capability in 2+ workflows; semver on fork/extend (D5.2/D5.3). *(D1.7)*
- [ ] Platform work type: transistor extraction — prefer hard executor from existing L2 script before soft template; `list-transistors --check-duplicates`; D4.5 regen after extraction. *(D4.7)*
- [ ] Platform DoD D6.5: TRANSISTORS.md row + ≥1 workflow JSON ref + `tests/unit/test_transistor_<id>.py` + staleness node (E5.4). *(D6.5)*
- [ ] Compose-first rank prepends `hard_transistor` (then script > soft_transistor > playbook > skill > facts); **gate transistors are edges, not capability substitutes** in rank ladder. *(E6.5, E2.3)*
- [ ] Compose miss = missing transistor → enqueue with `capability_id`/`suggested_io_schema`; product may proceed L0 for that node only (l0_waiver) until L6 minted; repeated miss raises priority. *(D2.1.5, E7.4)*

**Decisions encoded**
- [ ] One verify boundary per transistor. *(SEC-17-7)* · [ ] `_shared` + pack overlay scope. *(SEC-17-10)*

**Verification / tests**
- [ ] `tests/unit/test_transistor_schema.py` — valid/invalid manifests incl. each class. *(E6.2, E6.3)*
- [ ] `tests/unit/test_list_transistors.py` — listing + duplicate detection + I/O query. *(E6.4)*
- [ ] `tests/unit/test_transistors_index_regen.py` — `regenerate-transistors-index.py` deterministic. *(E6.1)*

**SEC-18 §Q acceptance gate**
- [ ] Walk the SEC-18 §Q acceptance checklist (registry + schema validated on CI; compose-first rank prepends hard_transistor; C6.1 applies on the iterative pipeline; bootstrap set present). *(SEC-18 §Q)*

**Exit gate**
- [ ] Registry validates; list/dup-detect + index regen work; manifests validated on commit; rank updated; SEC-18 §Q items checked; suite green; docs/journal updated.

---

## v2.25 — Workflow DAG schema + validator + compose phase

**Schemas / docs**
- [ ] `docs/platform/schemas/workflow-dag.v1.json` — DAG-level `workflow_id, goal_id, template_ref, pack_id, terminal_nodes[]`; node `transistor_id`+version, typed edges, `retry_max`, `evidence_path_template`, optional `l0_waiver{rationale,expiry}`; gate edges pass/fail/retry/H2. *(C6.2, B6.4, E7.4)*
- [ ] `docs/workflows/` storage for `<goal-id>.json` DAGs. *(C6.2)*

**Scripts**
- [ ] `scripts/automation/validate-workflow-dag.py` (S0) — **DAG acyclicity**, **gate edge completeness**, every node's **preconditions and postconditions** satisfiable from upstream outputs; fail closed on missing typed input / parallel-join gap; **re-validate on any DAG edit** before resume. *(E7.3)*
- [ ] `check-pipeline-blocked.py`: **workflow-compose phase mandatory before implement/scaffold/build** (C6.1) when `goal.workflow_policy=required` (default after v2.25) — applies to **all goal types** producing deliverables; **narrow exemptions only:** S0 mechanical, `coordination_only` tasks, observe-only, J2 harness waiver (see [03 §5.2](03-target-architecture.md)). Bridge mode uses L1 on task cards until flip. *(C6.1, ADR-V2-007, SEC-18 §C-9, INTRO-2, H1.7, G5.8)*
- [ ] Add `.cursor/rules/workflow-compose-before-implement.mdc` — states generator-first thesis; forbids direct deliverable implement when policy=required. *(ADR-V2-007)*
- [ ] Extend staleness for workflow + transistor nodes; version bump mid-pursuit → re-validate before next node. *(E5.4)*
- [ ] L0-waiver nodes link to a promotion-queue item with expiry (compose-miss path). *(E7.4)*

**Composition (compose-time — L2)**
- [ ] Resolve deliverable type → workflow template (E7.1); stitch transistors into DAG (E7.2); **each node binds catalog rank (L1)** inside workflow-composer; miss → enqueue transistor promotion (E7.4); **second workflow same unpromoted miss → H2**.
- [ ] Pack `pipelines/*.yaml` phases map to **DAG node templates** (HLD/DD/implement = nodes, not free-form skills). *(C2.5, ADR-V2-007)*

**Decisions encoded**
- [ ] JSON DAG authoritative; visual editor optional. *(SEC-17-9)*

**Verification / tests**
- [ ] `tests/unit/test_validate_workflow_dag.py` — valid DAG passes; missing typed input fails. *(E7.3)*
- [ ] `tests/integration/test_workflow_compose_phase.py` — implement blocked until compose done. *(C6.1)*

**Exit gate**
- [ ] Sample DAG validates; invalid wiring fails closed at compose; compose-before-implement enforced; suite green; docs/journal updated.

---

## v2.26 — Workflow composer + active_workflow + one-node-per-turn

**State schema**
- [ ] Add `pursuit.active_workflow` full shape (`workflow_id, path, current_node_id, completed_nodes[]{node_id,transistor_version,evidence[]}, failed_node_id, retry_counts{}, branches[], terminal_nodes[], validation_hash`). *(H1.7)*
- [ ] Update `docs/operator/export-contract.md` to document `active_workflow` for headless SDK consumers; redaction profiles + pack extensions; H3 export approval; contract violation → H2. *(H1.7, J5)*
- [ ] Extend the preCompact snapshot (v2.15) to include `active_workflow` so DAG position survives compaction/crash. *(G6.3, H1.7)*

**Skills / routing**
- [ ] `.cursor/skills/workflow-composer/SKILL.md` — S3, authors DAG from deliverable decomposition; **queries catalog per node (L1)**; conductor approves at H1. *(B6.1, B6.2, SEC-17-8, ADR-V2-007)*
- [ ] `scripts/run-soft-transistor.py` — ADR-V2-010 runtime: template load → economy worker → JSON Schema validate → evidence; retry_max then H2; never dual-write state. *(E6.3, ADR-V2-010)*
- [ ] Soft transistors used for **doc/design brief nodes** (HLD, DD, diagram spec) — not unconstrained phase skills. *(ADR-V2-007, E6.3)*
- [ ] **Generator-only deliverables:** direct file write / implement without bound node blocked at preflight when `workflow_policy=required`. *(ADR-V2-007, G5.8)*
- [ ] One workflow node per product turn (default). *(B6.3)*
- [ ] Gate transistor edge routing executes, with gate kinds `verify_result | file_exists | schema_match | budget_remaining | staleness_clear`. *(B6.4)*
- [ ] Task card binds `workflow_node_id` **and** `transistor_id`; running outside bound node = conformance failure. *(C6.3)*
- [ ] Executor boundary: script | tool | mcp dispatch; soft transistors via bounded workers; **never bypass preToolUse**; F6.3 role allowlist enforced. *(I4.4, F6.3)*

**Verification & recovery**
- [ ] Per-node evidence rollup → goal_verify. **Coexists with C3.4 task rollup:** goal_verify requires (a) task checklist + evidence (C3.4) AND (b) when `active_workflow` bound, all `terminal_nodes[]` in `completed_nodes[]` with per-node evidence paths (C6.5/G2.5). *(C6.5, C3.4, G2.5)*
- [ ] Checkpoint replay from **`failed_node_id`**; **graph change → full restart** (not partial replay). *(G6.4)*
- [ ] Fuzzy-chain guard: implement without workflow_node_id (when C6.1 applies) blocked at preflight. *(G5.8)*

**Verification / tests**
- [ ] `tests/integration/test_one_node_per_turn.py` — active_workflow advances one node/turn. *(B6.3, H1.7)*
- [ ] `tests/integration/test_checkpoint_replay.py` — failed node replays from checkpoint. *(G6.4)*
- [ ] `tests/unit/test_fuzzy_chain_guard.py` — unbound implement blocked. *(G5.8)*
- [ ] `tests/unit/test_soft_transistor_executor.py` — schema pass/fail/retry/H2 paths. *(ADR-V2-010)*
- [ ] `tests/unit/test_generator_only_deliverables.py` — direct implement blocked when policy=required. *(ADR-V2-007)*

**Exit gate**
- [ ] A goal runs its DAG one node/turn with rollup to goal_verify; replay works; fuzzy-chain guard active; suite green; docs/journal updated.

---

## v2.27 — Pack workflow templates + _shared transistors + parallel branches

- [ ] Pack `workflows/` + `transistors/` overlays inherit templates; **pack CI pre-publish validates workflow + transistor templates**. *(E7.5, F1.9)*
- [ ] `_shared` transistors library under `template-packs/_shared/transistors/` — bootstrap set (e.g. git-commit, verify-pytest, route-tier-preflight, journal-dual-write, scaffold-module). *(F5.4)*
- [ ] `_shared` workflow "standard cells" (reusable subgraphs) under `template-packs/_shared/workflows/`. *(SEC-18 §A, F5.4)*
- [ ] Parallel workflow branches via work orders/lanes (`active_workflow.branches[]`). *(C6.4)*
- [ ] `tests/integration/test_pack_workflow_inherit.py` + `tests/integration/test_parallel_branches.py`.

**Exit gate**
- [ ] Pack workflow template instantiates; `_shared` transistor resolves via overlay; parallel branch runs across lanes; suite green; docs/journal updated.

---

## v2.28 — Transistor maturity dashboard + metrics

- [ ] Maturity dashboard: class mix vs ~70% hard / 20% soft / 10% gate target (from `platform.composition.class_mix`). *(E6.5, E6.3, SEC-18)*
- [ ] Fuzzy-chain metrics in `state.platform.metrics.fuzzy_chain_incidents` (rate of unbound/prose implement). *(G5.8, SEC-15-v2.28)*
- [ ] Promotion debt SLA alert fires webhook when threshold exceeded (reads `platform.metrics.promotion_debt_by_capability`; non-blocking on notify fail). *(SEC-15-v2.28, ADR-V2-011)*
- [ ] Workflow coverage % per pack in `platform.metrics.workflow_coverage_by_pack` (deliverable types with bound templates / total). *(SEC-15-v2.28)*
- [ ] Optional DAG viewer (read-only static HTML from workflow JSON in `docs/platform/`). *(SEC-17-9)*
- [ ] Update `docs/automation/release-queue.json` to reflect the full v2.14–v2.28 history (J6 leaf stopped at v2.23). *(J6)*
- [ ] Walk SEC-18 §Q program-complete acceptance checklist end-to-end. *(SEC-18 §Q)*
- [ ] `tests/unit/test_maturity_metrics.py` — metrics computed from real registry/workflows.

**Exit gate**
- [ ] Dashboard reports maturity + fuzzy-chain rate from real data; release-queue current; SEC-18 §Q complete; suite green; docs/journal updated.

---

## G5 — Mistake → control mapping (verify each control is live)

Each AI failure mode must be neutralized by a named control. Tick when the control exists **and** has a test proving it fires.

- [ ] **G5.1** hallucinated done → evidence gate (`verify-router` + `evidence_required`) + **hierarchy audit re-enqueue deepen** when queue closes without artifacts. *(exists; regression test)*
- [ ] **G5.2** scope creep → `allowed_reads`/`forbidden_reads` cap + task card. *(v2.17/v2.19)*
- [ ] **G5.3** wrong architecture → self-gate checklist/reviewer + goal_verify. *(v2.15)*
- [ ] **G5.4** skipped tests → `verify-router` mandatory before advance. *(exists)*
- [ ] **G5.5** stale design → staleness graph + reconcile before merge. *(v2.18)*
- [ ] **G5.6** duplicate tooling → platform queue + compose-first + `list-transistors --check-duplicates`. *(v2.16/v2.24)*
- [ ] **G5.7** unsafe command → preToolUse hook allowlist per role. *(v2.15)*
- [ ] **G5.8** fuzzy chain lost in prose → workflow-node binding + preflight guard. *(v2.26)*

## Cross-cutting invariants (must hold across all releases)

- [ ] **Generator-first (ADR-V2-007):** after v2.26, deliverables (code, docs, diagrams, assets, configs) are terminal workflow-node outputs — not direct inline implement when `workflow_policy=required`.
- [ ] **Dual-write + resume:** every new state block (`goal`, `pursuit`, `platform`, `company`, `active_workflow`) has a mirror section in `journal/progress.md` (Goal, Pursuit, Platform, Company, **Workflow** for H1.7) and is repairable by `sync-state.py` after crash/laptop-close/concurrent-edit; **state.json wins** on router conflict. *(H1.*, H2, H6, MASTER-D edge cases)*
- [ ] **Writer authority (ADR-V2-009):** conductor sole writer of state/journal/promotion_queue; workers return summaries; S0 scripts append evidence/lanes/trace only.
- [ ] **Fail-closed:** any "claimed done without artifact" (promotion, goal, workflow node, role output) stops at H2, never advances silently. *(D2.2, G2.5, APP-A-improve)*
- [ ] **Platform never blocks product / product never starves platform:** scheduler defers (records) rather than skips; product proceeds while platform drains. *(D3, SEC-13)*
- [ ] **Authority order honored:** when a leaf's Behavior/Release header conflicts with vision §15 / SEC-18 / state-block leaf, the latter wins (see [07](07-traceability-matrix.md) authority note). *(cross-cutting)*
- [ ] **Hierarchy toolchain untouched:** `scripts/automation/` hierarchy/HTML scripts and their tests stay green; harness evolution (`release-queue.json`) is separate from consumer goals. *(J6)*
- [ ] **Stale transistor/workflow re-validation:** any transistor version bump marks the workflow stale (E5.4); pursuit re-runs `validate-workflow-dag.py` before the next node. *(E5.4, H1.7)*

## Final acceptance (vision achieved)

- [ ] All release exit gates green (v2.14–v2.28).
- [ ] [07-traceability-matrix.md](07-traceability-matrix.md) shows **every leaf ID covered** by a checked item.
- [ ] `python scripts/validate-workflow.py` green on full state with all blocks.
- [ ] Full test suite (unit + integration + e2e) green.
- [ ] An end-to-end company-scale goal runs from H1 to H3 using `goal_autopilot`, a composed transistor workflow, platform-queue drain, and pack role rotation — with evidence — and only H1/H2/H3 human interaction.
- [ ] `documents/full-automation-vision-and-hierarchy.md` §15 all rows shipped; `documents/plans/v2-full-evolution.md` complete.
- [ ] STATUS.md + dashboard reflect "vision complete."
