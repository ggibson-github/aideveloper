# 08 — Coverage ledger (brainstorming → master plan)

**Total source files tracked: 348** (every `.md` under `documents/`, excluding the generated `html-site/` payload).

**Status semantics:** Rows marked `[x]` mean **plan-covered** — the source idea is traced into master plan docs (`00`–`10`). They do **not** mean the feature is implemented in the repo. Implementation progress lives in [06-MASTER-CHECKLIST.md](06-MASTER-CHECKLIST.md). Read [10-implementation-readiness.md](10-implementation-readiness.md) before conflating the two.

## How to use this ledger

Iterate in batches. For each file, **read it**, confirm its ideas are reflected in the master plan (`00`–`10`) **verbosely and clearly**, enrich the plan where the source implies an important addition, then mark the row:

- `- [ ]` pending — not yet plan-verified
- `- [x] PATH — §<plan file/section>: <one-line note>` **plan-covered** (cite where the idea now lives; note any enrichment)

Future optional suffix: `impl-verified` when the matching [06](06-MASTER-CHECKLIST.md) checkbox passes its verify command.

Keep the per-group counts and the progress line at the bottom up to date as rows are checked.

---

## 00 Root design docs (4)

- [x] `documents/full-automation-vision-and-hierarchy.md` — §00 (north star, 4 shifts, HITL, completion, scope, 10 planes); whole plan derives from it.
- [x] `documents/genius-conductor-tiered-routing.md` — §01 baseline (S0–S4, three-layer stack, escalation loop, model-policy); confirmed v2.4–v2.13 baseline.
- [x] `documents/plans/v2-full-evolution.md` — §01 baseline + §04 roadmap appends after v2.23 row.
- [x] `documents/spec-to-artifacts-agent-skills-system.md` — §01 baseline (journal schema, gates, env-setup-first, spec-change/staleness); confirmed v1/v2 baseline.

## 01 INTRO (north star) (6)

- [x] `documents/plans/full-automation/INTRO-0-executive-summary---0.md` — §00 north star + four structural shifts.
- [x] `documents/plans/full-automation/INTRO-1.1-100--automation-scope-in-out.md` — §00 "Scope: in vs out" table (incl. irreversible-prod, silent-waiver, aesthetic-as-tests).
- [x] `documents/plans/full-automation/INTRO-1.2-human-touchpoint-contract-h1-h2-h3.md` — §00 HITL contract (H1 once/instantiation; H2 async pause/resume; H3 reject→re-enters pursuit; else self-gate w/ evidence).
- [x] `documents/plans/full-automation/INTRO-1.3-goal-completion-criterion.md` — §00 five-part completion + stop set; gated §06 v2.14 (goal-verify all five).
- [x] `documents/plans/full-automation/INTRO-2-transistor-building-blocks-north-star.md` — §00 4th shift + §03 transistor model; compose-before-implement scope.
- [x] `documents/plans/full-automation/INTRO-index.md` — index only; all 5 children covered above.

## 02 APP (appendices) (9)

- [x] `documents/plans/full-automation/APP-A-build-work-taxonomy-build.md` — §06 v2.19 APP-A build slice (implement/integrate/refactor, evidence, S0/S1 routing).
- [x] `documents/plans/full-automation/APP-A-design-work-taxonomy-design.md` — §06 v2.19 APP-A design slice (machine-checkable artifacts, catalog links).
- [x] `documents/plans/full-automation/APP-A-discover-work-taxonomy-discover-and-plan.md` — §06 v2.19 APP-A discover slice (H1, milestones, machine-checkable before design).
- [x] `documents/plans/full-automation/APP-A-index.md` — index only; all 7 APP-A slices covered in §06 v2.19.
- [x] `documents/plans/full-automation/APP-A-organize-work-taxonomy-organize-company.md` — §06 v2.19 APP-A organize slice + §03 company/roles (active_role, org simulation).
- [x] `documents/plans/full-automation/APP-A-release-work-taxonomy-release-and-operate.md` — §06 v2.19 APP-A release slice + §06 v2.16 J6 release-queue; irreversible-prod guard in §00.
- [x] `documents/plans/full-automation/APP-A-verify-work-taxonomy-verify.md` — §06 v2.19 APP-A verify slice + §06 v2.14 goal_verify.
- [x] `documents/plans/full-automation/APP-B-state-json-sketch.md` — §03 §1 full additive schema (APP-B leaf is stub; enriched §06 pre-flight cross-link).

## 03 MASTER (branch summaries) (11)

- [x] `documents/plans/full-automation/MASTER-A-branch-a---pursuit---control-plane.md` — §05 Plane A + §04 v2.14–v2.15 (goal model, pursuit loop, stop taxonomy).
- [x] `documents/plans/full-automation/MASTER-B-branch-b---cognition---routing-plane.md` — §05 Plane B + §06 v2.15–v2.17 (S0–S4, conductor, platform interleave).
- [x] `documents/plans/full-automation/MASTER-C-branch-c---product-execution-plane.md` — §05 Plane C + §06 v2.25–v2.27 (pipelines, task cards, C6 workflow layer).
- [x] `documents/plans/full-automation/MASTER-D-branch-d---platform-evolution-plane.md` — §05 Plane D summary (promotion ladder L0–L6, platform queue) + §02 gap.
- [x] `documents/plans/full-automation/MASTER-E-branch-e---knowledge---composition-plane.md` — §05 Plane E + §06 v2.17–v2.18, v2.24+ (catalog, compose-first, transistors).
- [x] `documents/plans/full-automation/MASTER-F-branch-f---organization-plane.md` — §05 Plane F + §06 v2.19–v2.22 (packs, roles, reference packs, _shared).
- [x] `documents/plans/full-automation/MASTER-G-branch-g---verification---quality-plane.md` — §05 Plane G + §06 G5 mistake map (evidence, goal_verify, rollback).
- [x] `documents/plans/full-automation/MASTER-H-branch-h---persistence---state-plane.md` — §05 Plane H + §03 §1 state blocks (incl. active_workflow v2.26 via H1.7).
- [x] `documents/plans/full-automation/MASTER-I-branch-i---runtime---integration-plane.md` — §05 Plane I + §06 v2.15 hooks, v2.18 CI, v2.26 executors.
- [x] `documents/plans/full-automation/MASTER-J-branch-j---governance---operator-plane.md` — §05 Plane J + §06 v2.15 J3, v2.16 J6, v2.23 audit.
- [x] `documents/plans/full-automation/MASTER-index.md` — index only; all 10 plane masters covered in §05.

## 04 SEC-13 pursuit flow (1)

- [x] `documents/plans/full-automation/SEC-13-pursuit-flow.md` — §04 v2.15 pursuit loop + §06 v2.16 SEC-13 platform-interleave acceptance test.
- [x] `documents/plans/full-automation/SEC-14-gap-analysis.md` — §02 gap analysis (authoritative counterpart; source Behavior contaminated).

## 05 SEC-15 release rows (16)

- [x] `documents/plans/full-automation/SEC-15-index.md` — index only; mirrors §04 release roadmap v2.14–v2.28.
- [x] `documents/plans/full-automation/SEC-15-v2.14-release-v2-14-goal-model-goal-verify.md` — §04 + §06 v2.14 (goal model, goal-verify, budget, INTRO-1.3 gate).
- [x] `documents/plans/full-automation/SEC-15-v2.15-release-v2-15-pursuit-loop-goal-autopilot-self-gate.md` — §04 + §06 v2.15 (goal_autopilot, self_gate_mode, strict_hitl, hooks, stop taxonomy).
- [x] `documents/plans/full-automation/SEC-15-v2.16-release-v2-16-platform-queue-scheduler.md` — §04 + §06 v2.16 (queue item schema, scheduler, release-queue, SEC-13 interleave).
- [x] `documents/plans/full-automation/SEC-15-v2.17-release-v2-17-catalog-compose-first-list-components.md` — §04 + §06 v2.17 (list-components, CATALOG.md, compose-first mandatory).
- [x] `documents/plans/full-automation/SEC-15-v2.18-release-v2-18-staleness-graph-platform-nodes.md` — §04 + §06 v2.18 (staleness for scripts/skills/packs; reconcile-stale).
- [x] `documents/plans/full-automation/SEC-15-v2.19-release-v2-19-company-pack-schema-active-role.md` — §04 + §06 v2.19 (company/role/pipeline schemas, active_role, APP-A slices).
- [x] `documents/plans/full-automation/SEC-15-v2.20-release-v2-20-game-studio-pack-reference.md` — §04 + §06 v2.20 (game studio pack, F3, H1/H3-only demo).
- [x] `documents/plans/full-automation/SEC-15-v2.21-release-v2-21-data-platform-pack-reference.md` — §04 + §06 v2.21 (data platform pack, F4, feeds v2.22 _shared).
- [x] `documents/plans/full-automation/SEC-15-v2.22-release-v2-22-cross-pack--shared-library.md` — §04 + §06 v2.22 (template-packs/_shared micro-packs, F5).
- [x] `documents/plans/full-automation/SEC-15-v2.23-release-v2-23-operator-polish-h2-audit-dashboard.md` — §04 + §06 v2.23 (H2 digests, audit trail, dashboard goal+queue depth).
- [x] `documents/plans/full-automation/SEC-15-v2.24-release-v2-24-transistor-schema-registry-list-transistors.md` — §04 + §06 v2.24 (transistor schema, bootstrap set, list-transistors, §Q gate).
- [x] `documents/plans/full-automation/SEC-15-v2.25-release-v2-25-workflow-dag-validate-workflow-dag.md` — §04 + §06 v2.25 (workflow-dag schema, validate-workflow-dag, C6.1).
- [x] `documents/plans/full-automation/SEC-15-v2.26-release-v2-26-workflow-composer-active-workflow-execution.md` — §04 + §06 v2.26 (composer skill, active_workflow, one-node-per-turn).
- [x] `documents/plans/full-automation/SEC-15-v2.27-release-v2-27-pack-workflow-templates-cross-domain.md` — §04 + §06 v2.27 (pack workflows/transistors, C6.4 parallel branches).
- [x] `documents/plans/full-automation/SEC-15-v2.28-release-v2-28-transistor-maturity-dashboard-metrics.md` — §04 + §06 v2.28 (class_mix, platform.metrics, promotion-debt SLA, workflow coverage %, DAG viewer); enriched this batch.

## 06 SEC-17 decisions (11)

- [x] `documents/plans/full-automation/SEC-17-1-decision-self-gate-rigor-checklist-vs-reviewer.md` — §00 open #1 (leaf default = checklist+evidence).
- [x] `documents/plans/full-automation/SEC-17-10-decision-global--shared-transistors-plus-pack-overlay.md` — §00 resolved (two-tier _shared + pack overlay, semver fork).
- [x] `documents/plans/full-automation/SEC-17-2-decision-h3-scope-task-milestone-release-company.md` — §00 open #2 (`h3_scope` in company.yaml; §03 §4).
- [x] `documents/plans/full-automation/SEC-17-3-decision-platform-k-ratio-fixed-vs-adaptive.md` — §00 open #3 + §06 v2.16 queue-depth logging.
- [x] `documents/plans/full-automation/SEC-17-4-decision-budget-caps-unlimited-vs-checkpoint.md` — §00 open #4 (`goal.deadline` + A4.3 resource stop).
- [x] `documents/plans/full-automation/SEC-17-5-decision-pack-authority-legal-finance-h2-always.md` — §00 open #5 (`role_class`+`automation_allowed`; §03 §4, §06 v2.19).
- [x] `documents/plans/full-automation/SEC-17-6-decision-multi-goal-single-stack-vs-company-autopilot.md` — §00 open #6 + §06 v2.19 preemption ADR.
- [x] `documents/plans/full-automation/SEC-17-7-decision-transistor-granularity-one-verify-boundary.md` — §00 resolved (one verify boundary).
- [x] `documents/plans/full-automation/SEC-17-8-decision-composer-s3-skill-not-conductor-inline.md` — §00 resolved (S3 composer, conductor approves).
- [x] `documents/plans/full-automation/SEC-17-9-decision-json-dag-authoritative-visual-editor-optional.md` — §00 resolved (JSON authoritative; viewer v2.28+).
- [x] `documents/plans/full-automation/SEC-17-index.md` — index only; all 10 decisions covered above.

## 07 SEC-18 transistor reference (2)

- [x] `documents/plans/full-automation/SEC-18-index.md` — index only; main ref covered below.
- [x] `documents/plans/full-automation/SEC-18-transistor-model-a-to-z-reference.md` — §03 §3 (manifest+DAG schemas, L6, bootstrap set, ranking) + §00 resolved §C-5/6/7/9; §06 v2.24–v2.28 + §Q acceptance.

## 99 Other full-automation (1)

- [x] `documents/plans/full-automation/INDEX.md` — authoritative index (281 spec leaves + H3-SIGNOFF); tracked by §07 + §08; release headers reconciled 2026-06-28.

## Branch A (33)

- [x] `documents/plans/full-automation/A1-index.md` — index only; A1.1–A1.5 covered §03 §1 + §06 v2.14.
- [x] `documents/plans/full-automation/A1.1-goal-id-parent-goal-goal-type.md` — §03 goal{id,parent_goal,type incl program} + §06 type routing + duplicate-id/parent validation.
- [x] `documents/plans/full-automation/A1.2-success-criteria-machine-checkable.md` — §06 v2.14 preflight rejects subjective criteria; goal-keeper binds criteria→task cards.
- [x] `documents/plans/full-automation/A1.3-goal-verify-command-meta-test.md` — §03 goal.verify{} + §06 goal-verify.py + tests.
- [x] `documents/plans/full-automation/A1.4-deadline-budget-steps-tokens-wall-clock.md` — §03 goal.deadline + §06 budget accounting; max_tokens→resource.max_cost alias; Plane D cross-ref.
- [x] `documents/plans/full-automation/A1.5-goal-state-enum-pursuing-blocked-verifying-achieved-rejected.md` — §03 goal.state enum + §06 A2.5 verifying→H3 transition.
- [x] `documents/plans/full-automation/A2-index.md` — index only; A2.1–A2.7 covered §05 Plane A + §06 v2.14–v2.15.
- [x] `documents/plans/full-automation/A2.1-preflight-check-pipeline-blocked-extended.md` — §06 check-pipeline-blocked exit 0=READY/1=BLOCKED; missing goal→H2. (Release: v2.15 per master plan.)
- [x] `documents/plans/full-automation/A2.2-if-ready-execute-one-pipeline-step.md` — §05 A2 one-step exec + §06 goal_autopilot_loop test.
- [x] `documents/plans/full-automation/A2.3-post-step-route-tier-dual-write-increment.md` — §06 route-tier --apply + budget increment post-step.
- [x] `documents/plans/full-automation/A2.4-goal-scope-complete-run-goal-verify.md` — §03 scope-complete predicate + §06 test_goal_scope_complete.
- [x] `documents/plans/full-automation/A2.5-goal-verify-pass-transition-h3-pending.md` — §06 verifying→hitl.pending=H3; A6.1 notify deferred v2.23.
- [x] `documents/plans/full-automation/A2.6-loop-until-blocked-budget-achieved-h3-reject.md` — §05 canonical A2.1→2.2→2.3 loop; §06 integration test.
- [x] `documents/plans/full-automation/A2.7-no-intermediate-wait-for-continue.md` — §06 pipeline-continue + approval-gates (no mid-loop continue prompts).
- [x] `documents/plans/full-automation/A3-index.md` — index only; A3.1–A3.4 covered §03 pursuit.mode + §06 v2.15.
- [x] `documents/plans/full-automation/A3.1-session-autopilot-max-steps-per-session.md` — §06 resource.session_cap via autopilot.steps_this_session + max_steps_per_session.
- [x] `documents/plans/full-automation/A3.2-goal-autopilot-until-goal-verify-or-hard-block.md` — §03 pursuit.mode=goal_autopilot + §06 autopilot skill + run-local-pipeline.
- [x] `documents/plans/full-automation/A3.3-company-autopilot-multi-goal-role-workstreams.md` — §03 pursuit.goal_queue[] + §06 v2.19 flag-gated + preemption ADR.
- [x] `documents/plans/full-automation/A3.4-sdk-daemon-run-local-pipeline-24-7.md` — §06 run-local-pipeline goal_autopilot + SDK auth-fail typed stop.
- [x] `documents/plans/full-automation/A4-index.md` — index only; A4.1–A4.5 covered §03 stop taxonomy comment + §06 v2.15.
- [x] `documents/plans/full-automation/A4.1-stop-human-h1-h2-h3.md` — §03/§06 human.H1|H2|H3 (dot notation canonical).
- [x] `documents/plans/full-automation/A4.2-stop-verify-evidence-goal-verify-regression.md` — §06 verify.evidence_fail|goal_verify_fail|regression.
- [x] `documents/plans/full-automation/A4.3-stop-resource-max-steps-max-cost-lease-expired.md` — §06 resource.* incl max_cost alias + session_cap + lease_expired.
- [x] `documents/plans/full-automation/A4.4-stop-integrity-validate-workflow-state-corrupt.md` — §06 v2.14 integrity.* + G6.3 snapshot restore cross-ref.
- [x] `documents/plans/full-automation/A4.5-stop-completion-goal-achieved-program-done.md` — §06 completion.goal_achieved|program_done + INTRO-1.3 five-part gate.
- [x] `documents/plans/full-automation/A5-index.md` — index only; A5.1–A5.3 covered §05 Plane A + §06 v2.15.
- [x] `documents/plans/full-automation/A5.1-continue-resume-pursuit-if-not-blocked.md` — §06 pipeline-continue: continue=resume if READY.
- [x] `documents/plans/full-automation/A5.2-continue-not-approval-self-gate-h1-h3-only.md` — §06 self_gate_mode + strict_hitl; continue≠approval.
- [x] `documents/plans/full-automation/A5.3-default-after-h1-auto-enter-goal-autopilot.md` — §06 goal-keeper sets autopilot.active + goal_autopilot post-H1.
- [x] `documents/plans/full-automation/A6-index.md` — index only; A6.1–A6.3 covered §05 Plane A (v2.23) + §06 v2.23.
- [x] `documents/plans/full-automation/A6.1-notify-dashboard-status-webhook-phase-complete.md` — §06 v2.23 dashboard/STATUS/webhook milestones (non-blocking).
- [x] `documents/plans/full-automation/A6.2-notify-digest-on-h2-blocker-not-every-step.md` — §06 v2.23 H2 digest (goal_id+stop_reason+action, not per-step).
- [x] `documents/plans/full-automation/A6.3-operator-observe-without-unblocking-loop.md` — §06 v2.23 observe-without-unblock (read-only does not clear H2).

## Branch B (33)

- [x] `documents/plans/full-automation/B1-index.md` — index only; B1.1–B1.5 covered §05 Plane B + §06 v2.15 S0–S4 rows.
- [x] `documents/plans/full-automation/B1.1-s0-deterministic-mandatory-first.md` — §06 v2.15 B1.1 mandatory-first preflight order; §05 B1 S0.
- [x] `documents/plans/full-automation/B1.2-s1-mechanical-economy-workers-catalog.md` — §06 v2.15 B1.2 S1 economy workers + model_escalation; §05 B1.
- [x] `documents/plans/full-automation/B1.3-s2-templated-artifacts.md` — §06 v2.15 B1.3 S2 skills (hld/dd/task-breakdown/diagram); §05 B1.
- [x] `documents/plans/full-automation/B1.4-s3-architecture-ambiguity.md` — §06 v2.15 B1.4 S3 genius-only ambiguity rules; §05 B1.
- [x] `documents/plans/full-automation/B1.5-s4-governance-escalation-h2-packaging.md` — §06 v2.15 B1.5 S4 H2 packaging + §03 hitl.payload; §05 B1.
- [x] `documents/plans/full-automation/B2-index.md` — index only; B2.1–B2.6 covered §05 Plane B + §06.
- [x] `documents/plans/full-automation/B2.1-conductor-genius-merge-route-platform-drain.md` — §05 B2 conductor + §06 v2.16 dual-stack peek/drain (B4.2/D3).
- [x] `documents/plans/full-automation/B2.2-librarian-allowed-reads-catalog-composition.md` — §06 v2.17 suggested_components + suggested_worker_role; max 5 allowed_reads.
- [x] `documents/plans/full-automation/B2.3-phase-workers-implement-design-explore.md` — §05 B2 phase workers; C4 program parallel lanes.
- [x] `documents/plans/full-automation/B2.4-verifier-tool-operator-evidence.md` — §06 G1 evidence gates + I4 tool-operator; B3.3 escalation on fail.
- [x] `documents/plans/full-automation/B2.5-reviewer-bugbot-security-risk-triggers.md` — §06 v2.23 G4 review triggers (Bugbot, security-review, risk).
- [x] `documents/plans/full-automation/B2.6-platform-worker-promotion-queue-parallel-slot.md` — §05 B2.6 + §06 v2.16 platform worker role.
- [x] `documents/plans/full-automation/B3-index.md` — index only; B3.1–B3.4 covered §05 Plane B + §06.
- [x] `documents/plans/full-automation/B3.1-genius-orchestration-only-thin-turns.md` — §06 v2.15 B3.1 genius thin turns; no inline implement when spawn_workers.
- [x] `documents/plans/full-automation/B3.2-economy-bulk-code-search-shell.md` — §06 v2.15 B3.2 economy bulk search/refactor scope.
- [x] `documents/plans/full-automation/B3.3-escalation-loop-on-verify-fail.md` — §06 v2.15 B3.3 verify-fail loop + v2.23 G4.3 repeated-fail→S4.
- [x] `documents/plans/full-automation/B3.4-platform-turns-economy-plus-s0-scripts.md` — §06 v2.16 B3.4 platform turns economy+S0; SEC-13 interleave.
- [x] `documents/plans/full-automation/B4-index.md` — index only; B4.1–B4.4 covered §05 Plane B + §06 v2.16–v2.17.
- [x] `documents/plans/full-automation/B4.1-product-next-action-task-each-turn.md` — §05 B4 + §06 A2 one-step + v2.16 product turn invariant.
- [x] `documents/plans/full-automation/B4.2-platform-promotion-queue-peek-drain.md` — §03 drain_policy + §06 v2.16 D3 scheduler K peek/drain.
- [x] `documents/plans/full-automation/B4.3-compose-first-catalog-before-improvise.md` — §06 v2.17 compose-first rule + E2 ranking (hard_transistor>script>…).
- [x] `documents/plans/full-automation/B4.4-divergence-log-when-not-composing.md` — §03 divergence_log entry schema + §06 v2.16 silent-invention fail.
- [x] `documents/plans/full-automation/B5-index.md` — index only; B5.1–B5.4 covered §06 v2.19.
- [x] `documents/plans/full-automation/B5.1-active-role-from-template-pack.md` — §03 company.active_role + §06 v2.19 pack instantiation.
- [x] `documents/plans/full-automation/B5.2-role-to-pipeline-id-skills-tool-permissions.md` — §03 roles/*.yaml fields + §06 v2.19 role mapping.
- [x] `documents/plans/full-automation/B5.3-handoff-manifest-artifact-graph.md` — §06 v2.19 manifest+artifact-graph handoffs; orchestrate-program.
- [x] `documents/plans/full-automation/B5.4-conductor-stays-workers-swap-role-context.md` — §06 v2.19 conductor fixed identity; workers swap allowed_reads per spawn.
- [x] `documents/plans/full-automation/B6-index.md` — index only; B6.1–B6.4 covered §05 Plane B + §06 v2.26.
- [x] `documents/plans/full-automation/B6.1-workflow-composer-skill-s3-graph-planning.md` — §06 v2.26 B6.1 S3 workflow-composer; SEC-17-8.
- [x] `documents/plans/full-automation/B6.2-conductor-approves-generator-workflow-at-h1.md` — §06 v2.26 B6.2 H1 DAG approval binding.
- [x] `documents/plans/full-automation/B6.3-one-workflow-node-per-product-turn-default.md` — §06 v2.26 B6.3 one node/turn; G5.8 binding.
- [x] `documents/plans/full-automation/B6.4-gate-transistor-pass-fail-edge-routing.md` — §06 v2.26 gate kinds (verify_result|file_exists|schema_match|budget_remaining|staleness_clear); soft gates forbidden.

## Branch C (31)

- [x] `documents/plans/full-automation/C1-index.md` — index only; C1.1–C1.4 covered §05 Plane C + §06 v2.19.
- [x] `documents/plans/full-automation/C1.1-pipeline-software-greenfield.md` — §05 C1 greenfield chain + §06 v2.15 pursuit/self-gate after H1.
- [x] `documents/plans/full-automation/C1.2-pipeline-iterative-feature.md` — §05 C1 iterative-feature + §06 C6.1 on iterative pipeline (SEC-18 §Q).
- [x] `documents/plans/full-automation/C1.3-pipeline-multi-domain-program.md` — §05 C1 program + §06 C4 orchestrate-program/manifest.
- [x] `documents/plans/full-automation/C1.4-pack-defined-pipelines-per-company-template.md` — §06 v2.19 C1.4 pipeline resolution + pipeline.schema.json fields.
- [x] `documents/plans/full-automation/C2-index.md` — index only; C2.1–C2.5 covered §05 Plane C + §06 v2.17.
- [x] `documents/plans/full-automation/C2.1-phase-spec-parser-requirements.md` — §05 C2 spec-parser phase; blocking questions halt downstream.
- [x] `documents/plans/full-automation/C2.2-phase-hld-dd-diagrams.md` — §05 C2 + §06 v2.15 self-gate HLD/DD; docs/design + docs/diagrams.
- [x] `documents/plans/full-automation/C2.3-phase-task-breakdown-scaffold-implement.md` — §05 C2 + §06 task-breakdown/scaffold; C6.1 inserts workflow-compose before implement (v2.25).
- [x] `documents/plans/full-automation/C2.4-phase-test-refactor-git-workflow.md` — §06 test-before-push + git-workflow when last_verify=passed.
- [x] `documents/plans/full-automation/C2.5-phase-inputs-outputs-verify-catalog-refs.md` — §06 v2.17 phase skill front-matter contract; phase verify ≠ goal_verify; B4.4 on missing refs.
- [x] `documents/plans/full-automation/C3-index.md` — index only; C3.1–C3.4 covered §05 Plane C + §06.
- [x] `documents/plans/full-automation/C3.1-task-cards-components-promotion-note.md` — §06 v2.16 Components+promotion_note; v2.26 adds workflow_node_id+transistor_id (C6.3).
- [x] `documents/plans/full-automation/C3.2-work-orders-parallel-lanes.md` — §06 C4 lanes/leases + v2.19 complete-work-order before role switch.
- [x] `documents/plans/full-automation/C3.3-evidence-per-task.md` — §06 G1 evidence gates + evidence-types.md; last_verify discipline.
- [x] `documents/plans/full-automation/C3.4-task-to-goal-rollup-percent-goal-verify.md` — §06 v2.14 task rollup; coexists with C6.5 workflow-node rollup at goal_verify.
- [x] `documents/plans/full-automation/C4-index.md` — index only; C4.1–C4.4 covered §05 Plane C + §06 v2.19.
- [x] `documents/plans/full-automation/C4.1-workstreams-lane-json-leases.md` — §06 v2.19 lane lease schema {holder,expires_at,work_order_path}; A4.3 lease_expired.
- [x] `documents/plans/full-automation/C4.2-orchestrate-program.md` — §05 C4 + existing orchestrate-program skill; manifest gate before parallel spawn.
- [x] `documents/plans/full-automation/C4.3-integration-manifest-cross-stream-contract.md` — §06 integration-manifest-keeper + human/self-gate before parallel implement.
- [x] `documents/plans/full-automation/C4.4-artifact-graph-per-program-and-pack.md` — §06 v2.18 reconcile-artifact-graph + pack graph templates.
- [x] `documents/plans/full-automation/C5-index.md` — index only; C5.1–C5.3 covered §05 Plane C + §06 v2.14.
- [x] `documents/plans/full-automation/C5.1-src-tests-e2e-delivery.md` — §06 pre-flight tests/integration + tests/e2e; standard layout paths.
- [x] `documents/plans/full-automation/C5.2-environment-setup-tasks-ordered-first.md` — §06 v2.14 C5.2 env-setup before package installs (AGENTS.md rule 17).
- [x] `documents/plans/full-automation/C5.3-definition-of-done-goal-slice-satisfied.md` — §06 C5.3 goal-slice DoD + INTRO-1.3 five-part gate; task-done ≠ goal-done.
- [x] `documents/plans/full-automation/C6-index.md` — index only; C6.1–C6.5 covered §05 Plane C + §06 v2.25–v2.27 + SEC-18.
- [x] `documents/plans/full-automation/C6.1-phase-workflow-compose-mandatory-before-implement.md` — §06 v2.25 C6.1 + check-pipeline-blocked; iterative+greenfield; goal-type exemptions.
- [x] `documents/plans/full-automation/C6.2-workflow-dag-artifact-schema-json.md` — §03 workflow-dag.v1.json + §06 v2.25 docs/workflows/<goal-id>.json.
- [x] `documents/plans/full-automation/C6.3-task-card-binds-workflow-node-id.md` — §06 v2.26 workflow_node_id+transistor_id binding; G5.8 fuzzy-chain guard.
- [x] `documents/plans/full-automation/C6.4-parallel-workflow-branches-via-work-orders.md` — §03 §3.4 active_workflow.branches[] + §06 v2.27 (antichains, join rules, goal_verify waits all branches).
- [x] `documents/plans/full-automation/C6.5-workflow-node-rollup-to-goal-verify.md` — §06 v2.26 terminal_nodes rollup + G2.5; coexists with C3.4 task rollup; G6.4 checkpoint replay.

## Branch D (42)

- [x] `documents/plans/full-automation/D1-index.md` — index only; D1.1–D1.7 covered §03 §2 ladder + §06 v2.16/v2.24.
- [x] `documents/plans/full-automation/D1.1-l0-ephemeral-one-off-reasoning.md` — §03 L0 + §06 enqueue when pattern repeats 2× (D2.1.1).
- [x] `documents/plans/full-automation/D1.2-l1-playbook-docs-playbooks.md` — §03 L1 docs/playbooks + §06 D4.1 playbook-keeper.
- [x] `documents/plans/full-automation/D1.3-l2-script-s0-scripts.md` — §03 L2 scripts/ + §06 D4.2 script extraction + D6.2 verify.
- [x] `documents/plans/full-automation/D1.4-l3-skill-command-cursor-skills.md` — §03 L3 skills/commands + §06 D4.3 wrapper.
- [x] `documents/plans/full-automation/D1.5-l4-ambient-hooks-ci-scheduled.md` — §03 L4 hooks/CI + §06 D4.4 platform work.
- [x] `documents/plans/full-automation/D1.6-l5-template-pack-fragment.md` — §03 L5 template-packs + §06 D4.6 pack export (v2.19).
- [x] `documents/plans/full-automation/D1.7-l6-transistor-registered-composable-block.md` — §03 L6 capstone + §06 v2.24 (subsumes L2–L5, L0 steady-state rule, semver fork).
- [x] `documents/plans/full-automation/D2-index.md` — index only; see D2.1-index for enqueue triggers.
- [x] `documents/plans/full-automation/D2-platform-queue-index.md` — aggregate spec; master §03/§06 authoritative (leaf stale: L1–L5, effort_class S1, omits D2.1.5).
- [x] `documents/plans/full-automation/D2.1-index.md` — index only; D2.1.1–D2.1.5 enqueue triggers covered §06 v2.16/v2.24.
- [x] `documents/plans/full-automation/D2.1.1-enqueue-repeated-manual-command-2x.md` — §06 v2.16 enqueue trigger; often target L2 script.
- [x] `documents/plans/full-automation/D2.1.2-enqueue-worker-flags-repetition.md` — §06 fingerprint dedupe; defer false positive until 2nd flag.
- [x] `documents/plans/full-automation/D2.1.3-enqueue-verify-pattern-n-task-cards.md` — §06 N in drain_policy.verify_pattern_task_threshold; sample task ids recorded.
- [x] `documents/plans/full-automation/D2.1.4-enqueue-conductor-post-mortem-escalation.md` — §06 post-mortem after S3/S4 escalation; D3.3 may raise priority.
- [x] `documents/plans/full-automation/D2.1.5-enqueue-compose-miss-missing-transistor.md` — §06 v2.24 capability_id/suggested_io_schema; L0 waiver until L6 minted.
- [x] `documents/plans/full-automation/D2.2-platform-queue-item-schema.md` — §03 promotion_queue item schema (L1–L6) + §06 v2.16 S0-validatable.
- [x] `documents/plans/full-automation/D2.3-dequeue-platform-turn-not-product.md` — §06 platform turn only; partial→re-enqueue; B2.6 parallel slots.
- [x] `documents/plans/full-automation/D3-index.md` — index only; D3.1–D3.5 covered §06 v2.16 scheduler.
- [x] `documents/plans/full-automation/D3.1-1-platform-turn-per-k-product-turns.md` — §03 drain_policy K + §06 steps_total % K == 0; skip when empty.
- [x] `documents/plans/full-automation/D3.2-priority-boost-queue-depth-threshold.md` — §03 boost_queue_depth + §06 D3.2 extra drains on depth.
- [x] `documents/plans/full-automation/D3.3-priority-cut-product-blocked-missing-tool.md` — §06 cut jumps platform ahead; product stays blocked; boost suspended.
- [x] `documents/plans/full-automation/D3.4-idle-drain-product-waits-h2.md` — §06 idle-drain during external H2 wait.
- [x] `documents/plans/full-automation/D3.5-max-platform-backlog-age-force-drain.md` — §06 force-drain on max age; age resets on partial promotion.
- [x] `documents/plans/full-automation/D4-index.md` — index only; D4.1–D4.7 covered §05 Plane D + §06.
- [x] `documents/plans/full-automation/D4.1-platform-work-playbook-keeper.md` — §06 D4.1 primary L1 platform work + B2.6 worker.
- [x] `documents/plans/full-automation/D4.2-platform-work-script-extraction.md` — §06 D4.2 L1→L2 script + idempotent CLI + tests.
- [x] `documents/plans/full-automation/D4.3-platform-work-skill-command-wrapper.md` — §06 D4.3 L2→L3 skill/command wrapper.
- [x] `documents/plans/full-automation/D4.4-platform-work-hook-validate-workflow.md` — §06 D4.4 L4 hook/CI validate-workflow extension.
- [x] `documents/plans/full-automation/D4.5-platform-work-catalog-regeneration.md` — §06 D4.5 + v2.17 E1.7 CATALOG regen.
- [x] `documents/plans/full-automation/D4.6-platform-work-pack-fragment-export.md` — §06 D4.6 L5 upward export to template-packs (v2.19).
- [x] `documents/plans/full-automation/D4.7-platform-work-transistor-extraction.md` — §06 v2.24 D4.7 hard-before-soft + list-transistors dedupe.
- [x] `documents/plans/full-automation/D5-index.md` — index only; D5.1–D5.3 covered §06 v2.16.
- [x] `documents/plans/full-automation/D5.1-configure-task-level-params-only.md` — §06 configure=params only, no staleness bump (K, N, thresholds).
- [x] `documents/plans/full-automation/D5.2-extend-backwards-compatible-staleness-bump.md` — §06 extend=back-compat + staleness bump + parent id proof.
- [x] `documents/plans/full-automation/D5.3-fork-new-catalog-entry-provenance.md` — §06 fork=new id + provenance; silent alias forbidden; task-card migration.
- [x] `documents/plans/full-automation/D6-index.md` — index only; D6.1–D6.5 covered §06 v2.16/v2.24.
- [x] `documents/plans/full-automation/D6.1-platform-done-catalog-index-row.md` — §06 D6.1 INDEX row mandatory (maturity + verify ref + promotion id).
- [x] `documents/plans/full-automation/D6.2-platform-done-verify-script-l2.md` — §06 D6.2 L1 manual verify OK until scripted; L2+ automated.
- [x] `documents/plans/full-automation/D6.3-platform-done-task-card-references.md` — §06 D6.3 ≥1 task card references promoted artifact.
- [x] `documents/plans/full-automation/D6.4-platform-done-staleness-node-wired.md` — §06 D6.4 staleness node + dependency edges (v2.18).
- [x] `documents/plans/full-automation/D6.5-platform-done-transistor-registry-and-graph.md` — §06 v2.24 D6.5 TRANSISTORS.md + workflow ref + unit test + E5.4.

## Branch E (39)

- [x] `documents/plans/full-automation/E1-index.md` — index only; E1.1–E1.7 covered §03 §5 + §06 v2.17.
- [x] `documents/plans/full-automation/E1.1-catalog-scripts-manifest-generated.md` — §06 v2.17 E1.1 scripts manifest via list-components.py.
- [x] `documents/plans/full-automation/E1.2-catalog-playbooks-index.md` — §06 v2.17 E1.2 playbooks INDEX scan.
- [x] `documents/plans/full-automation/E1.3-catalog-skills-index.md` — §03 §5 skills index w/ phase bindings + tool permissions metadata.
- [x] `documents/plans/full-automation/E1.4-catalog-facts-index.md` — §06 v2.17 E1.4 facts INDEX + §03 §5.2 E3.1.
- [x] `documents/plans/full-automation/E1.5-catalog-pipelines-manifest.md` — §06 v2.17 E1.5 pipelines manifest; C1.4 pack resolution cross-ref.
- [x] `documents/plans/full-automation/E1.6-catalog-template-packs-readme.md` — §06 v2.17 E1.6 packs README scan.
- [x] `documents/plans/full-automation/E1.7-catalog-platform-catalog-md-umbrella.md` — §03 §5 bidirectional INDEX cross-links + Plane D maturity tie-in.
- [x] `documents/plans/full-automation/E2-index.md` — index only; E2.1–E2.5 covered §03 §5 + §06 v2.17.
- [x] `documents/plans/full-automation/E2.1-compose-resolve-capability-needed.md` — §03 §5 resolve capability step; mandatory before S1+.
- [x] `documents/plans/full-automation/E2.2-compose-query-catalog-list-components.md` — §03 §5 component type + maturity tier query output; librarian suggested_components.
- [x] `documents/plans/full-automation/E2.3-compose-rank-script-playbook-skill-facts.md` — §03 rank ladder + tie-break pack-authored/maturity; H2 on rank failure.
- [x] `documents/plans/full-automation/E2.4-compose-plan-task-card-components.md` — §03 §5 compose into task-card Components section.
- [x] `documents/plans/full-automation/E2.5-compose-miss-l0-enqueue-promotion.md` — §03 §5 L0 + enqueue; repeated L0 elevates promotion priority.
- [x] `documents/plans/full-automation/E3-index.md` — index only; E3.1–E3.3 covered §03 §5.2 + §06 v2.17.
- [x] `documents/plans/full-automation/E3.1-facts-docs-facts-external-truth.md` — §03 §5.2 external truth; stale facts → journal + reconcile.
- [x] `documents/plans/full-automation/E3.2-decisions-docs-decisions-adr.md` — §06 E3.2 ADR template; supersede → downstream staleness; B1.4 S3 path.
- [x] `documents/plans/full-automation/E3.3-remember-skill-index-no-fts-global.md` — §03 §5.2 no global FTS; repeated captures → promotion candidates.
- [x] `documents/plans/full-automation/E4-index.md` — index only; E4.1–E4.3 covered §03 §5.1 + §06 v2.17.
- [x] `documents/plans/full-automation/E4.1-context-always-on-rules-agents-md.md` — §03 §5.1 layer-0 AGENTS + pack rule fragments; AGENTS change → staleness.
- [x] `documents/plans/full-automation/E4.2-context-hooks-inject-continue-start.md` — §06 E4.2 hooks inject journal + Context files; corrupt state → H2.
- [x] `documents/plans/full-automation/E4.3-context-allowed-reads-cap-max-5.md` — §06 E4.3 cap 5 retained; G5.2 scope-bleed class.
- [x] `documents/plans/full-automation/E5-index.md` — index only; E5.1–E5.4 covered §03 §5.3 + §06 v2.18/v2.25.
- [x] `documents/plans/full-automation/E5.1-staleness-design-graph-staleness-json.md` — §03 §5.3 base graph; vision § → deepen enqueue.
- [x] `documents/plans/full-automation/E5.2-staleness-extend-playbooks-scripts-pack-nodes.md` — §06 v2.18 extended nodes incl. skills/commands/AGENTS; catalog regen reconciles graph.
- [x] `documents/plans/full-automation/E5.3-staleness-reconcile-stale-artifact-graph-skills.md` — §06 reconcile rerun/waive/deepen paths; silent implement on stale forbidden.
- [x] `documents/plans/full-automation/E5.4-staleness-workflow-graph-transistor-nodes.md` — §06 v2.25 E5.4 validation_hash + re-validate before next node.
- [x] `documents/plans/full-automation/E6-index.md` — index only; E6.1–E6.5 covered §03 §3 + §06 v2.24.
- [x] `documents/plans/full-automation/E6.1-catalog-transistors-manifest-registry.md` — §06 v2.24 E6.1 TRANSISTORS.md + bootstrap set + validate on commit.
- [x] `documents/plans/full-automation/E6.2-transistor-schema-id-version-typed-io.md` — §03 transistor.v1.json (id/version/capability_id/inputs/outputs/preconditions/executor/verify) + §06 v2.24.
- [x] `documents/plans/full-automation/E6.3-transistor-classes-hard-soft-gate.md` — §03 transistor classes (hard/soft/gate executors, maturity mix ~70/20/10) + §06 v2.24.
- [x] `documents/plans/full-automation/E6.4-list-transistors-query-io-compatibility.md` — §06 v2.24 E6.4 list + I/O query + --check-duplicates (G5.6).
- [x] `documents/plans/full-automation/E6.5-compose-rank-hard-transistor-script-soft.md` — §06 v2.24 E6.5 rank prepends hard_transistor; gate = edges not capability substitutes.
- [x] `documents/plans/full-automation/E7-index.md` — index only; E7.1–E7.5 covered §06 v2.25/v2.27.
- [x] `documents/plans/full-automation/E7.1-resolve-deliverable-type-workflow-template.md` — §06 v2.25 E7.1 deliverable type → workflow template.
- [x] `documents/plans/full-automation/E7.2-stitch-transistors-into-generator-dag.md` — §03 §3.3 stitch transistors into DAG; workflow-composer S3.
- [x] `documents/plans/full-automation/E7.3-validate-wiring-preconditions-postconditions-s0.md` — §03 §3.3 acyclicity + gate completeness + re-validate on edit.
- [x] `documents/plans/full-automation/E7.4-workflow-miss-enqueue-transistor-promotion.md` — §06 v2.24/v2.25 E7.4 l0_waiver + second-workflow same miss → H2.
- [x] `documents/plans/full-automation/E7.5-pack-generator-workflow-templates-inherit.md` — §06 v2.27 E7.5 pack workflows/transistors inherit + CI pre-publish validation.

## Branch F (33)

- [x] `documents/plans/full-automation/F1-index.md` — index only; F1.1–F1.9 covered §03 §4 + §06 v2.19/v2.27.
- [x] `documents/plans/full-automation/F1.1-pack-company-yaml-schema.md` — §03 §4 company.yaml fields incl. imports/h3_scope/default_workflow_template.
- [x] `documents/plans/full-automation/F1.2-pack-roles---yaml.md` — §03 §4 role schema: role_class, automation_allowed, forbidden_reads, pipeline_slice, output_type evidence.
- [x] `documents/plans/full-automation/F1.3-pack-pipelines---yaml.md` — §03 §4 pipelines: phases, gates, skill_bindings, verify_suites; C1.4 resolution.
- [x] `documents/plans/full-automation/F1.4-pack-manifest-md-integration-contracts.md` — §03 §4 manifest.md integration contracts; F2.4 handoff prereqs.
- [x] `documents/plans/full-automation/F1.5-pack-artifact-graph-json-cross-role.md` — §03 §4 artifact-graph.json cross-role dependencies; C4 lanes.
- [x] `documents/plans/full-automation/F1.6-pack-playbooks-role-specific.md` — §03 §4 playbooks/ role-specific; F6.2 scoped reads.
- [x] `documents/plans/full-automation/F1.7-pack-template-tasks-seed-cards.md` — §06 v2.19 seed cards + v2.26 workflow_node_id/transistor_id bindings.
- [x] `documents/plans/full-automation/F1.8-pack-verify-goal-verify-suites.md` — §03 §4 verify/; C6.5 dual rollup at goal_verify.
- [x] `documents/plans/full-automation/F1.9-pack-transistors-and-generator-workflows.md` — §03 §4 workflows/transistors overlays; §06 v2.27 F1.9 + pack CI validation.
- [x] `documents/plans/full-automation/F2-index.md` — index only; F2.1–F2.4 covered §03 §4 + §06 v2.19.
- [x] `documents/plans/full-automation/F2.1-company-instantiate-program-scoper-pack-select.md` — §06 v2.19 program-scoper pack select + optional H1 gate (F2.1).
- [x] `documents/plans/full-automation/F2.2-company-spawn-workstream-department-role-lane.md` — §06 v2.19 workstream=dept/role lane; C4.1 lease schema.
- [x] `documents/plans/full-automation/F2.3-company-active-role-rotates-ready-work.md` — §03 §4 ready-work rotation (not round-robin); complete-work-order before switch.
- [x] `documents/plans/full-automation/F2.4-company-conductor-handoffs-manifest-graph.md` — §03 §4 S0 manifest+graph prereqs vs S3 ambiguous merge.
- [x] `documents/plans/full-automation/F3-index.md` — index only; F3.1–F3.4 covered §06 v2.20.
- [x] `documents/plans/full-automation/F3.1-game-studio-roles-designer-ta-animator-programmer-qa-build-r.md` — §06 v2.20 roles; optional/deferred lanes until milestone.
- [x] `documents/plans/full-automation/F3.2-game-studio-pipelines-concept-to-build.md` — §06 v2.20 concept→build pipeline; parallel asset lanes.
- [x] `documents/plans/full-automation/F3.3-game-studio-external-tools-blender-ue-git-ci.md` — §06 v2.20 Blender/UE/Perforce/Git/CI via tool-operator.
- [x] `documents/plans/full-automation/F3.4-game-studio-goal-verify-asset-engine-tests-perf.md` — §06 v2.20 goal_verify suite; weak initial OK + adversarial tightening ADR.
- [x] `documents/plans/full-automation/F4-index.md` — index only; F4.1–F4.2 covered §06 v2.21.
- [x] `documents/plans/full-automation/F4.1-data-platform-roles-analyst-engineer-dba-sre-governance.md` — §06 v2.21 roles; governance strict_hitl (SEC-17-5).
- [x] `documents/plans/full-automation/F4.2-data-platform-pipelines-ingest-model-deploy-monitor.md` — §06 v2.21 pipelines; deploy.maintenance_windows policy.
- [x] `documents/plans/full-automation/F5-index.md` — index only; F5.1–F5.4 covered §06 v2.22/v2.27.
- [x] `documents/plans/full-automation/F5.1-cross-pack-imports-micro-packs.md` — §03 §4 imports[]; §06 v2.22 pack import mechanism.
- [x] `documents/plans/full-automation/F5.2-template-packs--shared-library.md` — §06 v2.22 _shared micro-packs; blast-radius extend/fork or H2.
- [x] `documents/plans/full-automation/F5.3-no-repo-outside-template-packs-ceiling.md` — §03 §4 ceiling; hotfix via version/import/journal override only.
- [x] `documents/plans/full-automation/F5.4-shared-transistors-library-template-packs--shared.md` — §06 v2.27 _shared/transistors bootstrap + standard-cell workflows.
- [x] `documents/plans/full-automation/F6-index.md` — index only; F6.1–F6.4 covered §06 v2.19.
- [x] `documents/plans/full-automation/F6.1-role-mapping-conductor-context-switch-active-role.md` — §03 company.active_role persists across turns; mis-mapping = conformance fail.
- [x] `documents/plans/full-automation/F6.2-role-allowed-reads-scoped-playbooks-lane-tasks.md` — §06 v2.19 allowed_reads + forbidden_reads scoped to role/lane.
- [x] `documents/plans/full-automation/F6.3-role-tool-permissions-mcp-cli-allowlist.md` — §06 v2.19 mcp_allowlist + cli_patterns + write_scopes per role.
- [x] `documents/plans/full-automation/F6.4-role-evidence-requirements-per-output-type.md` — §06 v2.19 output_type evidence fail-closed even if generic verify passed.

## Branch G (33)

- [x] `documents/plans/full-automation/G1-index.md` — index only; G1.1–G1.3 covered §03 §6 + §06 v2.14/v2.15.
- [x] `documents/plans/full-automation/G1.1-task-verify-router-verifier.md` — §03 §6 task evidence verify-router.py + verifier skill; §06 G5.1.
- [x] `documents/plans/full-automation/G1.2-evidence-required-state.md` — §03 §6 evidence_required gate; §06 v2.14 + G5.1 fail-closed.
- [x] `documents/plans/full-automation/G1.3-last-verify-before-advance.md` — §03 §6 last_verify latch before advance; cross-ref G6.3 snapshot fields.
- [x] `documents/plans/full-automation/G2-index.md` — index only; G2.1–G2.5 covered §03 §6 + §06 v2.14/v2.26.
- [x] `documents/plans/full-automation/G2.1-goal-verify-command-state-pack.md` — §03 goal.verify{} + §06 v2.14 goal-verify.py; pack verify/ suites.
- [x] `documents/plans/full-automation/G2.2-goal-verify-aggregates-unit-integration-e2e-tool.md` — §03 §6 aggregates unit+integration+e2e+tool; §06 v2.14 G2.2.
- [x] `documents/plans/full-automation/G2.3-goal-verify-blocks-h3-until-pass.md` — §06 v2.14 A2.5 verifying→hitl.pending=H3 only after goal_verify pass.
- [x] `documents/plans/full-automation/G2.4-goal-verify-regression-every-implement-batch.md` — §03 §6 regression every implement batch; §06 v2.14 G2.4.
- [x] `documents/plans/full-automation/G2.5-per-node-evidence-rollup-goal-verify.md` — §06 v2.26 G2.5/C6.5 dual rollup: task + completed_nodes[] evidence.
- [x] `documents/plans/full-automation/G3-index.md` — index only; G3.1–G3.3 covered §03 §6 + §06 v2.14/v2.15.
- [x] `documents/plans/full-automation/G3.1-conformance-validate-workflow-ci.md` — §03 §6 validate-workflow.py; §06 v2.14 G3.1 + v2.18 CI step.
- [x] `documents/plans/full-automation/G3.2-conformance-route-tier-check.md` — §03 §6 route-tier --check; §05 Plane G G3.
- [x] `documents/plans/full-automation/G3.3-conformance-check-pipeline-blocked-goal-autopilot.md` — §03 §6 scope-complete→verifying predicate; §06 v2.14 A2.1/A2.4.
- [x] `documents/plans/full-automation/G4-index.md` — index only; G4.1–G4.4 covered §06 v2.23.
- [x] `documents/plans/full-automation/G4.1-review-security-review-touch-paths-deps.md` — §03 §6 declared files + diff stats; waivable findings w/ expiry under self-gate.
- [x] `documents/plans/full-automation/G4.2-review-bugbot-large-diffs.md` — §06 v2.23 bugbot supplemental ≠ verify-router; repeat pattern → D2.1 promotion enqueue.
- [x] `documents/plans/full-automation/G4.3-review-escalation-s4-repeated-verify-fail.md` — §03 §6 S4 escalation; §06 v2.23 G4.3 + v2.15 B3.3.
- [x] `documents/plans/full-automation/G4.4-review-staleness-reconciliation-before-merge.md` — §06 v2.18 G4.4/G5.5 reconcile before merge.
- [x] `documents/plans/full-automation/G5-index.md` — index only; G5.1–G5.8 covered §03 §6 mistake map + §06 spread.
- [x] `documents/plans/full-automation/G5.1-mistake-hallucinated-done-evidence-gate.md` — §06 G5.1 evidence gate + hierarchy audit re-enqueue on artifactless close.
- [x] `documents/plans/full-automation/G5.2-mistake-scope-creep-allowed-reads-task-card.md` — §06 G5.2 allowed_reads/forbidden_reads + E4.3 scope-bleed class.
- [x] `documents/plans/full-automation/G5.3-mistake-wrong-architecture-self-gate-goal-verify.md` — §06 v2.15 self_gate_mode + G5.3 goal_verify architecture check.
- [x] `documents/plans/full-automation/G5.4-mistake-skipped-tests-verify-router-mandatory.md` — §03 §6 verify-router mandatory; headless-verify/CI same path.
- [x] `documents/plans/full-automation/G5.5-mistake-stale-design-staleness-reconcile.md` — §06 v2.18 G5.5 staleness graph + reconcile-stale before implement.
- [x] `documents/plans/full-automation/G5.6-mistake-duplicate-tooling-platform-queue-catalog.md` — §06 G5.6 platform queue + compose-first + list-transistors dedupe.
- [x] `documents/plans/full-automation/G5.7-mistake-unsafe-command-pretooluse-allowlist.md` — §06 v2.15 preToolUse deny fail-closed + journal note per role allowlist.
- [x] `documents/plans/full-automation/G5.8-mistake-fuzzy-chain-lost-in-prose-workflow-control.md` — §03 §6 fuzzy-chain guard + v2.28 fuzzy_chain_incidents metric; §06 v2.26 G5.8.
- [x] `documents/plans/full-automation/G6-index.md` — index only; G6.1–G6.4 covered §03 §6 + §06 v2.15/v2.26.
- [x] `documents/plans/full-automation/G6.1-rollback-git-branch-per-goal-slice.md` — §03 §6 git branch per goal slice; branch name in journal handoff.
- [x] `documents/plans/full-automation/G6.2-rollback-journal-last-failure-structured-h2.md` — §06 v2.15 G6.2 structured last_failure; v2.23 A6.2 H2 digest.
- [x] `documents/plans/full-automation/G6.3-rollback-autopilot-resume-precompact-snapshot.md` — §06 v2.15 preCompact snapshot (next_action/evidence/last_verify/gates/autopilot) + v2.26 active_workflow extension; resume never from chat memory.
- [x] `documents/plans/full-automation/G6.4-workflow-checkpoint-replay-from-failed-node.md` — §06 v2.26 G6.4 replay from failed_node_id; graph change → full restart.

## Branch H (15)

- [x] `documents/plans/full-automation/H-index.md` — index only; H1–H6 covered §03 §1 persistence artifacts + §05 Plane H.
- [x] `documents/plans/full-automation/H1-index.md` — index only; H1.1–H1.7 covered §03 §1 field ownership + release map.
- [x] `documents/plans/full-automation/H1.1-state-existing-next-action-program-autopilot-evidence-tier.md` — §03 §1 legacy top-level router (next_action, program, autopilot, evidence_required, model_tier, spawn_workers, capability_class, gates_pending); S0-first.
- [x] `documents/plans/full-automation/H1.2-state-goal-block.md` — §03 §1 v2.14 goal block (id, type, success_criteria, verify_command, deadline, state, verify{}); §06 v2.14 A1.*.
- [x] `documents/plans/full-automation/H1.3-state-platform-block.md` — §03 §1 platform.promotion_queue[] SoT in state.json (not hierarchy queue JSON); drain_policy, divergence_log, metrics; J6 separation.
- [x] `documents/plans/full-automation/H1.4-state-pursuit-block.md` — §03 §1 pursuit block + legacy field-placement table; mode enum (not "continue"); stopped_reason taxonomy; master authoritative over contaminated Reader placement.
- [x] `documents/plans/full-automation/H1.5-state-hitl-block.md` — §03 §1 hitl{pending, since, payload} + self_gate_mode; H3 mirrors gates_pending.
- [x] `documents/plans/full-automation/H1.6-state-company-block.md` — §03 §1 company{pack_id, pack_version, active_role, role_queue, role_forbidden_reads}; manifest/leases in program+lane.json not company block.
- [x] `documents/plans/full-automation/H1.7-state-active-workflow-block.md` — §03 §3.4 `pursuit.active_workflow` (current_node_id, completed_nodes, retry_counts, branches, terminal_nodes, validation_hash) + §06 v2.26.
- [x] `documents/plans/full-automation/H2-journal-progress.md` — §03 persistence H2 mirror sections; state.json wins on conflict; §06 cross-cutting dual-write + A6.3 observe-without-unblock.
- [x] `documents/plans/full-automation/H3-SIGNOFF-BUNDLE.md` — hierarchy certification bundle (hierarchy-expander certify); separate from runtime state schema; not §03 state block.
- [x] `documents/plans/full-automation/H3-artifact-graphs.md` — §05 Plane H H3 staleness graph; §06 v2.18 E5.* platform nodes + pack artifact-graph.json.
- [x] `documents/plans/full-automation/H4-evidence.md` — §05 Plane H H4 immutable evidence/; task (G1) + workflow node rollup (G2.5/C6.5 v2.26).
- [x] `documents/plans/full-automation/H5-worker-runs.md` — §03 §1 H5 worker-runs.jsonl audit contract; §06 v2.15 spawn logging; goal/lane correlation; conductor-only writer.
- [x] `documents/plans/full-automation/H6-snapshots.md` — §03 §1 H6 preCompact→sync-state.py; journal/snapshots/; repair order dual-write > snapshot > H2; §06 G6.3 field list + active_workflow v2.26.

## Branch I (21)

- [x] `documents/plans/full-automation/I1-index.md` — index only; I1.1–I1.4 covered §03 §7 I1 + §06 v2.15.
- [x] `documents/plans/full-automation/I1.1-runtime-ide-genius-conductor-session.md` — §03 §7 I1.1 genius conductor; S0-first; B3.1 orchestrate-only when spawn_workers.
- [x] `documents/plans/full-automation/I1.2-runtime-ide-local-subagents-economy.md` — §03 §7 I1.2 economy subagents; C4.2 parallel gate; H5 audit.
- [x] `documents/plans/full-automation/I1.3-runtime-ide-slash-commands-autopilot-continue-lane-verify.md` — §03 §7 I1.3 full slash command inventory; commands ≠ H2/H3 approval.
- [x] `documents/plans/full-automation/I1.4-runtime-ide-hooks-beforesubmit-subagentstart-pretooluse-prec.md` — §06 v2.15 I1.4 hook set incl. preCompact/preToolUse/E4.2 inject.
- [x] `documents/plans/full-automation/I2-index.md` — index only; I2.1–I2.3 covered §03 §7 I2 + §06 v2.15/v2.18.
- [x] `documents/plans/full-automation/I2.1-runtime-sdk-run-local-pipeline-goal-autopilot.md` — §03 §7 I2.1 run-local-pipeline goal_autopilot; typed auth-fail stop.
- [x] `documents/plans/full-automation/I2.2-runtime-sdk-cursor-api-key-autopilot-model.md` — §03 §7 I2.2 CURSOR_API_KEY/AUTOPILOT_MODEL; facts INDEX; structured H2 on missing creds.
- [x] `documents/plans/full-automation/I2.3-runtime-sdk-operator-pc-worker-server.md` — §03 §7 I2.3 operator PC worker-server; C4.1 leases; evidence sync-back; network partition H2.
- [x] `documents/plans/full-automation/I3-index.md` — index only; I3.1–I3.3 covered §06 v2.18.
- [x] `documents/plans/full-automation/I3.1-runtime-headless-headless-verify.md` — §03 §7 I3.1 S0/disk-first headless-verify; last_verify for IDE resume.
- [x] `documents/plans/full-automation/I3.2-runtime-headless-github-actions-validate-verify.md` — §03 §7 I3.2 CI conformance ≠ goal_verify/H3 clearance.
- [x] `documents/plans/full-automation/I3.3-runtime-headless-pull-ready-complete-work-order-lanes.md` — §03 §7 I3.3 S0-only lane dual-write; conductor merge.
- [x] `documents/plans/full-automation/I4-index.md` — index only; I4.1–I4.4 covered §03 §7 I4 + §06 v2.20/v2.26.
- [x] `documents/plans/full-automation/I4.1-runtime-external-mcp-browser-dcc-cloud.md` — §03 §7 I4.1 MCP per-role allowlist; browser lock/navigate/unlock; conductor-owned state.
- [x] `documents/plans/full-automation/I4.2-runtime-external-tool-operator-tool-command-task-cards.md` — §03 §7 I4.2 tool-operator; no product-source edits; Tool command on task cards.
- [x] `documents/plans/full-automation/I4.3-runtime-external-evidence-types-non-pytest.md` — §03 §7 I4.3 non-pytest evidence types; evidence-types.md S0 validation.
- [x] `documents/plans/full-automation/I4.4-transistor-executors-mcp-tool-script-boundary.md` — §03 executor.kind (script/tool/soft_template/gate) + §06 v2.26 (S0 scripts, tool-operator/MCP allowlist, never bypass preToolUse, artifact handoff in I/O).
- [x] `documents/plans/full-automation/I5-index.md` — index only; I5.1–I5.2 covered §06 v2.23.
- [x] `documents/plans/full-automation/I5.1-runtime-notify-status-dashboard-generation.md` — §03 §7 I5.1 dashboard + STATUS; staleness-aware; journal-keeper regen.
- [x] `documents/plans/full-automation/I5.2-runtime-notify-webhook-email-h2-h3-only.md` — §03 §7 I5.2 H2/H3 + milestone webhooks; strict-env disable; A6.3 observe-without-unblock.

## Branch J (7)

- [x] `documents/plans/full-automation/J-index.md` — index only; J1–J6 covered §03 §8 + §05 Plane J.
- [x] `documents/plans/full-automation/J1-model-policy.md` — §03 §8 J1 model-policy.json tiers/routing; validate-workflow after policy edit; §06 v2.15 B1.2/I1.1.
- [x] `documents/plans/full-automation/J2-automation-waivers.md` — §03 §8 J2 structured waivers (expiry, goal_ids); template self-build v2.16; H3 never permanently waived; §06 J2/J4.
- [x] `documents/plans/full-automation/J3-strict-hitl.md` — §03 §8 J3 strict_hitl in model-policy + self_gate_mode; restores HLD/DD gates not H1/H2/H3 contract; §06 v2.15.
- [x] `documents/plans/full-automation/J4-audit.md` — §03 §8 J4 audit plane (worker-runs, waivers, evidence immutability, retention); §06 v2.15 H5 + v2.23.
- [x] `documents/plans/full-automation/J5-export-contract.md` — §03 §8 J5 export-contract redaction profiles, pack extensions, H3 export approval; §06 v2.26 active_workflow.
- [x] `documents/plans/full-automation/J6-release-queue.md` — §03 §8 J6 harness-only release-queue (≠ platform.promotion_queue); v2.14–v2.28; run-next-release.py; §06 v2.16/v2.28.

---

## Progress

- Verified: **348 / 348 (100%)**
- Last batch: Batch 12 — Branch J complete. **07 traceability final pass complete (2026-06-28).**
- Next action: begin implementation from `06-MASTER-CHECKLIST.md` v2.14.
