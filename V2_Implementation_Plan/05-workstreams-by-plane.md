# 05 — Workstreams by Plane

Concrete repo changes per plane, mapped from the leaf groups. Use this to understand *where in the codebase* each plane's work lands. The release that ships each item is in brackets. The verifiable checkboxes are in [06-MASTER-CHECKLIST.md](06-MASTER-CHECKLIST.md).

Artifact key: **[S]** script · **[K]** skill · **[C]** command · **[R]** rule · **[H]** hook · **[D]** doc/schema · **[J]** state.json · **[T]** test.

---

## Plane A — Pursuit & control

| Group | Change | Artifacts |
|-------|--------|-----------|
| A1 Goal model | `state.goal` block; goal-keeper populates at H1; **`goal.type` routing**: `milestone`→manifest gates, `feature`→task cards, `company_ops`→ops queue, `program`→workstreams; reject duplicate `goal.id` / invalid `parent_goal` at preflight | [J] goal [K] goal-keeper [v2.14] |
| A2 Pursuit loop | preflight (exit 0=READY/1=BLOCKED); one-step exec; post-step route-tier+dual-write+budget increment; **scope-complete predicate** (tasks done+evidence+no blockers)→`verifying`→goal_verify; loop-until; no mid-loop "waiting for continue" | [S] check-pipeline-blocked.py [K] autopilot [v2.15] |
| A3 Autopilot modes | `session_autopilot` (`autopilot.max_steps_per_session` → `resource.session_cap`); `goal_autopilot` (uncapped); `company_autopilot` (flag v2.19); `sdk_daemon` via run-local-pipeline | [J] pursuit.mode [S] run-local-pipeline.py [v2.15] |
| A4 Stop-reason taxonomy | exhaustive `pursuit.stopped_reason` — dot notation only (see §03 §1 comment); includes `resource.session_cap`, `integrity.artifact_graph_missing` | [S] check-pipeline-blocked.py [J] pursuit.stopped_reason [v2.15] |
| A5 Continue redefined | "continue"=resume if not blocked; ≠ approval; default `goal_autopilot` after H1; self-gate HLD/DD when `strict_hitl=false` | [R] pipeline-continue, approval-gates [v2.15] |
| A6 Notifications | dashboard/STATUS/webhook on milestones; H2 digest (not per-step); observe-without-unblock — **ships v2.23** (A2.5 H3 transition works without webhooks until then) | [S] generate-dashboard.py [K] generate-dashboard [v2.23] |

## Plane B — Cognition & routing

| Group | Change | Artifacts |
|-------|--------|-----------|
| B1 S0–S4 | **S0** mandatory-first (`route-tier`→`check-pipeline-blocked`→`validate-workflow`; BLOCKED stops S1–S4); **S1** economy workers + catalog binding; **S2** templated skills (`hld-writer`, `dd-writer`, `task-breakdown`, `diagram-generator`); **S3** genius ambiguity/merge only; **S4** structured H2 packaging (not “biggest model”) | [S] route-tier.py [R] deterministic-first [v2.15] |
| B2 Roles | conductor (genius, sole dual-writer); librarian (`allowed_reads` max 5, returns `suggested_components` + worker role hint); phase/verifier/reviewer/platform workers | [K] orchestrate-subagents [R] genius-conductor [v2.15–v2.23] |
| B3 Model policy | **Genius thin turns** (orchestrate only, no inline implement when `spawn_workers`); economy bulk search; **verify-fail escalation loop** (classify test/tool/env/design → retry/H2/refactor; repeated fail → S4); platform turns = economy+S0 | [D] model-policy.json [J] model_escalation [v2.15–v2.16] |
| B4 Dual-stack cognition | product turn = one `next_action`; every K turns peek/drain platform queue; compose-first before S1+; **divergence_log** on invention miss | [R] compose-first rule [J] platform.divergence_log [v2.16–v2.17] |
| B5 Company role switching | `active_role` → pipeline/skills/tools; handoff via manifest+graph; conductor fixed, workers swap role context; complete-work-order before role switch | [J] company [K] orchestrate-program [v2.19] |
| B6 Workflow composer (S3) | workflow-composer skill; DAG approved at H1; one node/turn; gate edges (`verify_result\|file_exists\|schema_match\|budget_remaining\|staleness_clear`); soft gates forbidden | [K] workflow-composer [v2.26] |

## Plane C — Product execution

| Group | Change | Artifacts |
|-------|--------|-----------|
| C1 Pipeline registry | 3 core pipelines (`software-greenfield`, `iterative-feature`, `multi-domain-program`) + pack-defined via `pipelines/*.yaml`; `program-scoper` sets `pipeline_id`; pack overrides default at company instantiation | [D] docs/manifest/pipelines + pack pipelines [v2.19] |
| C2 Phase chain | spec→HLD→DD→diagrams→task-breakdown→**workflow-compose (C6.1, v2.25+ — mandatory L2)**→scaffold→implement→test→git; **v2.26+ each phase output is a DAG node**, not free-form skill prose | [K] phase skills → transistor nodes [v2.17 bridge, v2.25+ L2] |
| C3 Task system | task cards: scope, allowed_reads, verify, evidence, **Components**, **promotion_note**, **workflow_node_id+transistor_id (v2.26)**; work orders + lanes; evidence per task; **task rollup (C3.4) + workflow-node rollup (C6.5) both required at goal_verify** | [S] new-task-card.py [K] task-breakdown [v2.16–v2.26] |
| C4 Program/parallel | lane.json `{holder, expires_at, work_order_path}`; orchestrate-program; integration manifest; artifact-graph; complete-work-order before role switch | exists → v2.19 [T] I3.3 CI |
| C5 Feature/app delivery | `src/` + `tests/unit|integration|e2e`; **env-setup tasks ordered before package installs** (C5.2); DoD = goal slice satisfied (tasks+evidence+goal_verify ready), not task-done alone (C5.3) | [K] task-breakdown, scaffold-project [v2.14] |
| C6 Generator workflow exec | **ADR-V2-007:** workflow DAG required (default); compose-first = L1 sub-step; narrow exemptions only; `workflow-dag.v1.json`; one node/turn; parallel branches; terminal evidence → goal_verify | [D] workflow-dag.v1.json [K] workflow-composer [J] active_workflow [v2.25–v2.27] |

## Plane D — Platform evolution

| Group | Change | Artifacts |
|-------|--------|-----------|
| D1 Promotion ladder | L0 ephemeral → L1 playbook → L2 script → L3 skill/command → L4 ambient → L5 pack fragment → **L6 transistor (v2.24)**; L0 steady-state forbidden for capability in 2+ workflows; L6 subsumes L2–L5 executors | [D] ladder doc [v2.16, L6 v2.24] |
| D2 Platform queue | enqueue triggers D2.1.1–1.5 (incl compose-miss L6); item schema L1–L6; dequeue=platform turn only; partial promotion→re-enqueue; conductor sole writer | [J] platform.promotion_queue [v2.16, D2.1.5 v2.24] |
| D3 Scheduling policy | 1/K (`steps_total % K == 0`); boost on depth; **cut jumps platform ahead** when product blocked on missing tool; idle-drain on H2; force-drain on max item age (resets on partial) | [S] autopilot scheduler [v2.16] |
| D4 Work types | playbook-keeper (L1), script extraction (L2, idempotent CLI), skill/command wrapper (L3), hook/validate ext (L4), catalog regen (D4.5), pack export (L5), **transistor extraction prefer hard L2 executor (v2.24)** | [K] playbook-keeper [v2.16, D4.7 v2.24] |
| D5 Extend/fork/configure | **configure**=params only (no staleness bump); **extend**=back-compat + staleness bump + parent id proof; **fork**=new catalog id + provenance, silent alias forbidden | [R]/[D] policy [v2.16] |
| D6 Platform DoD | D6.1 INDEX row; D6.2 verify (L1 manual OK until scripted); D6.3 task-card ref; D6.4 staleness node; **D6.5 TRANSISTORS.md + workflow ref + unit test (v2.24)** | [D] DoD checklist [v2.16, D6.5 v2.24] |

## Plane E — Knowledge & composition

| Group | Change | Artifacts |
|-------|--------|-----------|
| E1 Catalog | generated CATALOG.md umbrella over scripts/playbooks/skills/facts/pipelines/packs; **bidirectional INDEX cross-links**; rows include **maturity tier + component type** metadata | [S] list-components.py [D] CATALOG.md [v2.17] |
| E2 Compose protocol | **L1 of compose stack** (see 03 §5): resolve→query→rank→bind node transistor; sub-step of workflow-composer at v2.25+; bridge mode on task cards v2.17–v2.24 | [R] compose-first [v2.17] |
| E3 Facts & decisions | wire facts/decisions/remember; **no global FTS/vector store**; stale external facts → journal + optional reconcile; **ADR supersede → downstream staleness**; repeated remember captures → promotion candidates | [K] remember [v2.17] |
| E4 Context layers | **layer-0** AGENTS.md + always-on rules (+ pack rule fragments); hooks inject journal + **Context files** on continue/start; corrupt state → H2; **allowed_reads cap 5** tied to G5 scope-bleed | [R] rules + hooks [v2.17] |
| E5 Staleness | extend to playbooks/scripts/skills/commands/pack/AGENTS (v2.18); **vision § changes → deepen enqueue**; catalog regen reconciles graph; reconcile paths: rerun/waive/**deepen**; workflow/transistor nodes (E5.4, v2.25) | [S] update-staleness.py [v2.18, v2.25] |
| E6 Transistor registry | schema, classes, list-transistors, rank; **gate transistors are edges, not capability substitutes** in rank ladder | [D] transistor.v1.json [S] list-transistors.py [v2.24] |
| E7 Workflow composition | deliverable→template, stitch DAG, validate wiring (**acyclicity + gate completeness + re-validate on edit**), miss→enqueue; **second workflow same unpromoted miss → H2**; pack inherit + **CI pre-publish template validation** | [S] validate-workflow-dag.py [v2.25, inherit v2.27] |

## Plane F — Organization (template-packs)

| Group | Change | Artifacts |
|-------|--------|-----------|
| F1 Pack schema | company.yaml, roles, pipelines, manifest, artifact-graph, playbooks, tasks (v2.26 workflow bindings), verify (C6.5 dual rollup); transistors+workflows (F1.9) + APP-A slice mapping | [D] pack schemas [v2.19, F1.9 v2.27] |
| F2 Company instantiation | program-scoper selects pack (optional **H1** when policy requires); workstream=dept/role lane; **ready-work rotation** (not round-robin); **S0 mechanical vs S3 ambiguous** handoffs via manifest+graph | [K] program-scoper [v2.19] |
| F3 Game studio pack | full reference + e2e; **optional/deferred role lanes**; parallel asset lanes; weak goal_verify OK initially with adversarial tightening | [D] template-packs/game-asset-pipeline [v2.20] |
| F4 Data platform pack | full reference; **maintenance-window deploy blocks**; governance **strict_hitl** role | [D] template-packs/data-platform [v2.21] |
| F5 Cross-pack | imports, _shared library, ceiling enforcement; **hotfix via version/import/journal override** (no shadow forks); _shared blast-radius → extend/fork or H2; _shared transistors + workflow cells (F5.4) | [D] template-packs/_shared [v2.22, F5.4 v2.27] |
| F6 Role→agent mapping | **active_role persists in state.json** across turns; scoped reads; tool perms; **output_type evidence fail-closed** even if generic verify passed; mis-mapping = conformance fail | [J] company [R] role rules [v2.19] |

## Plane G — Verification & quality

| Group | Change | Artifacts |
|-------|--------|-----------|
| G1 Evidence gates | verify-router + `evidence_required` + `last_verify` latch before advance; cross-ref G6.3 snapshot | exists |
| G2 Goal-level verify | goal_verify aggregates unit+int+e2e+tool; **regression every implement batch** (G2.4); blocks H3; **dual rollup** task + per-node evidence (G2.5/C6.5) | [S] goal-verify.py [v2.14, G2.5 v2.26] |
| G3 Conformance | validate-workflow, route-tier --check, check-pipeline-blocked; **scope-complete→verifying→goal_verify** predicate; validate-workflow-dag (v2.25) | [S] validate-workflow.py [v2.14] |
| G4 Review triggers | security-review on **declared files + diff stats** (waivable w/ expiry under self-gate); bugbot on large diffs (**≠ verify-router**; repeat→promotion enqueue); S4 escalation; staleness reconcile before merge | [H]/[K] review [v2.23] |
| G5 Mistake→control | G5.1–G5.8 mapped; **hierarchy audit re-enqueue** on artifactless close; G5.8 fuzzy-chain preflight + v2.28 metrics | [R]/[H] [v2.16–v2.28] |
| G6 Rollback/recovery | git branch per slice (**journal branch name**); structured H2; preCompact snapshot incl. **active_workflow**; **checkpoint replay from failed_node_id** (graph change → full restart) | [H] preCompact [v2.15, G6.4 v2.26] |

## Plane H — Persistence & state

| Group | Change | Artifacts |
|-------|--------|-----------|
| H1 state.json blocks | … **program block schema** (§03 §1.1) · writer authority ADR-V2-009 | [J] [S] sync-state.py, validate-workflow.py [v2.14–v2.26] |
| H2 progress.md | human mirror + session summary; **required sections** per state block; state.json wins on conflict | [K] journal-keeper |
| H3 Artifact graphs | design+program+**platform** staleness (skills, AGENTS v2.18); SIGNOFF-BUNDLE = hierarchy certify (separate) | [S] update-staleness.py [v2.18] |
| H4 evidence/ | immutable task + **workflow node** evidence logs (dual rollup v2.26) | exists |
| H5 worker-runs.jsonl | spawn audit schema (role, tier, allowed_reads, goal/lane correlation); conductor-only | [J] worker-runs contract [v2.15] |
| H6 Snapshots | preCompact → sync-state.py; field list incl. active_workflow; repair precedence dual-write > snapshot > H2 | [H] preCompact [v2.15, v2.26] |

## Plane I — Runtime & integration

| Group | Change | Artifacts |
|-------|--------|-----------|
| I1 IDE | genius conductor (I1.1) + economy subagents (I1.2, C4.2 parallel gate); slash commands `/continue /autopilot /status /gate /task /verify /lane /program` — **commands ≠ H2/H3 clearance** (I1.3); full hook set incl. postToolUse/sessionStart (I1.4) | [H] [v2.15+] |
| I2 SDK daemon | I2.1 goal_autopilot via run-local-pipeline; I2.2 CURSOR_API_KEY/AUTOPILOT_MODEL (secrets via facts, structured H2 on auth fail); **I2.3 operator PC worker-server** (lane leases, GPU/tool offload, evidence sync-back) | [S] run-local-pipeline.py [v2.15, I2.3 v2.18] |
| I3 Headless/CI | headless-verify **S0/disk-first** (no LLM default); CI validates conformance **≠ goal_verify / H3**; headless lanes **S0-only dual-write** + conductor merge (I3.3) | CI workflows [v2.18] |
| I4 External tools | I4.1 MCP per-role allowlist + browser lock/navigate/unlock; I4.2 tool-operator (no product-source edits); I4.3 non-pytest evidence types; **I4.4** executor script/tool/mcp + soft path, preToolUse non-bypass | [K] tool-operator [v2.20, I4.4 v2.26] |
| I5 Notifications | dashboard + STATUS; webhook/email H2/H3 + milestones; **`pursuit-trace.jsonl`** correlation (ADR-V2-011); v2.28 SLA alert on promotion debt | [S] generate-dashboard.py [v2.23] |

## Plane J — Governance & operator

| Group | Change | Artifacts |
|-------|--------|-----------|
| J1 model-policy.json | genius/economy tiers, autopilot defaults, `capability_classes`, routing table; **validate-workflow after policy edit** | [D] `docs/operator/model-policy.json` [v2.15] |
| J2 automation-waivers | **template self-build (v2.16)** + structured waiver rows (operator, rationale, expiry, goal_ids); H3 never permanently waived; expiry → strict behavior | [D] `docs/decisions/automation-waivers.md` |
| J3 strict_hitl flag | flag in **model-policy.json** (not state.hitl alone); restores HLD/DD human gates via `self_gate_mode`; pack governance roles may force strict | [J]/[D] [v2.15] |
| J4 audit | worker-runs.jsonl + waiver/self-gate audit trail; evidence immutability; retention policy | [D] audit log [v2.15, v2.23] |
| J5 export-contract | state/evidence export; **redaction profiles** + pack extensions; H3 export approval; `active_workflow` + trace_id fields; secrets never exported | [D] `docs/operator/export-contract.md` |
| J6 release-queue.json | **harness evolution only** (separate from platform.promotion_queue + hierarchy queues); v2.14–v2.28 rows; run-next-release.py + unattended-prompt | [D] [S] `docs/automation/release-queue.json` [v2.16, v2.28] |

---

## Phase skill → transistor migration (ADR-V2-007)

| Phase skill | v2.24 action | v2.26 action |
|-------------|--------------|--------------|
| `hld-writer`, `dd-writer`, `diagram-generator` | Wrap as **soft transistor** templates under `docs/platform/transistors/` | DAG node only; skill invoked only via `run-soft-transistor.py` |
| `implement-feature` | Decompose into workflow templates + hard transistors | **Forbidden** as direct `next_action` when `workflow_policy=required` |
| `task-breakdown` | Emits task cards **with** `workflow_node_id` placeholders | Binds to DAG compose output |

Verify: `tests/unit/test_phase_skill_routing_forbidden.py` (v2.26). Bootstrap minimum set: [bootstrap-transistors.manifest.json](../docs/platform/bootstrap-transistors.manifest.json).
