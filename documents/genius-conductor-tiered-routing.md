# Genius conductor, tiered routing, and deterministic harness

Design notes for a planned evolution of the AIDeveloper expert system (v2.4+). Captures brainstorming on **model cost**, **Fable / genius-tier orchestration**, **subagent delegation**, and **scripts-first** workflows.

**Status:** Implemented v2.4–v2.12. See `documents/plans/v2-full-evolution.md`.

**Related:** [v2 verified delivery harness](spec-to-artifacts-agent-skills-system.md#8-v2-verified-delivery-harness), [export contract](../docs/operator/export-contract.md), [orchestrate-subagents skill](../.cursor/skills/orchestrate-subagents/SKILL.md).

---

## 1. Goals

1. **Spend premium model capacity only on irreplaceable thinking** — architecture, ambiguity, gates, escalation.
2. **Move bulk token usage to economy subagents** — implement, explore, shell verify.
3. **Move repeatable work to zero-token deterministic code** — scripts, hooks, CI (extend v2 `scripts/`).
4. **Avoid false “auto-switch” promises** — be explicit about what Cursor can and cannot do for the parent Composer model.
5. **Align with long-horizon orchestration models** (e.g. Claude Fable 5 in Cursor) as the **Genius parent**, not as the model that writes every line of code.

---

## 2. Problem with naive model switching

| Approach | Issue |
|----------|--------|
| Switch Composer model every `next_action` | Cursor does not reliably change the **parent** Agent model via hooks; frustrates operators. |
| One cheap model for everything | Weak HLD/DD, gate bypass, rework → higher total cost and risk. |
| One premium model for everything | Expensive boilerplate (tests, scaffold, git) wastes Fable/Opus capacity. |
| LLM for clerical steps | Parsing journal, running pytest, refreshing dashboard — already solved in v2 by Python. |

**Target behavior:** Genius parent orchestrates; workers implement; scripts clerk.

---

## 3. Three-layer stack

```text
┌─────────────────────────────────────────────────────────┐
│  Layer A: Genius parent (Fable / best available)        │
│  Planning, gates, orchestration, journal/state, merge   │
│  Human selects model once per orchestration session     │
└──────────────────────────┬──────────────────────────────┘
                           │ spawn Task / explore / shell
┌──────────────────────────▼──────────────────────────────┐
│  Layer B: Economy workers (subagents)                   │
│  Implement, Librarian explore, Verifier shell, review   │
│  Model chosen automatically when spawning workers       │
└──────────────────────────┬──────────────────────────────┘
                           │ invoke without LLM
┌──────────────────────────▼──────────────────────────────┐
│  Layer C: Deterministic harness (scripts, hooks, CI)    │
│  validate-workflow, sync-state, dashboard, headless-verify│
│  Zero LLM tokens                                        │
└─────────────────────────────────────────────────────────┘
```

This extends v2’s **conductor + workers + evidence** design; it does not replace `journal/state.json` or approval gates.

---

## 4. Genius parent (Fable and equivalents)

[Claude Fable 5](https://cursor.com/docs/models/claude-fable-5) (Anthropic Mythos-class, available in Cursor) is aimed at **long-horizon, multi-step agent work** — planning across stages, delegating to sub-agents, fewer check-ins. That matches the **Genius conductor** role.

### Parent responsibilities (only)

- Blocking questions and expert-system clarification
- Human gates (HLD, DD, feature design)
- Orchestrating subagents ([orchestrate-subagents](../.cursor/skills/orchestrate-subagents/SKILL.md))
- Dual-writing `journal/progress.md` + `journal/state.json` (or approving script output)
- Escalation decisions after failed evidence
- Reviewing worker summaries (not re-reading entire repos inline)

### Parent should not (by default)

- Grep large codebases for routine implement tasks
- Run full test suites in the parent context (use **Verifier** shell subagent)
- Read full DD/HLD during implement phase (use **Librarian** + `allowed_reads` + task cards + playbooks)
- Re-implement tasks that an economy worker can do from a task card

### Operator setup

- Select **Fable** (or the configured `genius_models` entry) in the Cursor Composer model picker for the **orchestration chat**.
- Keep that model for the session (e.g. a “design day” or “continue” session) rather than switching every phase.
- Dashboard / `state.json` will recommend **Genius session** vs **delegate-heavy session** (implement phase).

When Fable is unavailable or plan-limited, policy falls back to “best available” genius tier (e.g. Opus-class) — see [model policy stub](../docs/operator/model-policy.json).

---

## 5. How model “switching” actually works

| Layer | Switched automatically? | How |
|-------|-------------------------|-----|
| **Parent Composer** | **No** (not reliably) | Operator picks Genius model once per session; rules + dashboard **nudge** |
| **Subagents** | **Yes** | Conductor spawns Task/explore/shell with `model` from policy |
| **Scripts / hooks / CI** | N/A | No model; deterministic |

**Do not** document or implement “silent Composer model flip every `next_action`” as a guarantee.

**Do** document:

1. Genius parent stays on Fable (or fallback) for orchestration.
2. Implement / explore / verify run on **economy workers** by default.
3. Clerical steps run via **scripts** without LLM.

---

## 6. Capability classes (S0–S4)

Route work by **capability class**, not only by file type or phase name.

| Class | Description | Execution | Model tier |
|-------|-------------|-----------|------------|
| **S0** | Deterministic clerical | `scripts/`, hooks, GitHub Actions | None |
| **S1** | Mechanical code/test from spec | Economy subagent + task card + playbooks | Economy |
| **S2** | Structured artifacts from templates | Standard subagent or script-assisted | Standard |
| **S3** | Architecture, ambiguity, tradeoffs | Genius parent or premium subagent | Genius |
| **S4** | Governance, gates, security, escalation | Genius parent | Genius |

### Example mapping from `next_action`

| `next_action` (prefix) | Class | Notes |
|------------------------|-------|--------|
| `run spec-parser` (blocking Q) | S3 | Genius parent |
| `run hld-writer`, `run dd-writer` | S3 | Genius parent or premium phase worker |
| `wait for … approval` | S4 | Genius parent talks to human |
| `run diagram-generator`, `run task-breakdown` | S2 | Template-heavy |
| `run scaffold-project` | S1–S2 | Often delegable |
| `implement-feature` | S1 | Economy worker; Genius merges |
| `run git-workflow (push)` | S0 + S1 | Scripts validate; shell runs tests |
| `reconcile-stale` | S3 | Genius |
| Verifier / `validate-workflow.py` | S0 | No LLM |
| Failed evidence retry | S4 → S1 | Escalate once on Genius, then economy retry |

### Escalation loop

1. Implement on **S1** (economy worker) → Verifier fails.
2. State sets `capability_class: S4`, `model_escalation: true`.
3. One retry with Genius parent or premium subagent reviewing task card + failure log.
4. If still failing → blocker; human decision (not infinite premium spend).

---

## 7. Deterministic-first rule

**Principle:** If a step is a function of files on disk (parse JSON, diff spec, run tests, check evidence paths), it must **not** be an agent turn.

### Already in v2 (S0)

| Artifact | Role |
|----------|------|
| `scripts/validate-workflow.py` | Conformance |
| `scripts/sync-state.py` | Journal ↔ state repair |
| `scripts/generate-dashboard.py` | Operator dashboard + STATUS |
| `scripts/headless-verify.py` | Scheduled verify stub |
| `.cursor/hooks/` | Context injection, read guards, compaction snapshots |
| `.github/workflows/` | CI validate + verify schedule |

### Planned S0 expansions (v2.4+)

| Step | Proposed script |
|------|-----------------|
| Tier/class for `next_action` | `scripts/route-tier.py` |
| Staleness from file mtimes | `scripts/update-staleness.py` |
| New task card from TODOS | `scripts/new-task-card.py` |
| Evidence gate before advance | Extend `validate-workflow.py` |

**Planned rule:** `.cursor/rules/deterministic-first.mdc` — before an agent turn, check if a script in `scripts/` or a hook already performs the step.

---

## 8. Model policy (configuration)

Policy lives in **`docs/operator/model-policy.json`** (operator-editable). Tiers are stable; Cursor model IDs change.

### Tier definitions (conceptual)

| Tier | Purpose | Example Cursor / API ids (change over time) |
|------|---------|-----------------------------------------------|
| **genius** | Orchestration, S3–S4 | `claude-fable-5`, top Mythos-class |
| **standard** | S2 structured work | Sonnet-class, Composer default |
| **economy** | S1 workers | Fast / mini / composer-fast variants |

### Routing

- Map **`next_action`** prefixes and **subagent roles** to tier (see stub JSON).
- **journal-keeper** (when implemented) sets `capability_class`, `model_tier`, `spawn_workers` alongside `next_action`.

### Planned `state.json` fields (v2.4)

```json
{
  "capability_class": "S3",
  "model_tier": "genius",
  "spawn_workers": false,
  "subagent_models": {
    "librarian": "economy",
    "phase_worker": "economy",
    "reviewer": "genius"
  },
  "model_escalation": false,
  "genius_session_recommended": true
}
```

---

## 9. Subagent defaults (orchestrate-subagents)

| Role | Subagent type | Default tier | Writes |
|------|---------------|--------------|--------|
| Librarian | explore (readonly) | economy | nothing |
| Phase worker (implement) | generalPurpose | economy | src/tests per task card |
| Phase worker (HLD/DD) | generalPurpose | genius (optional) | design docs only |
| Verifier | shell | n/a (shell) | `evidence/*.log` |
| Reviewer | bugbot / security-review | genius | review notes |

**Conductor** merges worker output and dual-writes journal/state. Workers must not update `next_action` or gates ([subagentStart hook](../.cursor/hooks/cursor_context_hook.py) reinforces contract).

---

## 10. Operator UX

| Surface | Shows |
|---------|--------|
| `docs/operator/dashboard.md` | `capability_class`, `model_tier`, “Genius session recommended”, escalation flag |
| `/status` command | Same, no design doc reads |
| Planned `/model` command | Current tier + policy recommendation |
| `STATUS.md` | Short summary line from dashboard script |

**Implement phase message (example):** “Stay on Genius as conductor; spawn economy workers for task N. Do not implement large changes inline.”

---

## 11. Cost and quality strategy

- **Fable / genius on parent** is affordable when each parent turn is thin: read `state.json`, spawn worker, merge summary — not 2k lines of code per turn.
- **Playbooks** ([docs/playbooks/](../docs/playbooks/)) reduce S1 tokens over time.
- **Evidence gates** prevent marking S1 complete without proof — avoids cheap model “done” hallucinations.
- **Escalation** limits premium spend to failed or high-risk paths.

---

## 12. Headless and external runtimes

[`export-contract.md`](../docs/operator/export-contract.md) can export `capability_class` and `model_tier` for OpenClaw / Hermes / GitHub Actions. External jobs should:

- Run **S0** scripts on schedule (validate, verify).
- Not require Genius model for cron work.
- See [`integrations.md`](../docs/operator/integrations.md).

---

## 13. Out of scope (for this design)

- Silent automatic flip of parent Composer model every phase (until Cursor exposes a reliable API/hook).
- Billing integration with Cursor/Anthropic usage APIs.
- FTS / global cross-session memory (use playbooks + facts INDEX instead).
- Replacing human approval gates with model tier logic.

---

## 14. Implementation roadmap

| Phase | Status |
|-------|--------|
| **v2.4** | Implemented — tier fields, rules, work orders, dashboard |
| **v2.5** | Implemented — `route-tier.py`, `/model`, worker-runs audit |
| **v2.6** | Implemented — staleness/task-card scripts, validate extensions |
| **v2.7** | Implemented — program mode, pipelines, program-scoper |
| **v2.8** | Implemented — artifact graph, reconcile-artifact-graph |
| **v2.9** | Implemented — orchestrate-program |
| **v2.10** | Implemented — verify-router, tool-operator |
| **v2.11** | Implemented — lane lease, pull/complete scripts |
| **v2.12** | Implemented — template packs, design doc §10 |
| **v2.13** | Implemented — local autopilot, `check-pipeline-blocked`, `run-local-pipeline` |

See [documents/plans/v2-full-evolution.md](../documents/plans/v2-full-evolution.md) and `docs/automation/README.md`.

---

## 16. Local autopilot (v2.13)

Run the pipeline on **your PC** without repeated Continue:

- **In-IDE:** `/autopilot` — genius-tier parent loops continue steps; spawns **local** economy subagents per step when `spawn_workers` is true.
- **S0:** `scripts/automation/check-pipeline-blocked.py`
- **SDK (optional):** `scripts/automation/run-local-pipeline.py` with **local** runtime (`cursor-sdk`, not Cloud Agents).

Stops on gates, blocking questions, evidence wait, or `max_steps_per_session`. Does not clear human gates automatically.

---

## 15. Summary

| Question | Answer |
|----------|--------|
| Who uses the genius tier? | **Orchestration parent** for S3–S4 (operator selects best genius-tier model in UI; see `model-policy.json`). |
| Where do most tokens go? | **Economy subagents** for implement, explore, shell. |
| Where do zero tokens go? | **Scripts, hooks, CI** (expand v2 harness). |
| Does the parent model auto-switch? | **No** — stable Genius session + automatic **worker** models. |
| What is the expert system’s job? | Route by `state.json`, enforce delegation, evidence, and deterministic-first — not maximize LLM usage. |

---

*Last updated: 2026-06-26 — v2.4–v2.13 implemented.*
