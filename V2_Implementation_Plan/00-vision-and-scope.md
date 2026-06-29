# 00 — Vision & Scope

Distilled from [`documents/full-automation-vision-and-hierarchy.md`](../documents/full-automation-vision-and-hierarchy.md) (§0–§1, §14, §21) and the INTRO-* / SEC-* leaves.

---

## North star

> An agent-driven expert system that **pursues verified goals autonomously**, maintains a **parallel platform stack** of reusable building blocks, and scales to **full organizational workflows** via template-packs — with human involvement limited to **initial planning, blocker resolution, and final sign-off**.

The conductor behaves like a senior tech lead who **composes generator workflows from proven "transistors," executes one verified block per turn, and promotes yesterday's improvisation into tomorrow's catalog entry** — until `goal_verify` passes and only H3 remains for the human.

---

## The four structural shifts (what we are building toward)

| # | Shift | From (v2.13) | To (v2.28) |
|---|-------|--------------|------------|
| 1 | **Pursuit loop** | Burst → update → wait for "Continue"; autopilot capped at 25 steps | Run until goal verified; `goal_autopilot` default after H1 |
| 2 | **Dual-stack with platform queue** | Platform/distillation optional and manual | Product never waits on distillation; platform queue drained on a schedule, never starves |
| 3 | **Template-pack = company** | Two stub packs (manifest + graph only) | Roles, pipelines, integrations, artifact graphs compose entire studios/enterprises |
| 4 | **Transistor workflows** | Long prose implement chains; prose-only skills | **Generator-first:** compose verified workflow DAGs from transistors; agents assemble generators — code, docs, assets are terminal-node outputs, not direct inline work |

---

## Human touchpoint contract (minimal HITL)

Only **three** classes of human interaction. Everything else (including HLD/DD *review*) becomes an **agent self-gate with evidence**, unless the operator explicitly enables `strict_hitl`.

```
H1 — Initial planning gate
      Input:  spec / mega-spec / company charter
      Output: approved plan artifact (HLD or program milestone + manifest, and the generator workflow DAG)
      Once:   per project / program / company template instantiation

H2 — Blocker assistance
      Trigger: check-pipeline-blocked OR goal_verify failed OR external dependency (creds/access)
      Output:  answer, credential, access, or decision with recorded rationale
      Async:   system pauses, notifies (digest), resumes when unblocked

H3 — Final sign-off
      Trigger: goal_verification.passed == true
      Output:  accept / reject with notes → reject re-enters the pursuit loop
      Once:    per goal milestone or release
```

**Continue is redefined:** "continue" = *resume the pursuit loop if not blocked*. It is **not** approval and **not** an answer to an open question. (This preserves the existing `approval-gates` and `pipeline-continue` rules while adding the pursuit semantics.)

---

## Goal completion criterion

A goal is **achieved** only when **all** hold:

1. **Acceptance artifacts** exist (tests, logs, demos, manifests).
2. **Automated verification** passes (`goal_verify` suite).
3. **Staleness / integration graph** is consistent.
4. **No `blocking_questions`** without `deferred_with_rationale`.
5. **Platform debt** for this goal is either promoted or explicitly waived with an expiry.

The agent **does not stop** for status updates. It stops only on: **H1/H2/H3**, **unrecoverable failure**, or **resource budget cap** (see Stop-reason taxonomy in plane A / [05](05-workstreams-by-plane.md)).

---

## Scope: in vs out (by policy)

| In scope (automate) | Out of scope (by policy) |
|---------------------|--------------------------|
| All SDLC phases after the initial plan is approved | Initial requirements elicitation without a seed spec |
| Implement, test, refactor, integrate, deploy-prep | Irreversible production actions without verify + rollback path |
| Multi-role company workflows via template-packs | Legal/financial actions requiring human authority of record |
| Blocker **detection** and structured escalation | Blocker **resolution** when external creds/access are missing |
| Self-improvement of the harness (platform queue) | Silent waiver of safety gates |
| Final deliverable + evidence bundle for sign-off | Subjective aesthetic approval unless encoded as acceptance tests |

---

## Authority & known caveats (read before trusting a single leaf)

The 281 spec leaves (+ H3-SIGNOFF certification bundle) were machine-expanded and carry some **template contamination**. Use this authority order when sources disagree:

1. **Vision §15 roadmap** (release schedule) and **§19/§20** (transistor model + state sketch).
2. **SEC-18** transistor A–Z reference (`SEC-18-transistor-model-a-to-z-reference.md`).
3. **V2 master plan** [03-target-architecture.md](03-target-architecture.md) §5 + [docs/decisions/v2-evolution-policy-adrs.md](../docs/decisions/v2-evolution-policy-adrs.md) (ADR-V2-007 generator-first).
4. **APP-B** state sketch + each capability leaf's **Reader narrative**, **State/data fields**, and **Repo artifacts** sections.
5. **INDEX titles**.

Do **not** trust, without cross-checking the above:
- Leaf **Behavior / step logic** sections — several contain steps copied from unrelated nodes (pass-3 contamination).
- Release headers were bulk-reconciled to [07-traceability-matrix.md](07-traceability-matrix.md) (2026-06-28); if drift recurs, **07 + 04 + 06** win over leaf headers.

This caveat is also recorded in [07-traceability-matrix.md](07-traceability-matrix.md). Cleaning the leaf prose is itself a candidate platform-queue item, not a blocker for implementation.

## Ten planes (master hierarchy)

```
FULL AUTOMATION SYSTEM
├── A. Pursuit & control plane          (never stop until verified)
├── B. Cognition & routing plane        (S0–S4, genius conductor, workers, transistor composer B6)
├── C. Product execution plane          (pipelines, tasks, evidence, workflow-compose C6)
├── D. Platform evolution plane         (parallel queue, promotion ladder L0–L6)
├── E. Knowledge & composition plane    (catalog, playbooks, facts, packs, transistor registry E6/E7)
├── F. Organization plane               (template-packs = companies)
├── G. Verification & quality plane     (anti-mistake immune system)
├── H. Persistence & state plane        (journal, state, graphs, leases, active_workflow)
├── I. Runtime & integration plane      (IDE, SDK, headless, external tools, executors)
└── J. Governance & operator plane      (policy, waivers, audit, dashboards)
```

The **transistor & generator-workflow model** (vision §19) is not a separate plane; it threads through B6, C6, D1.7, D4.7, D6.5, E5.4, E6, E7, F1.9, F5.4, G2.5, G5.8, G6.4, H1.7, I4.4 and ships in releases **v2.24–v2.28**.

---

## Design decisions already resolved (do not re-litigate)

| Decision | Resolution | Leaf |
|----------|------------|------|
| Transistor granularity | One verify boundary per block; if verify isn't one command/predicate, split. Max soft scope = one bounded S1 job. Whole-task implement = a workflow, not one transistor. | SEC-17-7 |
| Composer placement | S3 `workflow-composer` skill, catalog-only reads; conductor approves + dual-writes, does **not** compose large DAGs inline | SEC-17-8 |
| Visual vs JSON workflow | JSON DAG required + authoritative (v2.25+); visual editor optional operator tooling (v2.28+), never a substitute for schema validation | SEC-17-9 |
| Transistor library scope | Two-tier: `template-packs/_shared/transistors/` (global) + pack overlay; `list-transistors` merges with `pack_id` filter; overlay overrides `_shared` only via semver fork | SEC-17-10 |
| New top-level plane? | **No Branch K** — transistors extend planes B, C, D, E, F, G, H, I (unify E+C+D) | SEC-18 §C-5 |
| Transistor vs L2 script | **L6 wraps L2**; the script is the executor implementation inside a hard transistor | SEC-18 §C-6 |
| Transistor vs skills | **Skills orchestrate phases; transistors execute steps.** Skills become soft-executor internals | SEC-18 §C-7 |
| Compose-before-implement scope | **Workflow DAG required (default)** for all deliverable-producing work — code, docs, diagrams, assets, configs. Catalog compose-first is a **sub-step** when binding each DAG node. Narrow exemptions only: S0 mechanical, coordination-only tasks, observe-only, J2 harness waiver. Bridge mode v2.17–v2.24 until L2 ships. | ADR-V2-007, SEC-18 §C-9, INTRO-2, C6.1 |
| SEC-17-1 self-gate | Default `checklist`; escalate to economy `reviewer` on risk triggers; `dual_reviewer` when strict pack requires | ADR-V2-001 |
| SEC-17-2 H3 scope | Default per **milestone**; pack `h3_scope` overrides | ADR-V2-002 |
| SEC-17-3 K ratio | Adaptive K, floor 1:5; queue depth samples in `platform.metrics` | ADR-V2-003 |
| SEC-17-4 budget | `goal.deadline` authoritative; precedence wall → steps → tokens → session cap | ADR-V2-004 |
| SEC-17-5 pack authority | legal/finance/compliance → `H2-always` unless waiver | ADR-V2-005 |
| SEC-17-6 multi-goal | Single stack until v2.19; preemption ADR when `company_autopilot` enabled | ADR-V2-006 |
| Platform debt at goal done | `platform_debt_clear_for_goal()` — goal-scoped queue items promoted or waived-with-expiry | ADR-V2-008 |
| Writer authority | Conductor sole state/journal writer; workers summaries only | ADR-V2-009 |

Full ADR text: [docs/decisions/v2-evolution-policy-adrs.md](../docs/decisions/v2-evolution-policy-adrs.md). Operator may override any ADR at **H1** with journal record; do not silently diverge during implement.

## Operator override at H1

If defaults above are wrong for your program, record the override in journal **Resolved Q&A** and update the matching ADR row. Overrides needed before: v2.15 (ADR-001, 002, 004), v2.16 (003), v2.19 (005, 006), v2.26 (007 enforcement).
