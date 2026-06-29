# 09 — Architectural Supplements

Cross-cutting specifications added after architect review (2026-06-28). **Authority:** these supplements override ambiguous leaf prose when cited by checklist items.

| Topic | Primary spec | ADR |
|-------|--------------|-----|
| SEC-17 policy defaults | [00-vision-and-scope.md](00-vision-and-scope.md) | [docs/decisions/v2-evolution-policy-adrs.md](../docs/decisions/v2-evolution-policy-adrs.md) ADR-001..017 |
| Generator-first / workflow DAG maximized | [03-target-architecture.md](03-target-architecture.md) §5 | ADR-V2-007 |
| Program block + lanes | [03-target-architecture.md](03-target-architecture.md) §1.1 | ADR-V2-009 |
| Platform debt predicate | [03-target-architecture.md](03-target-architecture.md) §6.1 | ADR-V2-008 |
| Soft transistor executor | [03-target-architecture.md](03-target-architecture.md) §3.2.1 | ADR-V2-010 |
| Budget precedence | ADR-V2-004 | [06](06-MASTER-CHECKLIST.md) v2.14–15 |
| Observability | [03-target-architecture.md](03-target-architecture.md) §9 | ADR-V2-011 |
| L0 waiver bounds | ADR-V2-015 | [06](06-MASTER-CHECKLIST.md) v2.25/v2.28 |
| Security taxonomy | ADR-V2-016 | [06](06-MASTER-CHECKLIST.md) v2.23 |
| Parent goal tree | ADR-V2-017 | [06](06-MASTER-CHECKLIST.md) v2.14/v2.19 |
| JSON Schema registry | [docs/platform/schemas/README.md](../docs/platform/schemas/README.md) | Phase B |
| Bootstrap transistor manifest | [docs/platform/bootstrap-transistors.manifest.json](../docs/platform/bootstrap-transistors.manifest.json) | Phase E |
| CI test matrix | [06](06-MASTER-CHECKLIST.md) Pre-flight | — |
| Capability debt window (packs pre-transistor) | [04-release-roadmap.md](04-release-roadmap.md) v2.20–v2.23 | — |

When implementing, read **03 §5** (compose stack) and **ADR-V2-007** before any v2.17+ composition work.

## CI test matrix (pre-flight)

| Release | Required suites |
|---------|-----------------|
| v2.14+ | unit + integration (`goal`, `platform-debt-clear`, budget caps) |
| v2.15+ | + goal_autopilot integration, stop_reasons, writer authority |
| v2.16+ | + platform interleave (SEC-13) |
| v2.18+ | + headless-verify CI, staleness platform, lane lease |
| v2.19+ | + pack schema, active_role, preemption |
| v2.20+ | + **contract** (`tests/contract/` fixtures) + e2e (mock externals at boundary) |
| v2.25+ | + `validate-workflow-dag.py` |
| v2.26+ | + generator-only, soft transistor, fuzzy-chain, `test_phase_skill_routing_forbidden.py` |

Pre-flight scaffold: [tests/contract/README.md](../tests/contract/README.md).

Tag `v2.N` only when the row for **N** and all prior rows are green.
