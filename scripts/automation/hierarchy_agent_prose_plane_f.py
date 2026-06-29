#!/usr/bin/env python3
"""Agent-authored Reader narratives for Plane F (organization / template-packs)."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

PLANE_F_NARRATIVES: dict[str, str] = {
    "F1.1": """\
`company.yaml` is the root schema for every template-pack: company name, industry, department list, role references, default pipeline, and pack metadata. Instantiation copies or binds this file into pursuit state via program-scoper—`state.company.pack_id` and initial `active_role` derive from here.

The schema must compose with sibling pack artifacts ([F1.2](F1.2-pack-roles---yaml.md) roles, [F1.3](F1.3-pack-pipelines---yaml.md) pipelines, [F1.8](F1.8-pack-verify-goal-verify-suites.md) verify suites) without ad hoc fields in consumer repos. Pack authors validate against conformance scripts before publish; consumer goals reference pack version, not forked company.yaml inline. See [Vision §8 — Branch F](../../full-automation-vision-and-hierarchy.md#8-branch-f-organization-plane-template-packs-ceiling).""",
    "F1.2": """\
`roles/*.yaml` declares each organizational role: `role_id`, bound `pipeline_id`, tool permissions, MCP allowlists, KPI hints, and handoff targets. Roles are the unit of agent persona swap—workers inherit role context from spawn contracts while the conductor identity stays fixed ([F6.1](F6.1-role-mapping-conductor-context-switch-active-role.md)).

Mis-bound pipeline_id routes implement into wrong phases ([B5.2](B5.2-role-to-pipeline-id-skills-tool-permissions.md)). Per-role `allowed_reads` and evidence rules extend in [F6.2](F6.2-role-allowed-reads-scoped-playbooks-lane-tasks.md) and [F6.4](F6.4-role-evidence-requirements-per-output-type.md). company.yaml lists role ids; this directory holds authoritative bindings.""",
    "F1.3": """\
`pipelines/*.yaml` encodes phase order, human gates, pack_keywords, and skill bindings for each pipeline_id a pack offers—greenfield, iterative_feature, program variants per company template. program-scoper and route-tier read these files to set `next_action` without improvising phase graphs.

Pipelines connect pack organization to Plane C execution ([C1.4](C1.4-pack-defined-pipelines-per-company-template.md)). Integration manifest and lane work orders reference pipeline phases for parallel spawn eligibility ([F2.2](F2.2-company-spawn-workstream-department-role-lane.md)). Schema changes mark downstream task cards stale via reconcile-stale.""",
    "F1.4": """\
`manifest.md` in the pack defines integration contracts—internal handoffs between roles and external boundaries (APIs, repos, third-party tools). This is the pack-authored precursor to `program/integration/manifest.md` that program-scoper materializes at instantiation ([F2.4](F2.4-company-conductor-handoffs-manifest-graph.md)).

Human gate clears parallel lanes only after manifest approval ([B5.3](B5.3-handoff-manifest-artifact-graph.md)). Contracts must name artifact types, verify commands, and blocking dependencies—not vague "coordinate with team." Cross-pack imports ([F5.1](F5.1-cross-pack-imports-micro-packs.md)) extend manifest rows when micro-packs add roles.""",
    "F1.5": """\
`artifact-graph.json` registers cross-role dependencies inside the pack: which design nodes, task templates, and verify suites must exist before downstream roles proceed. reconcile-artifact-graph marks stale nodes when upstream pack fragments change.

The graph pairs with integration manifest ([F1.4](F1.4-pack-manifest-md-integration-contracts.md)) for program mode—manifest is human-readable contract, graph is machine reconciliation input. Missing graph edges cause silent parallel spawn before prerequisites exist. Pack authors wire nodes at publish; conductors run S0 reconcile before orchestrate-program.""",
    "F1.6": """\
Pack `playbooks/` hold role-specific procedures distilled for that industry template—game QA asset checks, data platform deploy runbooks, onboarding flows. They complement repo `docs/playbooks/` after instantiation copies or references pack fragments into the consumer catalog ([E1.2](E1.2-catalog-playbooks-index.md)).

Compose-first ([B4.3](B4.3-compose-first-catalog-before-improvise.md)) searches pack playbooks via role-scoped allowed_reads ([F6.2](F6.2-role-allowed-reads-scoped-playbooks-lane-tasks.md)). Playbook-keeper promotes repeated patterns from product pursuit back into pack fragments via Plane D promotion queue—not ad hoc edits in consumer repos ([F5.3](F5.3-no-repo-outside-template-packs-ceiling.md)).""",
    "F1.7": """\
`template tasks/` seeds task cards per role—pre-written Components, Test commands, evidence types, and promotion_note stubs so instantiation does not start from empty TODOS. program-scoper or task-breakdown copies seeds into `docs/features/` or program lanes with pack_id provenance.

Seed cards bind pack verify suites ([F1.8](F1.8-pack-verify-goal-verify-suites.md)) and role evidence rules ([F6.4](F6.4-role-evidence-requirements-per-output-type.md)) at first implement turn. Seeds are templates, not completed work—evidence gates still apply. Platform promotion ([D6.3](D6.3-platform-done-task-card-references.md)) requires task cards reference promoted artifacts after they have been promoted from the improvement queue into lasting catalog entries.""",
    "F1.8": """\
Pack `verify/` defines goal_verify suites per deliverable type—aggregated pytest profiles, validate-workflow hooks, checksum tools, and meta-tests that prove pack intent beyond per-task evidence. When implement batch completes, conductor resolves `goal.verify_command` from state or active pack suite before H3 ([A2.4](A2.4-goal-scope-complete-run-goal-verify.md)).

Fail closed: missing task evidence blocks goal_verify; goal_verify failure blocks H3 auto-clear ([A2.5](A2.5-goal-verify-pass-transition-h3-pending.md)). Domain packs specialize suites—game studio asset/engine checks ([F3.4](F3.4-game-studio-goal-verify-asset-engine-tests-perf.md))—without weakening the generic suite contract here.""",
    "F2.1": """\
Company instantiation begins when program-scoper reads the mega-spec, scores pack_keywords against available template-packs, and selects `pack_id`. Selection sets `state.company.pack_id`, default `active_role`, and initial program structure—workstreams, blocking questions, milestone gates.

Wrong pack selection is high-risk: roles, pipelines, and verify suites all derive from the choice. Scoper records rationale in journal Q&A; H1 plan approval covers pack choice when policy requires. Pack ceiling ([F5.3](F5.3-no-repo-outside-template-packs-ceiling.md)) means organization changes flow through pack updates or imports ([F5.1](F5.1-cross-pack-imports-micro-packs.md)), not silent consumer-repo forks.""",
    "F2.2": """\
After pack bind, program-scoper spawns program workstreams mapped to departments or role lanes—each lane gets lane.json leases, work orders, and spawn_policy compatible with integration manifest. Department boundaries align with pack roles ([F1.2](F1.2-pack-roles---yaml.md)); parallel lanes require manifest gate clearance ([F1.4](F1.4-pack-manifest-md-integration-contracts.md)).

orchestrate-program spawns workers only for ready lanes with valid leases ([C4.1](C4.1-workstreams-lane-json-leases.md)). Spawn without manifest approval violates program pipeline order. Lane spawn is S0 where lane scripts exist; otherwise conductor invokes program-scoper skill with pack context.""",
    "F2.3": """\
Company autopilot rotates `state.company.active_role` based on ready work in lane queues—not fixed round-robin. When a role lane has unblocked tasks and leases available, conductor switches active_role, updates spawn contracts, and schedules pursuit for that persona ([A3.3](A3.3-company-autopilot-multi-goal-role-workstreams.md)).

Rotation must release held lane leases before role switch (complete-work-order). Role switch updates tool permissions ([F6.3](F6.3-role-tool-permissions-mcp-cli-allowlist.md)) and allowed_reads ([F6.2](F6.2-role-allowed-reads-scoped-playbooks-lane-tasks.md)) without merging permissions across roles. Conductor identity persists across switches ([F6.1](F6.1-role-mapping-conductor-context-switch-active-role.md)).""",
    "F2.4": """\
The conductor orchestrates cross-role handoffs using instantiated manifest.md plus artifact-graph.json—checking prerequisite nodes, updating handoff manifest sections, and spawning the next role lane when contracts satisfy. This implements pack integration contracts ([F1.4](F1.4-pack-manifest-md-integration-contracts.md)) at runtime.

Handoffs are conductor-owned S3 merges when ambiguity exists; mechanical prerequisite checks are S0 via reconcile-artifact-graph. Failed handoff surfaces structured H2 with missing artifact id and suggested owner role. Pair with [B5.3](B5.3-handoff-manifest-artifact-graph.md) and [B5.4](B5.4-conductor-stays-workers-swap-role-context.md) for worker vs parent separation.""",
    "F3.1": """\
The game studio example pack defines roles: designer, technical artist, animator, programmer, QA, build engineer, release manager—each with pipeline slice, tools, and KPIs appropriate to concept-to-ship asset work. Roles map to [F1.2](F1.2-pack-roles---yaml.md) schema and demonstrate multi-disciplinary company pursuit under one pack_id.

This pack is reference, not mandatory—all studios need not use every role; program-scoper may defer lanes until milestone needs them. External tool bindings ([F3.3](F3.3-game-studio-external-tools-blender-ue-git-ci.md)) and pipelines ([F3.2](F3.2-game-studio-pipelines-concept-to-build.md)) specialize these roles. Cross-pack HR onboarding may import via [F5.1](F5.1-cross-pack-imports-micro-packs.md).""",
    "F3.2": """\
Game studio pipelines walk concept → mesh → rig → animation → engine import → QA → build—each phase bound to roles and gates in pipelines/*.yaml. Phase order prevents animator work before rig exists and blocks build before QA evidence passes.

Pipeline phases reference pack playbooks ([F1.6](F1.6-pack-playbooks-role-specific.md)) and seed task cards ([F1.7](F1.7-pack-template-tasks-seed-cards.md)) for implement turns. Integration manifest declares which phases may parallelize (e.g. multiple asset lanes). goal_verify at ship uses [F3.4](F3.4-game-studio-goal-verify-asset-engine-tests-perf.md) suite atop generic [F1.8](F1.8-pack-verify-goal-verify-suites.md).""",
    "F3.3": """\
Game studio packs declare external tools: Blender, Unreal Engine, Perforce or Git, CI build farms—MCP servers, CLI allowlists, and tool-operator task card patterns per role ([F6.3](F6.3-role-tool-permissions-mcp-cli-allowlist.md)). Tool-operator and verifier workers run bounded exports and engine tests; they do not edit pursuit state.

Missing tool install or credentials is H2—not skip. Facts INDEX holds download URLs and credential locations ([E1.4](E1.4-catalog-facts-index.md)). Evidence for tool runs follows [F6.4](F6.4-role-evidence-requirements-per-output-type.md) output types (render checksum, export log, CI artifact path). Compose-first searches pack playbooks before improvising tool commands.""",
    "F3.4": """\
Game studio goal_verify proves assets load in engine, automated tests pass, and performance budgets hold—beyond per-task pytest evidence. The suite aggregates tool-operator logs, engine test output, and perf counters into one `goal.verify_command` resolved at scope complete ([A2.4](A2.4-goal-scope-complete-run-goal-verify.md)).

Weak goal_verify (smoke import only) is an accepted risk documented in adversarial review—pack authors tighten suites over releases. Failure blocks H3 and packages H2 with evidence paths attached. Extends generic pack verify ([F1.8](F1.8-pack-verify-goal-verify-suites.md)) without replacing task-level verify-router discipline.""",
    "F4.1": """\
The data platform example pack defines roles: analyst, data engineer, DBA, SRE, governance reviewer—each with pipeline bindings for ingest-to-production workflows. Roles demonstrate regulated data work: schema approval, deploy windows, and audit evidence distinct from game asset roles ([F3.1](F3.1-game-studio-roles-designer-ta-animator-programmer-qa-build-r.md)).

Governance role may hold H2-equivalent gates inside pack policy (strict_hitl). Tool permissions restrict production deploy commands to SRE role ([F6.3](F6.3-role-tool-permissions-mcp-cli-allowlist.md)). Pipelines ([F4.2](F4.2-data-platform-pipelines-ingest-model-deploy-monitor.md)) sequence work across these roles. Shared micro-packs ([F5.1](F5.1-cross-pack-imports-micro-packs.md)) may add generic security review fragments.""",
    "F4.2": """\
Data platform pipelines follow ingest → model/transform → deploy → monitor/alert—phases mapped to engineer, DBA, and SRE roles with governance checkpoints. Deploy phases require evidence bundles and may block outside maintenance windows per pack policy.

Manifest and artifact graph ([F1.4](F1.4-pack-manifest-md-integration-contracts.md), [F1.5](F1.5-pack-artifact-graph-json-cross-role.md)) wire schema approval before deploy lanes start. Monitor phase feeds goal_verify metrics checks in [F1.8](F1.8-pack-verify-goal-verify-suites.md). S0 scripts should validate pipeline YAML against pack schema before instantiation saves bad graphs to state.""",
    "F5.1": """\
Cross-pack imports let a company pack compose micro-packs—studio pack imports generic HR/onboarding, data pack imports security baseline—via declared import list in company.yaml or manifest. Imports merge roles, playbooks, and verify fragments without copying entire foreign packs into consumer repos.

Import resolution is S0 at instantiation; broken import path is H2 with missing pack id. Imports must respect ceiling ([F5.3](F5.3-no-repo-outside-template-packs-ceiling.md))—only template-packs namespace, not ad hoc paths. Provenance links support SEC-14 gap analysis and [D5.3](D5.3-fork-new-catalog-entry-provenance.md) when imported fragment diverges.""",
    "F5.2": """\
`template-packs/_shared/` is the generic library: onboarding micro-packs, security baselines, common verify hooks, and reusable role fragments consumed by industry packs via [F5.1](F5.1-cross-pack-imports-micro-packs.md). Shared content versions independently from game studio or data platform packs.

Authors promote mature fragments from product repos into _shared via Plane D pack fragment export ([D4.6](D4.6-platform-work-pack-fragment-export.md)). INDEX and catalog regeneration ([E1.7](E1.7-catalog-platform-catalog-md-umbrella.md)) must list _shared entries for compose-first discovery. Editing _shared affects all importers—extend with backwards compatibility ([D5.2](D5.2-extend-backwards-compatible-staleness-bump.md)) or fork ([D5.3](D5.3-fork-new-catalog-entry-provenance.md)).""",
    "F5.3": """\
The template-packs ceiling rule: no organizational authority lives outside `template-packs/` for pack-defined roles, pipelines, governance, and verify suites. Consumer repos instantiate packs; they do not silently fork company.yaml, roles, or pipelines into undocumented paths—this capability enforces auditability.

Urgent hotfixes flow through pack version bump, import, or operator policy override recorded in journal—not permanent shadow copies. Platform promotion targets pack fragments ([D4.6](D4.6-platform-work-pack-fragment-export.md)); consumer-only patterns fail maturity claims. Vision §8 treats template-packs as whole-company organizational ceiling.""",
    "F6.1": """\
Role mapping keeps one genius-tier conductor while `state.company.active_role` switches context—pipeline_id, spawn policy, and HITL strictness follow the active role from pack bindings ([B5.1](B5.1-active-role-from-template-pack.md)). Workers swap personas per spawn; conductor merges summaries and dual-writes journal/state.

Context switch is not a new chat session—state.json carries active_role across turns. Switching mid-lease requires lane release ([F2.3](F2.3-company-active-role-rotates-ready-work.md)). Mis-mapping (platform permissions on product role) is conformance failure. Same conductor identity enables centralized S4 H2 packaging ([B5.4](B5.4-conductor-stays-workers-swap-role-context.md)).""",
    "F6.2": """\
Per-role `allowed_reads` scopes workers to role playbooks, lane task cards, facts entries, and design slices declared in pack YAML—not the full vision monolith or unrelated department lanes. Librarian returns paths within this cap (max five) before implement spawn ([B2.2](B2.2-librarian-allowed-reads-catalog-composition.md)).

Scope bleed (QA worker reading finance playbooks) violates pack intent and risks cross-department edits. allowed_reads updates on active_role rotation ([F6.1](F6.1-role-mapping-conductor-context-switch-active-role.md)). Lane.json work orders may further narrow reads for parallel slots. Forbidden paths are explicit deny list alongside allowed_reads.""",
    "F6.3": """\
Tool permissions per role encode MCP server allowlists, CLI patterns, and write scopes—programmer may run build CLI; designer may run Blender MCP; governance may read-only audit tools. Bindings live in roles/*.yaml and mirror operator policy overrides ([B5.2](B5.2-role-to-pipeline-id-skills-tool-permissions.md)).

Violations block spawn or fail verifier with permission error—never silent downgrade to broader tools. External game tools ([F3.3](F3.3-game-studio-external-tools-blender-ue-git-ci.md)) and data deploy CLIs declare here. Pack authors test permission matrix with conformance scripts before publish.""",
    "F6.4": """\
Evidence requirements per role output type define what verify must prove for each deliverable—code diff + pytest for programmer tasks, export checksum + render for TA tasks, schema migration log for DBA tasks. Requirements extend generic evidence_required in state with pack-specific output_type rows.

Task cards reference output_type; verify-router and tool-operator write matching evidence paths ([G-plane task evidence](C3.3-evidence-per-task.md)). goal_verify ([F1.8](F1.8-pack-verify-goal-verify-suites.md)) aggregates role evidence at scope complete. Missing output_type evidence blocks task completion even when generic last_verify passed—fail closed per role contract.""",
}


def apply_plane_f(out_dir: Path | None = None) -> int:
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from hierarchy_agent_prose import apply_narrative  # noqa: E402
    from hierarchy_completeness import item_id_from_path  # noqa: E402

    base = out_dir or ROOT / "documents/plans/full-automation"
    applied = 0
    for p in sorted(base.glob("*.md")):
        text = p.read_text(encoding="utf-8")
        iid = item_id_from_path(p, text)
        if iid not in PLANE_F_NARRATIVES:
            continue
        new_text, issues = apply_narrative(p, PLANE_F_NARRATIVES[iid], version="plane-f")
        p.write_text(new_text, encoding="utf-8")
        applied += 1
        if issues:
            print(f"{iid}: {', '.join(issues)}")
    print(f"Applied Plane F agent prose to {applied} leaves")
    return 0


if __name__ == "__main__":
    raise SystemExit(apply_plane_f())
