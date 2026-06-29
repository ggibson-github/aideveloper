#!/usr/bin/env python3
"""Agent-authored Reader narratives for Plane E (knowledge & composition)."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

PLANE_E_NARRATIVES: dict[str, str] = {
    "E1.1": """\
The scripts catalog is a generated manifest under `scripts/` that lists every S0-capable entry point—route-tier, validate-workflow, verify-router, hierarchy automation—so conductors and compose queries discover deterministic behavior without grep-ing the tree.

Regeneration runs via S0 when scripts change; the manifest feeds [E2.2](E2.2-compose-query-catalog-list-components.md) list-components and the umbrella [E1.7](E1.7-catalog-platform-catalog-md-umbrella.md). Stale manifest rows trigger [E5.2](E5.2-staleness-extend-playbooks-scripts-pack-nodes.md) graph updates. See [Vision §7 — Branch E](../../full-automation-vision-and-hierarchy.md#7-branch-e-knowledge-composition-plane).""",
    "E1.2": """\
`docs/playbooks/INDEX.md` catalogs repo-scoped playbooks distilled after features complete—patterns for implement, verify, git-workflow, and pack-specific flows. Playbooks sit between skills (procedure) and facts (external truth) in the reuse ladder.

The INDEX is a first-class catalog node referenced by [E2.3](E2.3-compose-rank-script-playbook-skill-facts.md) ranking (script beats playbook beats skill) and by playbook-keeper after delivery. Compose-first ([B4.3](B4.3-compose-first-catalog-before-improvise.md)) requires playbook search before inventing new procedural guidance. Staleness marks playbook nodes when upstream design changes per [E5.1](E5.1-staleness-design-graph-staleness-json.md).""",
    "E1.3": """\
The skills index enumerates `.cursor/skills/` (and `.agents/skills/`) entries—continue, implement-feature, librarian, verifier—each with phase bindings and tool permissions. Catalog discovery prevents conductors from improvising phase behavior already encoded in skills.

Skills rank below scripts and playbooks in [E2.3](E2.3-compose-rank-script-playbook-skill-facts.md) compose ranking because they still invoke model turns; prefer S0 when a skill step is file-derived. Task cards reference skill ids in Components used ([E2.4](E2.4-compose-plan-task-card-components.md)). Pack authors extend the index via template-packs README ([E1.6](E1.6-catalog-template-packs-readme.md)).""",
    "E1.4": """\
`docs/facts/INDEX.md` is the entry point for external truth: URLs, credentials locations, API endpoints, team contacts, and captured snippets. Agents must read INDEX before guessing configuration—the facts-retrieval rule and [E3.1](E3.1-facts-docs-facts-external-truth.md) enforce this.

Facts rank lowest in compose preference ([E2.3](E2.3-compose-rank-script-playbook-skill-facts.md)) because they inform but do not execute. The remember skill ([E3.3](E3.3-remember-skill-index-no-fts-global.md)) appends to captured facts and updates INDEX—no global FTS memory. Librarian may include one fact path in allowed_reads ([E4.3](E4.3-context-allowed-reads-cap-max-5.md)).""",
    "E1.5": """\
The pipelines manifest under `docs/manifest/pipelines/` declares pipeline_id values—greenfield, iterative_feature, program—with phase order, default skills, and verify suites. Instantiation sets `pipeline_id` in state.json; route-tier selects the active pipeline for next_action.

This catalog binds Plane E discovery to Plane C execution ([C1.4](C1.4-pack-defined-pipelines-per-company-template.md)). Pack-defined pipelines differ per company template without forking conductor code. Changes mark dependent task cards stale via [E5.1](E5.1-staleness-design-graph-staleness-json.md) and may require reconcile-stale ([E5.3](E5.3-staleness-reconcile-stale-artifact-graph-skills.md)).""",
    "E1.6": """\
Each template-pack publishes a README cataloging pack fragments: roles, pipeline overrides, verify suites, and governance defaults. README files under `template-packs/*/` are discoverable catalog nodes for compose and pack instantiation.

Pack READMEs complement the generated platform umbrella ([E1.7](E1.7-catalog-platform-catalog-md-umbrella.md)) with consumer-specific bindings ([B5.2](B5.2-role-to-pipeline-id-skills-tool-permissions.md)). Promotion from L0 reasoning should target pack fragments listed here. Staleness extends to pack nodes when vision or parent pack schema changes ([E5.2](E5.2-staleness-extend-playbooks-scripts-pack-nodes.md)).""",
    "E1.7": """\
`docs/platform/CATALOG.md` is the generated umbrella index merging scripts, playbooks, skills, facts, pipelines, and pack README entries into one discovery surface. S0 regeneration keeps the umbrella current when any child catalog changes.

Operators and conductors start compose queries here before deep tree walks. The umbrella feeds [E2.2](E2.2-compose-query-catalog-list-components.md) and satisfies the single discovery surface goal of E1. Cross-links to child INDEX files must stay bidirectional. Platform maturity claims in Plane D depend on umbrella completeness and staleness graph coverage ([E5.1](E5.1-staleness-design-graph-staleness-json.md)).""",
    "E2.1": """\
Before any S1+ work, compose must resolve which capability the turn needs: routing, implement, verify, design artifact, platform promotion. Resolution names the capability id and target catalog slice—not a vague "figure it out" prompt.

Librarian and conductor share this step; output drives [E2.2](E2.2-compose-query-catalog-list-components.md) query and [E2.3](E2.3-compose-rank-script-playbook-skill-facts.md) ranking. Unresolved capability blocks spawn until catalog search completes. This implements mandatory compose-before-invent from [B4.3](B4.3-compose-first-catalog-before-improvise.md) at the Plane E protocol layer.""",
    "E2.2": """\
Catalog query runs through S0 `list-components.py` (or successor) against the umbrella and child INDEX manifests—returning candidate paths, maturity tier, and component type. Queries are deterministic; conductors use output rather than re-deriving hits in chat.

Input is the resolved capability from [E2.1](E2.1-compose-resolve-capability-needed.md); output feeds [E2.3](E2.3-compose-rank-script-playbook-skill-facts.md) ranking and task card Components ([E2.4](E2.4-compose-plan-task-card-components.md)). Empty results trigger [E2.5](E2.5-compose-miss-l0-enqueue-promotion.md) L0 proceed plus promotion enqueue—not silent invention.""",
    "E2.3": """\
Compose ranking orders catalog hits: script (S0) first, then playbook, then skill, then facts. The ladder maximizes determinism and reuse—run the script before invoking a skill that wraps the same behavior; read facts only to disambiguate, not to replace executable components.

Ranking applies after [E2.2](E2.2-compose-query-catalog-list-components.md) list-components returns hits. Ties break toward higher maturity and pack-authored fragments. Divergence from ranked choice requires [B4.4](B4.4-divergence-log-when-not-composing.md) log entry. Ranking aligns with capability_class S0–S4 in Plane B.""",
    "E2.4": """\
The compose plan lands on the task card Components section: explicit catalog refs (script path, playbook id, skill name) bound before implement spawn. Components used is auditable evidence that compose-first ran—not optional prose.

Conductor or task-breakdown writes Components after [E2.3](E2.3-compose-rank-script-playbook-skill-facts.md) ranking. Workers inherit listed refs in allowed_reads ([E4.3](E4.3-context-allowed-reads-cap-max-5.md)). Missing components when catalog had matches is a conformance failure; missing catalog match pairs with [E2.5](E2.5-compose-miss-l0-enqueue-promotion.md) promotion enqueue.""",
    "E2.5": """\
When compose finds no suitable catalog component, pursuit proceeds at L0 (ephemeral reasoning) for the immediate turn—but must enqueue a promotion_queue item so Plane D can distill the pattern into script, playbook, or pack fragment later.

This closes the reuse loop: product is not blocked, platform debt is recorded. Pair with [B4.4](B4.4-divergence-log-when-not-composing.md) divergence logging and [B4.2](B4.2-platform-promotion-queue-peek-drain.md) K-step drain. Repeated L0 for the same capability signals catalog gap—prioritize promotion over repeated improvisation.""",
    "E3.1": """\
`docs/facts/` holds external truth separate from design and journal narrative: environment URLs, schema snippets, operator-provided credentials pointers, team routing. Agents read facts; they do not invent URLs or API shapes when INDEX lists a topic file.

Facts integrate with compose at lowest rank ([E2.3](E2.3-compose-rank-script-playbook-skill-facts.md)) and with context retrieval ([E1.4](E1.4-catalog-facts-index.md)). Blocking questions about external config resolve by reading or extending facts—not by guessing. Stale facts when upstream systems change should trigger journal note and optional reconcile-stale ([E5.3](E5.3-staleness-reconcile-stale-artifact-graph-skills.md)).""",
    "E3.2": """\
`docs/decisions/` stores ADRs and recorded trade-offs when S3 ambiguity resolves: architecture choices, gate waivers with rationale, program manifest conflicts. Journal Q&A captures session decisions; ADRs persist cross-session authoritative rationale.

S3 turns in Plane B should end in journal entry or ADR ([B1.4](B1.4-s3-architecture-ambiguity.md)). ADRs link from design artifacts and task cards when implement depends on a settled choice. Unlike facts, decisions are repo-authored judgment—not external truth. Staleness may mark downstream design nodes when ADRs supersede prior assumptions ([E5.1](E5.1-staleness-design-graph-staleness-json.md)).""",
    "E3.3": """\
The remember skill captures operator snippets into `docs/facts/captured.md` and updates facts INDEX—explicit "remember this" workflow, not ambient chat memory. There is no global FTS or hidden vector store; all retained knowledge is file-backed and discoverable via [E1.4](E1.4-catalog-facts-index.md).

This keeps Plane E honest: if it is not in facts/decisions/catalog, agents should not treat it as project truth. Remember complements journal Resolved Q&A for durable non-decision snippets (Slack URLs, SQL fragments). Promotion candidates from repeated captures may enqueue via [E2.5](E2.5-compose-miss-l0-enqueue-promotion.md).""",
    "E4.1": """\
Always-on context layers inject project rules and `AGENTS.md` every session—the baseline conductor contract, evidence rules, approval gates, and pipeline semantics. Workers inherit applicable rules via spawn context; they do not re-read the full AGENTS monolith unless allowed.

This is layer zero of context retrieval—below hooks ([E4.2](E4.2-context-hooks-inject-continue-start.md)) and Librarian allowed_reads ([E4.3](E4.3-context-allowed-reads-cap-max-5.md)). Pack authors may extend always-on rules through template-pack fragments. Changes to AGENTS.md mark dependent playbooks and skills stale in [E5.2](E5.2-staleness-extend-playbooks-scripts-pack-nodes.md).""",
    "E4.2": """\
Cursor hooks inject journal summary, state.json snapshot, and Context files on continue/start—deterministic session resume without re-pasting progress. Hooks run before the conductor LLM turn; agents still must read journal per continue skill, but injection reduces cold-start drift.

Hook output complements always-on rules ([E4.1](E4.1-context-always-on-rules-agents-md.md)) and precedes Librarian briefing. Hook scripts live under `.cursor/hooks.json` and should stay S0-thin. Failed injection surfaces H2 when state.json corrupt—pair with [A4.4](A4.4-stop-integrity-validate-workflow-state-corrupt.md).""",
    "E4.3": """\
`allowed_reads` caps worker and Librarian context at five paths—hard bound on scope expansion. Librarian returns the cap; conductors pass it unchanged in spawn contracts; workers must not read outside the list except via declared tool output.

The cap forces compose and catalog search to prioritize ([E2.1](E2.1-compose-resolve-capability-needed.md)–[E2.4](E2.4-compose-plan-task-card-components.md)) instead of loading entire design trees. Conductor may read more than workers but should still prefer INDEX and task cards. Violations are scope-bleed failure class; orchestrate-subagents enforces in worker prompts.""",
    "E5.1": """\
`docs/manifest/staleness.json` is the design-graph staleness manifest: nodes for HLD, DD, diagrams, task cards with dependency edges and stale flags when upstream artifacts change. S0 update-staleness.py (or successor) maintains the graph file-derived.

Staleness blocks implement spawn against obsolete design until reconcile completes. Program artifact graphs ([C4.4](C4.4-artifact-graph-per-program-and-pack.md)) complement this manifest for multi-stream work. Vision § changes enqueue deepen items for affected hierarchy ids. See [E5-index](E5-index.md) for sibling extensions.""",
    "E5.2": """\
The staleness graph extends beyond design docs to playbooks, scripts catalog nodes, and template-pack fragments—any reusable component that downstream pursuit depends on. When a script or playbook changes, dependent task cards and compose hits mark stale.

Extension connects Plane E catalog maturity to traceability: promoted platform artifacts are first-class staleness nodes, not orphan files. Regeneration of [E1.1](E1.1-catalog-scripts-manifest-generated.md) and [E1.7](E1.7-catalog-platform-catalog-md-umbrella.md) should reconcile graph entries. Pack verify suites ([F1.8](../full-automation/MASTER-F-branch-f---organization-plane.md)) may assert graph completeness.""",
    "E5.3": """\
reconcile-stale and reconcile-artifact-graph skills plan reruns or operator approval when staleness.json or program artifact graphs flag stale nodes. Conductor invokes before implement spawn on affected paths; workers pause until reconciliation clears flags or H2 waiver records.

S0 scripts mark stale; skills decide rerun vs waive vs deepen hierarchy queue. Pair with [C4.4](C4.4-artifact-graph-per-program-and-pack.md) for program mode and [E5.1](E5.1-staleness-design-graph-staleness-json.md) for design graph source. Silent implement against stale design violates Plane E contract and undermines goal_verify evidence.""",
}


def apply_plane_e(out_dir: Path | None = None) -> int:
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from hierarchy_agent_prose import apply_narrative, find_paths_for_item_ids  # noqa: E402

    base = out_dir or ROOT / "documents/plans/full-automation"
    applied = 0
    paths = find_paths_for_item_ids(base, set(PLANE_E_NARRATIVES))
    for iid, narrative in PLANE_E_NARRATIVES.items():
        p = paths.get(iid)
        if not p:
            print(f"Missing leaf for {iid}", file=sys.stderr)
            continue
        new_text, issues = apply_narrative(p, narrative, version="plane-e")
        p.write_text(new_text, encoding="utf-8")
        applied += 1
        if issues:
            print(f"{iid}: {', '.join(issues)}")
    print(f"Applied Plane E agent prose to {applied} leaves")
    return 0


if __name__ == "__main__":
    raise SystemExit(apply_plane_e())
