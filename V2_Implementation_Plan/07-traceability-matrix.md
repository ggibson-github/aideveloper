# 07 — Traceability Matrix

Proves that **every leaf** under `documents/` is covered by a release and a checklist section in [06-MASTER-CHECKLIST.md](06-MASTER-CHECKLIST.md). Grouped by leaf-ID prefix.

**Measured inventory (2026-06-28 final pass):**

| Bucket | Count | Notes |
|--------|------:|-------|
| Capability + meta leaves | **281** | `documents/plans/full-automation/*.md` excluding `*-index.md`, `INDEX.md`, `H3-SIGNOFF-BUNDLE.md` |
| Index / navigation files | **62** | `*-index.md` + `INDEX.md` |
| Root design docs | **3** | `documents/*.md` (vision, genius-conductor, spec-to-artifacts) |
| Hierarchy sign-off | **1** | `H3-SIGNOFF-BUNDLE.md` (certification artifact, not a runtime state block) |
| **Coverage ledger total** | **348** | [08-coverage-ledger.md](08-coverage-ledger.md) — all rows verified |
| INDEX.md leaf claim | **281** spec leaves + 1 certification bundle (`H3-SIGNOFF-BUNDLE.md`); **282** non-index `.md` in this directory |

Legend: **Release** = owning release in [04](04-release-roadmap.md) · **§06** = checklist section.

> **Authority note (read before trusting any single leaf):** Leaf **Behavior / step logic** sections may contain pass-3 template contamination. Controlling sources, in order: **vision §15** → **SEC-18** → **[03 §5 generator-first](03-target-architecture.md)** + **[ADR-V2-007](../docs/decisions/v2-evolution-policy-adrs.md)** → **APP-B** → leaf **Reader narrative** + **State/data fields** + **Repo artifacts** → **INDEX titles**. Leaf `Release:` headers were bulk-reconciled to this matrix (2026-06-28); if drift recurs, **07 + 04 + 06** win.

---

## Plane A — Pursuit & control (~27 leaves)

| Group | Leaves | Release | §06 |
|-------|--------|---------|-----|
| A1 Goal model | A1.1–A1.5 | v2.14 | v2.14 |
| A2 Pursuit loop | A2.1–A2.7 | v2.14 (A2.4); v2.15 (A2.1–3,5–7) | v2.14, v2.15 |
| A3 Autopilot modes | A3.1–A3.4 | v2.15 (A3.3 multi-goal — see note) | v2.15 |
| A4 Stop reasons | A4.1–A4.5 | v2.14 (A4.4 integrity); v2.15 (rest) | v2.14, v2.15 |
| A5 Continue semantics | A5.1–A5.3 | v2.15 | v2.15 |
| A6 Notification | A6.1–A6.3 | v2.23 | v2.23 |

> **A3.3 multi-goal / `company_autopilot`:** the leaf describes a multi-goal queue. Per open decision **SEC-17-6**, the plan ships single-pursuit-stack first and `company_autopilot` behind a flag in **v2.19+**. Resolve SEC-17-6 at H1 to confirm.

## Plane B — Cognition & routing (~27 leaves)

| Group | Leaves | Release | §06 |
|-------|--------|---------|-----|
| B1 S0–S4 | B1.1–B1.5 | exists; keep (route-tier) | pre-flight, v2.14 |
| B2 Roles | B2.1–B2.6 | exists; B2.6 platform worker v2.16; B2.5 reviewer v2.23 | v2.16, v2.23 |
| B3 Model policy | B3.1–B3.4 | exists; B3.4 v2.16 | v2.16 |
| B4 Dual-stack cognition | B4.1–B4.4 | v2.16–v2.17 | v2.16, v2.17 |
| B5 Company role switch | B5.1–B5.4 | v2.19 | v2.19 |
| B6 Workflow composer | B6.1–B6.4 | v2.26 | v2.26 |

## Plane C — Product execution (~25 leaves)

| Group | Leaves | Release | §06 |
|-------|--------|---------|-----|
| C1 Pipeline registry | C1.1–C1.4 | exists; C1.4 v2.19 | v2.19 |
| C2 Phase chain | C2.1–C2.5 | exists; C2.5 catalog refs v2.17 | v2.17 |
| C3 Task system | C3.1–C3.4 | C3.1 v2.16; C3.4 v2.14 | v2.14, v2.16 |
| C4 Program/parallel | C4.1–C4.4 | exists; pack use v2.19 | v2.19 |
| C5 Feature/app delivery | C5.1–C5.3 | pre-flight (e2e dir); v2.14 (DoD) | pre-flight, v2.14 |
| C6 Generator workflow exec | C6.1–C6.5 | v2.25 (C6.1–2); v2.26 (C6.3,5); v2.27 (C6.4) | v2.25–v2.27 |

## Plane D — Platform evolution (~34 leaves)

| Group | Leaves | Release | §06 |
|-------|--------|---------|-----|
| D1 Promotion ladder | D1.1–D1.6, **D1.7** | D1.1–6 v2.16; D1.7 v2.24 | v2.16, v2.24 |
| D2 Platform queue | D2.1.1–D2.1.4, D2.2, D2.3, **D2.1.5** | v2.16; D2.1.5 v2.24 | v2.16, v2.24 |
| D3 Scheduling | D3.1–D3.5 | v2.16 | v2.16 |
| D4 Work types | D4.1–D4.6, **D4.7** | v2.16; D4.7 v2.24 | v2.16, v2.24 |
| D5 Extend/fork/configure | D5.1–D5.3 | v2.16 | v2.16 |
| D6 Platform DoD | D6.1–D6.4, **D6.5** | v2.16; D6.5 v2.24 | v2.16, v2.24 |

## Plane E — Knowledge & composition (~29 leaves)

| Group | Leaves | Release | §06 |
|-------|--------|---------|-----|
| E1 Catalog | E1.1–E1.7 | v2.17 (E1.1–6 child indexes + E1.7 umbrella) | v2.17 |
| E2 Compose protocol | E2.1–E2.5 | v2.17 | v2.17 |
| E3 Facts & decisions | E3.1–E3.3 | v2.17 (mostly exists; E3.2 ADR template) | v2.17 |
| E4 Context layers | E4.1–E4.3 | exists; E4.2 hook inject confirmed v2.17 | v2.17 |
| E5 Staleness | E5.1–E5.3, **E5.4** | v2.18; E5.4 v2.25 | v2.18, v2.25 |
| E6 Transistor registry | E6.1–E6.5 | v2.24 | v2.24 |
| E7 Workflow composition | E7.1–E7.5 | v2.25 (E7.1–4); E7.5 v2.27 | v2.25, v2.27 |

## Plane F — Organization (~27 leaves)

| Group | Leaves | Release | §06 |
|-------|--------|---------|-----|
| F1 Pack schema | F1.1–F1.8, **F1.9** | v2.19; F1.9 v2.27 | v2.19, v2.27 |
| F2 Company instantiation | F2.1–F2.4 | v2.19 | v2.19 |
| F3 Game studio pack | F3.1–F3.4 | v2.20 (incl. SEC-18 §K domain transistors) | v2.20 |
| F4 Data platform pack | F4.1–F4.2 | v2.21 (incl. §K domain transistors) | v2.21 |
| F5 Cross-pack | F5.1–F5.3, **F5.4** | v2.22; F5.4 v2.27 | v2.22, v2.27 |
| F6 Role→agent mapping | F6.1–F6.4 | v2.19 (incl. forbidden_reads, permission matrix tests) | v2.19 |

## Plane G — Verification & quality (~27 leaves)

| Group | Leaves | Release | §06 |
|-------|--------|---------|-----|
| G1 Evidence gates | G1.1–G1.3 | exists; keep | v2.14 |
| G2 Goal-level verify | G2.1–G2.4, **G2.5** | v2.14 (incl. G2.4 batch regression); G2.5 v2.26 | v2.14, v2.26 |
| G3 Conformance | G3.1–G3.3 | v2.14 | v2.14 |
| G4 Review triggers | G4.1–G4.4 | v2.23 (G4.4 v2.18) | v2.18, v2.23 |
| G5 Mistake→control | G5.1–G5.7, **G5.8** | mapped in §06 "G5 mistake→control" table; G5.8 v2.26/28 | all + dedicated table |
| G6 Rollback/recovery | G6.1–G6.3, **G6.4** | v2.15 (G6.1 branch, G6.2 last_failure, G6.3 preCompact); G6.4 v2.26 | v2.15, v2.26 |

## Plane H — Persistence & state (~12 leaves)

| Group | Leaves | Release | §06 |
|-------|--------|---------|-----|
| H1 state blocks | H1.1–H1.6, **H1.7** | H1.2 v2.14, H1.3 v2.16, H1.4/5 v2.15, H1.6 v2.19, H1.7 v2.26 | v2.14–v2.26 |
| H2 progress.md | H2 | exists; keep (regression in pre-flight) | all |
| H3 Artifact graphs | H3 (+ H3-SIGNOFF-BUNDLE) | v2.18 | v2.18 |
| H4 evidence/ | H4 | exists; keep | v2.14, v2.26 (dual rollup paths) |
| H5 worker-runs | H5 | v2.15 (spawn audit contract) | v2.15 |
| H6 Snapshots | H6 | v2.15 (preCompact fields); v2.26 (`active_workflow` in snapshot) | v2.15, v2.26 |

## Plane I — Runtime & integration (~16 leaves)

| Group | Leaves | Release | §06 |
|-------|--------|---------|-----|
| I1 In-IDE | I1.1–I1.4 | exists; I1.4 full hook set v2.15 | v2.15 |
| I2 SDK daemon | I2.1–I2.2 | v2.15 | v2.15 |
| I2 SDK worker-server | **I2.3** | **v2.18** (lane leases, headless offload) | v2.18 |
| I3 Headless/CI | I3.1–I3.3 | v2.18 (incl. I3.3 lanes in CI) | v2.18 |
| I4 External tools | I4.1–I4.3, **I4.4** | v2.20; I4.4 executor boundary v2.26 | v2.20, v2.26 |
| I5 Notifications | I5.1–I5.2 | v2.23 | v2.23 |

## Plane J — Governance & operator (6 leaves)

| Group | Leaves | Release | §06 |
|-------|--------|---------|-----|
| J1 model-policy | J1 | exists; extend v2.15 | v2.15 |
| J2 automation-waivers | J2 | **v2.16** (template self-build waivers); **v2.23** (structured audit trail) | v2.16, v2.23 |
| J3 strict_hitl + self_gate_mode | J3 | v2.15 (`strict_hitl` in model-policy, not state.hitl alone) | v2.15 |
| J4 audit | J4 | **v2.15** (worker-runs.jsonl); **v2.23** (waiver/self-gate audit + retention) | v2.15, v2.23 |
| J5 export-contract | J5 | exists; **updated for active_workflow + redaction profiles** v2.26 | v2.26 |
| J6 release-queue | J6 | v2.16 (schema + unattended harness); kept current through **v2.28** | v2.16, v2.28 |

## Meta documents (~51 leaves)

| Group | Leaves | Coverage + §06 |
|-------|--------|----------------|
| INTRO-0 | 1 | [00-vision-and-scope.md](00-vision-and-scope.md) |
| INTRO-1.1–1.3 | 3 | [00](00-vision-and-scope.md); **INTRO-1.3 5-part completion criterion gated in §06 v2.14** |
| INTRO-2 | 1 | [03](03-target-architecture.md) §3; v2.24 |
| APP-A-build/design/discover/improve/organize/release/verify | 7 | [00](00-vision-and-scope.md) scope + **pack-authoring guide gated in §06 v2.19 (APP-A row)** |
| APP-B (state sketch) | 1 | [03](03-target-architecture.md) §1 |
| MASTER-A … MASTER-J | 10 | Plane summaries in [05](05-workstreams-by-plane.md); each plane's verify rolls into its release exit gate |
| SEC-13 pursuit flow | 1 | v2.15 pursuit loop + **cross-release platform-interleave acceptance (§06 v2.16)** |
| SEC-14 gap analysis | 1 | [02-gap-analysis.md](02-gap-analysis.md) |
| SEC-15-v2.14 … v2.28 | 15 | one per release in [04](04-release-roadmap.md) / §06 |
| SEC-17-index + decisions 1–10 | 11 | [00](00-vision-and-scope.md) + pre-flight / v2.15 state slots; SEC-17-7–10 encoded v2.24–v2.26 |
| SEC-18 transistor A–Z | 1 (`SEC-18-transistor-model-a-to-z-reference.md`) | [03](03-target-architecture.md) §3; **SEC-18 §Q acceptance gate in §06 v2.24/final** |

---

## Coverage assertion

- **Planes A–J:** every leaf group maps to ≥1 release and a §06 section. **Measured capability leaves:** A=27, B=27, C=25, D=34, E=29, F=27, G=27, H=12, I=16, J=6 → **230**; meta leaves (INTRO, APP, MASTER, SEC) → **51**; **281 total** capability+meta leaves.
- **Transistor threads** (B6.*, C6.*, D1.7, D2.1.5, D4.7, D6.5, E5.4, E6.*, E7.*, F1.9, F5.4, G2.5, G5.8, G6.4, H1.7, I4.4, INTRO-2, SEC-18) all map to **v2.24–v2.28**.
- **Meta docs** map to plan files (00–05) **and** carry dedicated §06 gates where they impose runtime behavior (INTRO-1.3, APP-A, SEC-13, SEC-18 §Q).
- **Coverage ledger:** [08-coverage-ledger.md](08-coverage-ledger.md) **348 / 348 verified** — every `documents/**/*.md` (excl. `html-site/`) cross-checked against 00–07.

---

## Final pass verification (2026-06-28)

**Method:** Python inventory of `documents/plans/full-automation/*.md`; authoritative release rules derived from [04](04-release-roadmap.md) + [06](06-MASTER-CHECKLIST.md); cross-check against [08](08-coverage-ledger.md) batch notes.

### Results

| Check | Result |
|-------|--------|
| Unmapped capability leaves | **0 / 281** |
| §06 sections for v2.14–v2.28 | **15 / 15** present |
| Transistor-thread leaves → v2.24+ | **All mapped** |
| Ledger ↔ matrix plane groups | **Aligned** (348 ledger files = 281 leaves + 62 indexes + 3 root + INDEX + H3-SIGNOFF) |

### Corrections applied this pass

| Leaf / group | Issue | Fix |
|--------------|-------|-----|
| **I2.3** | Source header `v2.15`; master assigns headless worker-server to **v2.18** | Matrix split I2.1–2 vs I2.3; §06 v2.18 |
| **H5** | Matrix said v2.16 | Corrected to **v2.15** (spawn audit with hooks) |
| **H6** | Snapshot missing v2.26 extension | Added **v2.26** (`active_workflow` in preCompact fields) |
| **J2** | Matrix said v2.23 only | Split **v2.16** (template self-build) + **v2.23** (audit) |
| **J4** | Matrix said v2.23 only | Split **v2.15** (worker-runs) + **v2.23** (waiver audit) |
| **SEC-17** | Split into 6+4 rows | Consolidated to **11 files** (index + 10 decisions) |
| **INDEX 284 vs 281** | Count drift | **Resolved:** INDEX.md updated to 281 spec leaves + certification bundle; SEC-18 links to leaf file |

### Source header drift (resolved 2026-06-28)

- Leaf `**Release:**` headers were bulk-corrected to match this matrix + [04](04-release-roadmap.md) + [06](06-MASTER-CHECKLIST.md).
- **Authoritative release** remains this matrix when headers and roadmap diverge in future edits.

### Release → primary leaf groups (quick reference)

| Release | Primary leaf groups |
|---------|---------------------|
| v2.14 | A1.*, A2.4, A4.4, G1–G3, G2.1–4, C3.4, C5.*, H1.2, H4, INTRO-1.3, APP-B, SEC-15-v2.14 |
| v2.15 | A2.* (exc. 2.4), A3.1–2, A3.4, A4.* (exc. 4.4), A5.*, B1.*, G6.1–3, H1.4–5, H5, H6, I1.*, I2.1–2, J1, J3, SEC-13 |
| v2.16 | D1.1–6, D2.* (exc. 2.1.5), D3.*, D4.1–6, D5.*, D6.1–4, B2.6, B3.4, B4.1–4, C3.1, H1.3, J2, J6 |
| v2.17 | E1–E4, B4.3, C2.5 |
| v2.18 | E5.1–3, G4.4, G5.5, I3.*, I2.3, H3-artifact-graphs |
| v2.19 | F1.1–8, F2.*, F6.*, B5.*, H1.6, A3.3, APP-A.*, SEC-17-5 |
| v2.20 | F3.*, I4.1–3 |
| v2.21 | F4.* |
| v2.22 | F5.1–3 |
| v2.23 | A6.*, I5.*, G4.1–3, J4 (audit), SEC-15-v2.23 |
| v2.24 | E6.*, D1.7, D2.1.5, D4.7, D6.5, INTRO-2, SEC-18, SEC-17-7/10 |
| v2.25 | C6.1–2, E7.1–4, E5.4, SEC-17-9 |
| v2.26 | B6.*, C6.3/5, H1.7, G2.5, G5.8, G6.4, I4.4, J5, SEC-17-8 |
| v2.27 | C6.4, E7.5, F1.9, F5.4 |
| v2.28 | SEC-15-v2.28, G5.8 metrics, E6.5 metrics view, J6 queue update |

> Maintenance rule: this matrix, [04](04-release-roadmap.md), [06](06-MASTER-CHECKLIST.md), and [08](08-coverage-ledger.md) must stay in sync. When leaves are added, update all four.
