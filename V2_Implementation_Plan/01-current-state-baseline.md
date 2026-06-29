# 01 — Current State Baseline (v2.13)

Inventory of what **already exists** in the repo as of 2026-06-28. This is the starting line; the [gap analysis](02-gap-analysis.md) is *vision − this*.

Verdict legend: **DONE** = shipped & usable · **PARTIAL** = exists but incomplete vs vision · **MISSING** = not present.

---

## A. Core pipeline scripts (`scripts/`) — DONE

| Script | Purpose |
|--------|---------|
| `route-tier.py` | Map `next_action` → capability class, model tier, `spawn_workers` from `model-policy.json`. |
| `validate-workflow.py` | v2 conformance: workflow artifacts + `state.json` consistency. |
| `sync-state.py` | Repair/validate `progress.md` vs `state.json` (stdlib only). |
| `generate-dashboard.py` | Generate `docs/operator/dashboard.md` + refresh `STATUS.md`. |
| `headless-verify.py` | Headless verify → delegates to `verify-router.py`. |
| `verify-router.py` | Run Test/Tool command from a task card; write `evidence/`. |
| `update-staleness.py` | Update `staleness.json` from dep graph + mtimes. |
| `new-task-card.py` | Create a task card markdown from title/fields. |
| `pull-ready-work-orders.py` | List leasable work orders from program lanes. |
| `complete-work-order.py` | Validate evidence for a lane task, release lease. |
| `automation/run-local-pipeline.py` | Local SDK pipeline driver: loop-until-blocked. |
| `automation/check-pipeline-blocked.py` | S0 gate: exit 0 = run, 1 = blocked. |

> Note: `scripts/automation/` also holds ~46 **hierarchy/HTML-publication** scripts (the brainstorming-doc toolchain). These are unrelated to the v2 harness runtime but must not be broken by harness changes.

## B. Skills (`.cursor/skills/`) — 28 present (PARTIAL vs vision)

Present and relevant: `autopilot`, `continue`, `spec-parser`, `hld-writer`, `dd-writer`, `diagram-generator`, `task-breakdown`, `scaffold-project`, `implement-feature`, `test-writer`, `test-ui-automation`, `refactor`, `git-workflow`, `iterative-feature`, `journal-keeper`, `librarian`, `orchestrate-subagents`, `orchestrate-program`, `program-scoper`, `integration-manifest-keeper`, `reconcile-stale`, `reconcile-artifact-graph`, `playbook-keeper`, `verifier`, `tool-operator`, `generate-dashboard`, `remember`, `hierarchy-expander`.

**MISSING skills (vision):** `goal-keeper`, `workflow-composer`.

## C. Commands (`.cursor/commands/`) — DONE

`/autopilot`, `/continue`, `/status`, `/gate`, `/task`, `/verify`, `/research`, `/model`, `/program`, `/lane` (+ `/expand-hierarchy`).
**MISSING (vision):** `/goal`, `/workflow` (or fold into existing) — optional, see roadmap.

## D. Rules (`.cursor/rules/`) — DONE (extend later)

`approval-gates`, `autopilot`, `conductor`, `dd-api`, `deterministic-first`, `evidence-required`, `facts-retrieval`, `genius-conductor`, `integration-manifest`, `pipeline-continue`, `program-conductor`, `test-before-push`.
**To add:** compose-first rule (v2.17), workflow-compose-before-implement rule (v2.25/26).

## E. `journal/state.json` — PARTIAL (greenfield v2 baseline)

Present top-level keys: `version(2)`, `spec_file`, `spec_version`, `mode`, `phase`, `feature_id`, `pipeline_id`, `repo_url`, `current_branch`, `last_completed`, `next_action`, `context_files`, `allowed_reads`, `forbidden_reads`, `gates_pending`, `blocking_questions`, `deferred_questions`, `resolved_qa_archive`, `blockers`, `pause_reason`, `last_failure`, `completion_status`, `evidence_required`, `evidence_files`, `last_verify`, `last_session_summary`, `capability_class`, `model_tier`, `spawn_workers`, `subagent_models`, `model_escalation`, `genius_session_recommended`, `program(null)`, `autopilot{active,max_steps_per_session:25,steps_this_session,stopped_reason}`.

**MISSING blocks (vision §20):** `goal`, `pursuit` (+ `pursuit.active_workflow`), `platform`, `company`, `hitl`.

## F. `docs/` — PARTIAL

| Path | Verdict |
|------|---------|
| `docs/manifest/staleness.json` | DONE (v1 graph, design nodes only) |
| `docs/manifest/pipelines/*.yaml` | DONE (3: software-greenfield, data-platform-program, multi-domain-program) |
| `docs/operator/model-policy.json` | DONE |
| `docs/operator/dashboard.md`, `export-contract.md`, `evidence-types.md` | DONE |
| `docs/facts/INDEX.md` | DONE (placeholders) |
| `docs/decisions/` | DONE (`decisions.md`, `automation-waivers.md`, `archive.md`) |
| `docs/playbooks/INDEX.md` | PARTIAL — empty index; 2 unindexed playbooks (`blender-export.md`, `ue-import.md`) |
| `docs/platform/CATALOG.md` | MISSING |
| `docs/platform/transistors/` + `TRANSISTORS.md` + `schemas/` | MISSING |
| `docs/workflows/` (DAG JSON) | MISSING |

## G. `template-packs/` — PARTIAL (2 stub packs)

| Pack | Has | Missing vs vision |
|------|-----|-------------------|
| `game-asset-pipeline` | `README.md`, `manifest.md`, `artifact-graph.json`, `playbooks/{blender-export,ue-import}.md` | `company.yaml`, `roles/`, `pipelines/`, `verify/`, `transistors/`, `workflows/` |
| `data-platform` | `README.md`, `manifest.md`, `artifact-graph.json` | `company.yaml`, `roles/`, `pipelines/`, `playbooks/`, `verify/`, `transistors/` |
| `_shared/` | — | MISSING entirely |

## H. Tests (`tests/`) — PARTIAL

- `tests/unit/` — **12 files**: `test_autopilot_state`, `test_check_pipeline_blocked`, `test_route_tier`, `test_verify_router`, `test_lane_scripts`, + 7 hierarchy/HTML tests.
- `tests/integration/` — **MISSING**
- `tests/e2e/` — **MISSING**

---

## One-line baseline summary

The **verified-delivery harness is shipped** (conductor, state machine, evidence gates, tier routing, program mode, autopilot-until-blocked, lanes, 2 stub packs). What is **not** built is everything that turns it into the *ultimate autonomous worker*: the **goal/pursuit model**, the **platform promotion queue + scheduler**, the **catalog/compose-first** discovery surface, **full company packs**, and the entire **transistor + generator-workflow** layer.
