# 10 — Implementation Readiness (100% spec gate)

**Read this before starting v2.14 code.** This document defines when the master plan is **spec-complete** vs when the **system is built**.

---

## Plan vs implementation (never conflate)

| Artifact | Measures | Status today |
|----------|----------|--------------|
| [08-coverage-ledger.md](08-coverage-ledger.md) | Every source `.md` is **plan-covered** (idea lives in 00–09) | 348/348 plan-covered |
| [06-MASTER-CHECKLIST.md](06-MASTER-CHECKLIST.md) | Every feature is **built and verified** in the repo | 0/N implementation checkboxes |
| [11-implementation-tracker.md](11-implementation-tracker.md) | Same todos as 06 with **stable IDs + progress %** | 0/293 done |
| [07-traceability-matrix.md](07-traceability-matrix.md) | Leaf ID → release → checklist row | Complete |

**Rule:** A row in `08` marked `[x]` means **traceability**, not shipped code. Only `[x]` in `06` (with passing verify command) means implemented.

### Implementation status (update after each release)

| Release | 06 items done | Exit gate | Tag |
|---------|---------------|-----------|-----|
| Pre-flight | 0 / TBD | — | — |
| v2.14 | 0 / TBD | — | — |
| … | | | |
| v2.28 | — | — | — |

Conductor updates this table at each release tag.

---

## Bridge sunset policy (ADR-V2-007)

`goal.workflow_policy` controls generator-first enforcement:

| Policy | Allowed when | Meaning |
|--------|--------------|---------|
| `bridge` | v2.14–v2.24 only | L1 compose-first on task cards; phase skills allowed for deliverables |
| `required` | **Default from v2.25** | L2+L3: validated workflow DAG + one transistor node per turn |
| `exempt` | Operator waiver only | Row in [automation-waivers.md](../docs/decisions/automation-waivers.md) with expiry |

**Mandatory transitions:**

1. **v2.25:** All active goals auto-flip `bridge` → `required` unless explicit waiver row (see `migrate-bridge-to-workflow.py` in 06).
2. **v2.26:** Bridge mode **disabled by default** in state template; enabling bridge requires waiver + expiry.
3. **v2.28 final acceptance:** Sign-off line **"Bridge mode disabled; generator-first enforced."**

---

## Human checkpoint (moved)

The **recommended operator checkpoint** is **after v2.26 exit gate**, not v2.23:

- v2.23 delivers operator polish (dashboard, H2 digest) but **not** generator-first enforcement.
- v2.26 delivers `active_workflow`, forbidden phase-skill routing, and generator-only deliverables.

At checkpoint: review SEC-18 §Q progress, fuzzy-chain metrics, and reference-pack workflow coverage before v2.27–28 polish.

---

## P0 readiness gates (blocking)

Each gate must pass before tagging the named release.

| Gate | Release | Verify command / artifact | Blocks |
|------|---------|---------------------------|--------|
| State JSON schemas in registry | v2.14+ (per block) | `python scripts/validate-workflow.py --strict` | Tag if fail |
| ADR-V2-001..017 published | Pre-flight | File exists + linked from [decisions.md](../docs/decisions/decisions.md) | v2.14 start |
| Platform debt predicate | v2.14 | `python scripts/platform-debt-clear.py --goal <id>` | goal_verify pass |
| Stop taxonomy complete | v2.15 | `pytest tests/unit/test_stop_reasons.py` | Tag v2.15 |
| Bridge → required flip | v2.25 | `migrate-bridge-to-workflow.py` + all goals `required` or waived | Tag v2.25 |
| Generator-only routing | v2.26 | `pytest tests/unit/test_phase_skill_routing_forbidden.py` | Tag v2.26 |
| Bootstrap transistor manifest | v2.24 | `docs/platform/bootstrap-transistors.manifest.json` complete | SEC-18 §Q |
| Workflow coverage ≥ 90% | v2.28 | Dashboard `workflow_coverage_by_pack` | H3 on demo goal |
| L0 waiver bounds | v2.25+ | ADR-V2-015; `max_l0_waivers_per_goal=3` | goal_verify |
| Reference pack verify tightened | v2.28 | ADR-V2-013; no weak waiver rows | Final acceptance |

---

## Explicit non-goals (v2.28 scope)

Out of scope unless operator adds ADR at H1:

- Disaster recovery / state backup runbooks beyond preCompact snapshot (H6)
- Load/soak testing for SDK daemon
- Secrets rotation automation for `CURSOR_API_KEY`
- Supply-chain / dependency CVE scanning beyond G4.1 security-review triggers
- Multi-region / HA deployment of the harness itself

These may be added as v2.29+ program work via `release-queue.json` (J6).

---

## Definition of done: 100% spec ready

All must be true **before v2.14 implementation begins**:

- [x] This document (10) exists and README links it
- [x] [08](08-coverage-ledger.md) labeled plan-covered only
- [x] JSON Schema registry under `docs/platform/schemas/` (see 06 pre-flight)
- [x] ADR-V2-001..017 in [v2-evolution-policy-adrs.md](../docs/decisions/v2-evolution-policy-adrs.md)
- [x] Bridge sunset + H1 era split in [00](00-vision-and-scope.md) and [03](03-target-architecture.md)
- [x] No contradictory "open SEC-17" or "interim K" lines in 06/07
- [x] Final acceptance in 06 rewritten with measurable thresholds
- [x] Bootstrap manifest + skill migration in 05/06

When all boxes above are checked, update **Implementation status** and begin [06 pre-flight](06-MASTER-CHECKLIST.md).
