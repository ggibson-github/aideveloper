#!/usr/bin/env python3
"""Transistor / generator-workflow hierarchy leaf definitions (v2.24+)."""

from __future__ import annotations

# New expand nodes under existing branches
TRANSISTOR_EXPAND_NODES: list[dict] = [
    {"id": "B6", "title": "Workflow composer routing", "source_section": "§19", "parent": "B", "branch": "B"},
    {"id": "C6", "title": "Generator workflow execution", "source_section": "§19", "parent": "C", "branch": "C"},
    {"id": "E6", "title": "Transistor registry", "source_section": "§19", "parent": "E", "branch": "E"},
    {"id": "E7", "title": "Generator workflow composition", "source_section": "§19", "parent": "E", "branch": "E"},
]

TRANSISTOR_LEAVES: dict[str, dict] = {
    "INTRO-2": {
        "title": "Transistor building blocks north star",
        "parent": "INTRO",
        "release": "v2.24",
        "vision_section": "§19",
        "narrative": (
            "The fourth structural shift after pursuit loops, dual-stack platform evolution, and "
            "template-pack companies: **generator workflows** built from **transistors**—registered "
            "composable blocks with typed inputs, outputs, executors, and per-block verify—instead of "
            "long prose-only skill chains.\n\n"
            "Agents compose before they invent: search the transistor registry, stitch a DAG, execute "
            "one node per turn with evidence, promote misses to the platform queue. Read "
            "[SEC-18](SEC-18-transistor-model-a-to-z.md) for the complete A–Z reference."
        ),
        "steps": [
            "After H1 approves a goal, pursuit must produce or bind a generator workflow DAG before direct implement improvisation when goal type is app, feature, milestone, or pack-defined deliverable.",
            "Each workflow node references a catalog transistor or records an L0 miss plus promotion_queue enqueue per E7.4.",
            "Product turns execute the current workflow node; platform turns mint new transistors from repeated L0 patterns per D4.7.",
            "Goal completion requires workflow completion rollup (C6.5) plus goal_verify—not merely task cards closed in chat order.",
            "Skills and playbooks remain orchestration documentation; transistors are the executable contract the conductor and S0 tools enforce.",
        ],
    },
    "SEC-18": {
        "title": "Transistor model A to Z reference",
        "parent": "SEC",
        "release": "v2.24",
        "vision_section": "§19",
        "narrative": (
            "Authoritative end-to-end model for transistors and generator workflows. Defines terminology, "
            "schema, promotion ladder extension (L6), composition protocol, execution semantics, verification, "
            "persistence, pack integration, release sequencing v2.24–v2.28, and resolved design decisions. "
            "All E6/E7/B6/C6 leaf specs must align with this document."
        ),
        "steps": [
            "Terminology: transistor (atomic block), generator workflow (DAG of transistor instances), composer (S3 skill), executor (script|tool|soft|gate).",
            "Registry lives under docs/platform/transistors/ with generated TRANSISTORS.md; list-transistors.py queries by capability and I/O compatibility.",
            "Ranking extends E2.3: hard_transistor > script > soft_transistor > playbook > skill > facts.",
            "H1 artifact includes approved workflow JSON; state.pursuit.active_workflow tracks current node and checkpoints.",
            "Platform promotion L6 closes the loop: repeated L0 → transistor manifest + verify + staleness node per D6.5.",
        ],
    },
    "B6.1": {
        "title": "workflow-composer skill S3 graph planning",
        "parent": "B6",
        "release": "v2.26",
        "narrative": (
            "The workflow-composer skill is S3 architecture work: given goal success_criteria and "
            "capability_needed, it searches the transistor registry and pack workflow templates, "
            "proposes a generator DAG, and lists promotion misses—without spawning implement workers."
        ),
        "steps": [
            "Conductor invokes workflow-composer at task-breakdown or pre-implement when C6.1 requires a bound workflow.",
            "Composer allowed_reads: SEC-18 summary, E6 catalog slice, pack templates (F1.9), goal success_criteria—max five paths per E4.3.",
            "Output: docs/workflows/<goal-id>.json DAG plus promotion_queue items for missing transistors.",
            "Composer does not edit src/ or run tools; S0 validate-workflow-dag.py checks wiring before H1 self-gate or operator review.",
            "If composer cannot resolve deliverable type, pursuit stops at H2 with structured capability gap—not silent L0 implement.",
        ],
    },
    "B6.2": {
        "title": "conductor approves generator workflow at H1",
        "parent": "B6",
        "release": "v2.26",
        "narrative": (
            "The genius-tier conductor merges composer output into the H1 plan artifact: human-readable "
            "workflow summary plus machine-readable DAG path. Approval binds pursuit to that graph unless "
            "staleness or divergence triggers re-compose."
        ),
        "steps": [
            "H1 plan lists workflow_id, node count, critical path transistors, and known promotion debt.",
            "Dual-write binds state.pursuit.active_workflow.workflow_id and docs/workflows path in journal.",
            "Self-gate default: validate-workflow-dag.py pass suffices; strict_hitl may require operator sign-off on DAG.",
            "Re-compose only via reconcile-stale, goal scope change, or logged divergence (B4.4)—not mid-turn whim.",
            "Unapproved or missing workflow when C6.1 applies blocks implement next_action at preflight.",
        ],
    },
    "B6.3": {
        "title": "one workflow node per product turn default",
        "parent": "B6",
        "release": "v2.26",
        "narrative": (
            "Default product turn executes exactly one workflow node—mirroring A2.2 one pipeline step. "
            "This prevents fuzzy multi-hop improvisation and keeps evidence per node auditable."
        ),
        "steps": [
            "Preflight reads active_workflow.current_node_id; route-tier maps node to transistor executor class.",
            "Hard transistors run via S0 or tool-operator; soft transistors spawn bounded S1 workers with output schema validation.",
            "After node verify passes, advance current_node_id; dual-write completed_nodes[] and evidence paths.",
            "Gate transistors may branch without consuming an extra product turn when S0 branch resolver handles pass/fail edges.",
            "Batching multiple nodes per turn requires explicit pack policy or operator waiver in journal—never default.",
        ],
    },
    "B6.4": {
        "title": "gate transistor pass fail edge routing",
        "parent": "B6",
        "release": "v2.26",
        "narrative": (
            "Gate transistors are control-flow blocks: they consume verify results or S0 predicate output "
            "and select the next edge in the workflow DAG—pass, fail, retry, or H2—without LLM interpretation."
        ),
        "steps": [
            "Gate executor kinds: verify_result, file_exists, schema_match, budget_remaining, staleness_clear.",
            "validate-workflow-dag.py requires explicit edges for every gate outcome; no implicit fall-through.",
            "Fail edges default to structured H2 when retry_count exhausted; retry edges increment node-local counter in state.",
            "Gate transistors rank as hard when fully S0; soft gates forbidden—control flow must be deterministic.",
            "Miswired gate (missing edge) fails conformance at compose time, not at runtime surprise.",
        ],
    },
    "C6.1": {
        "title": "phase workflow-compose mandatory before implement",
        "parent": "C6",
        "release": "v2.25",
        "narrative": (
            "workflow-compose is a phase between task-breakdown and scaffold/implement for deliverable goals. "
            "It ensures the agent designs the generator before generating—matching the transistor north star."
        ),
        "steps": [
            "When next_action would enter implement-feature and no active_workflow is bound, insert workflow-compose phase.",
            "Phase invokes workflow-composer (B6.1) and writes docs/workflows/<goal-id>.json.",
            "Exceptions: pure L0 spike goals explicitly marked in H1 with expiry; platform-only goals use APP-A-improve taxonomy.",
            "Phase verify: validate-workflow-dag.py exit 0 and all referenced transistors exist in registry or promotion_queue.",
            "Skip without journal record triggers B4.4 divergence and G5.8 fuzzy-chain control.",
        ],
    },
    "C6.2": {
        "title": "workflow DAG artifact schema JSON",
        "parent": "C6",
        "release": "v2.25",
        "narrative": (
            "Generator workflows are versioned JSON DAGs: nodes (transistor ref + params), edges (including gate labels), "
            "metadata (goal_id, pack_id, composer model audit). Schema is validated by S0—not prose in task cards alone."
        ),
        "steps": [
            "Schema path: docs/platform/schemas/workflow-dag.v1.json; workflows stored under docs/workflows/.",
            "Each node: { id, transistor_id, params, retry_max, evidence_path_template }.",
            "Edges: { from, to, on: pass|fail|retry|default } for gate routing per B6.4.",
            "Pack templates live under template-packs/*/workflows/*.json and copy by reference at instantiate.",
            "Workflow version bumps trigger E5.4 staleness on dependent task cards and active_workflow.",
        ],
    },
    "C6.3": {
        "title": "task card binds workflow_node_id",
        "parent": "C6",
        "release": "v2.26",
        "narrative": (
            "Implement task cards gain workflow_node_id and transistor_id fields linking pursuit to the DAG. "
            "Components used lists the transistor manifest path; promotion_note captures subgraph extraction candidates."
        ),
        "steps": [
            "new-task-card.py emits workflow_node_id when active_workflow is set; one card maps to one node default.",
            "Task verify command comes from transistor manifest verify block unless overridden by pack.",
            "Workers must not execute transistors outside the bound node without conductor graph update.",
            "Missing workflow_node_id when active_workflow exists fails C3.1 conformance.",
            "Completed node clears card; conductor advances active_workflow.current_node_id before next spawn.",
        ],
    },
    "C6.4": {
        "title": "parallel workflow branches via work orders",
        "parent": "C6",
        "release": "v2.27",
        "narrative": (
            "Independent workflow branches—nodes with no path between them—may run in parallel via C3.2 work orders "
            "and C4.1 lane leases, each branch carrying its own current_node pointer under active_workflow."
        ),
        "steps": [
            "validate-workflow-dag.py identifies parallel-ready antichains; orchestrate-program assigns lanes per branch.",
            "state.pursuit.active_workflow.branches[] holds per-branch current_node_id and lease owner.",
            "Join nodes declare required upstream branch outputs as typed inputs—manifest integration contract.",
            "Parallel branches must not share mutable output paths without explicit gate merge transistor.",
            "Program goal_verify waits for all branches to reach terminal nodes before G2 rollup.",
        ],
    },
    "C6.5": {
        "title": "workflow node rollup to goal_verify",
        "parent": "C6",
        "release": "v2.26",
        "narrative": (
            "Goal scope completion requires terminal workflow nodes reached with evidence, not only legacy task "
            "checklist done. goal_verify aggregates per-node evidence paths listed in the DAG."
        ),
        "steps": [
            "A2.4 goal_scope_complete checks active_workflow.terminal_nodes all in completed_nodes[].",
            "goal_verify_command receives manifest of evidence paths from workflow completion record.",
            "Partial workflow completion without waived nodes blocks H3 per INTRO-1.3.",
            "Rollback (G6.4) may reset from failed_node without rerunning succeeded upstream nodes.",
            "Pack F1.8 verify suites may append domain checks beyond generic workflow rollup.",
        ],
    },
    "D1.7": {
        "title": "L6 transistor registered composable block",
        "parent": "D1",
        "release": "v2.24",
        "narrative": (
            "L6 is the promotion ladder capstone: a reusable block registered in the transistor catalog with "
            "typed I/O, executor binding, and verify—composable in generator workflows. L2 scripts often "
            "implement the executor inside an L6 manifest."
        ),
        "steps": [
            "Promotion target_level L6 adds docs/platform/transistors/<id>.json plus TRANSISTORS.md row.",
            "L6 subsumes L2–L5 artifacts: a transistor may reference script path, skill wrapper, hook, or pack fragment.",
            "Ephemeral L0 must not remain the steady state for any capability appearing in two workflows.",
            "L6 definition of done extends D6 with transistor-specific criteria (D6.5).",
            "Fork versus extend follows D5.2/D5.3 with semver on transistor_id.",
        ],
    },
    "D2.1.5": {
        "title": "enqueue compose miss missing transistor",
        "parent": "D2.1",
        "release": "v2.24",
        "narrative": (
            "When workflow composition cannot find a registry transistor for a required capability, enqueue "
            "promotion with target_level L6 and capability metadata—extending E2.5/E7.4 compose-miss path."
        ),
        "steps": [
            "promotion_queue item adds fields: capability_id, suggested_io_schema, source_workflow_id.",
            "Product turn may proceed at L0 for that node only with divergence log until platform drain mints L6.",
            "Repeated compose miss for same capability_id raises priority per D3.2.",
            "Platform worker D4.7 extracts transistor from repeated L0 execution traces.",
            "Blocking H2 when miss count exceeds pack threshold without promotion progress.",
        ],
    },
    "D4.7": {
        "title": "platform work transistor extraction",
        "parent": "D4",
        "release": "v2.24",
        "narrative": (
            "Platform turn work type: distill repeated manual or L0 sequences into L6 transistor manifests—"
            "generalized I/O, script/tool executor, verify command, catalog registration."
        ),
        "steps": [
            "Input: promotion_queue item with traces from worker promotion_note or divergence log.",
            "Output: docs/platform/transistors/<id>.json, unit test, TRANSISTORS.md row, staleness node.",
            "Prefer hard executor extraction from existing L2 script before wrapping soft templates.",
            "Run list-transistors.py --check-duplicates to satisfy G5.6 duplicate tooling control.",
            "Regenerate CATALOG.md via D4.5 after extraction completes.",
        ],
    },
    "D6.5": {
        "title": "platform done transistor registry and graph",
        "parent": "D6",
        "release": "v2.24",
        "narrative": (
            "Platform promotion to L6 completes only when the transistor is registered, referenced by at least "
            "one workflow or task card, verify-tested, and wired in staleness graph (E5.4)."
        ),
        "steps": [
            "D6.1–D6.4 remain necessary; D6.5 adds TRANSISTORS.md INDEX row and schema validation pass.",
            "At least one docs/workflows/*.json or pack template references the new transistor_id.",
            "tests/unit/test_transistor_<id>.py or transistor verify script exits 0.",
            "docs/manifest/staleness.json registers node; reconcile-stale propagates bumps.",
            "False complete audit: audit-hierarchy-depth equivalent for transistor registry coverage.",
        ],
    },
    "E6.1": {
        "title": "catalog transistors manifest registry",
        "parent": "E6",
        "release": "v2.24",
        "narrative": (
            "docs/platform/transistors/ holds one JSON manifest per transistor; docs/platform/TRANSISTORS.md "
            "is the generated INDEX merged into E1.7 CATALOG.md umbrella."
        ),
        "steps": [
            "S0 regenerate-transistors-index.py runs on transistor JSON changes.",
            "Each entry lists capability_tags, class (hard|soft|gate), maturity, pack provenance.",
            "E1.7 umbrella includes transistors section with bidirectional links to scripts and playbooks.",
            "Empty registry blocks workflow-compose for non-trivial goals until bootstrap transistors ship.",
            "Staleness E5.4 marks workflows stale when referenced transistor version changes.",
        ],
    },
    "E6.2": {
        "title": "transistor schema id version typed io",
        "parent": "E6",
        "release": "v2.24",
        "narrative": (
            "Transistor manifest schema defines id, version, capability_id, class, inputs[], outputs[], "
            "preconditions[], executor, verify, and promotion provenance—enabling S0 wiring validation."
        ),
        "steps": [
            "Schema file: docs/platform/schemas/transistor.v1.json; validated on commit via validate-workflow.py.",
            "Inputs/outputs use typed slots: string, path, json, artifact_ref, enum with optional schema $ref.",
            "preconditions are S0-checkable predicates before executor runs.",
            "version semver; breaking output changes require fork (D5.3) not silent overwrite.",
            "SEC-18 documents field semantics; leaf specs must not diverge.",
        ],
    },
    "E6.3": {
        "title": "transistor classes hard soft gate",
        "parent": "E6",
        "release": "v2.24",
        "narrative": (
            "Three executor classes: hard (deterministic script/tool), soft (bounded LLM with output schema), "
            "gate (branch on verify/predicate). Target maturity mix: ~70% hard, ~20% soft, ~10% gate."
        ),
        "steps": [
            "hard: executor.kind script|tool; no LLM in block; preferred for all control-adjacent work.",
            "soft: executor.kind soft_template with prompt_template_path, output_schema, max_tokens, capability_class S1.",
            "gate: executor.kind gate with predicate script only; edges defined in workflow DAG not in prose.",
            "Pack maturity report (SEC-15-v2.28) flags soft-heavy workflows for promotion debt.",
            "Ranking in E6.5 always prefers hard over soft for same capability_id.",
        ],
    },
    "E6.4": {
        "title": "list-transistors query io compatibility",
        "parent": "E6",
        "release": "v2.24",
        "narrative": (
            "list-transistors.py queries by capability tag and optional required output types—composer uses "
            "this before list-components for workflow stitching."
        ),
        "steps": [
            "CLI: --capability, --produces, --consumes, --class hard|soft|gate.",
            "Returns ranked hits compatible with upstream node outputs for DAG extension.",
            "Integrates with librarian suggested_components in B2.2 briefing.",
            "Empty result triggers E7.4 promotion enqueue—not improvised implement.",
            "Unit tests under tests/unit/test_list_transistors.py.",
        ],
    },
    "E6.5": {
        "title": "compose rank hard transistor script soft",
        "parent": "E6",
        "release": "v2.24",
        "narrative": (
            "Extends E2.3 ranking for workflow node binding: hard_transistor > script > soft_transistor > "
            "playbook > skill > facts. Gate transistors are not capability substitutes—they are edges."
        ),
        "steps": [
            "When filling a workflow node, composer applies E6.5 before E2.3 legacy single-component compose.",
            "Ties break toward higher maturity and pack-authored transistors (F1.9).",
            "Invoking soft when hard exists requires B4.4 divergence with justification.",
            "Facts disambiguate only; never replace executable transistors in ranked slots.",
            "Conformance check in validate-workflow.py when task card transistor_id mismatches rank.",
        ],
    },
    "E7.1": {
        "title": "resolve deliverable type workflow template",
        "parent": "E7",
        "release": "v2.27",
        "narrative": (
            "Composition starts by mapping goal type and pack deliverable to a seed workflow template—"
            "software-greenfield, iterative-feature, game-asset-rig, etc.—before custom node insertion."
        ),
        "steps": [
            "Pack templates under template-packs/*/workflows/ per F1.9; _shared holds generic seeds per F5.4.",
            "program-scoper records deliverable_type in state.goal for composer lookup.",
            "Template copy is by reference; instance params filled from success_criteria.",
            "No template match triggers blank DAG with capability decomposition—not skip compose.",
            "Template version pinned in workflow metadata for staleness tracking.",
        ],
    },
    "E7.2": {
        "title": "stitch transistors into generator DAG",
        "parent": "E7",
        "release": "v2.25",
        "narrative": (
            "Composer iterates template gaps: for each required capability, list-transistors, rank per E6.5, "
            "wire outputs to inputs, insert gate nodes at verify boundaries."
        ),
        "steps": [
            "Walk template or decomposed capability list in dependency order.",
            "Each stitch adds node + edges; params from goal context and upstream output refs.",
            "Subgraph reuse: reference pack standard_cells when F5.4 defines them.",
            "Composer output includes unresolved[] array driving promotion_queue.",
            "Human-readable mermaid summary optional in H1 plan; JSON is authoritative.",
        ],
    },
    "E7.3": {
        "title": "validate wiring preconditions postconditions S0",
        "parent": "E7",
        "release": "v2.25",
        "narrative": (
            "validate-workflow-dag.py verifies DAG acyclicity, typed edge compatibility, gate edge completeness, "
            "and transistor preconditions satisfiable from goal inputs—before implement starts."
        ),
        "steps": [
            "Run at workflow-compose phase exit and on any DAG edit before resume.",
            "Type mismatch between node output and downstream input fails closed with line-level report.",
            "Unknown transistor_id or stale version fails per E5.4 graph.",
            "Integrates with validate-workflow.py in CI on docs/workflows/ changes.",
            "Pass result stored in state.pursuit.active_workflow.validation_hash.",
        ],
    },
    "E7.4": {
        "title": "workflow miss enqueue transistor promotion",
        "parent": "E7",
        "release": "v2.24",
        "narrative": (
            "Extends E2.5: compose miss at workflow level enqueues L6 promotion with capability and I/O hints; "
            "product may proceed with explicit L0 node waiver in DAG metadata."
        ),
        "steps": [
            "Unresolved workflow nodes marked l0_waiver: true require journal rationale and expiry.",
            "promotion_queue items link source_workflow_id and node_id for traceability.",
            "Platform drain prioritizes misses blocking critical path nodes per D3.3.",
            "Second workflow needing same miss without promotion triggers H2.",
            "Divergence log records L0 waivers for G5.8 metrics.",
        ],
    },
    "E7.5": {
        "title": "pack generator workflow templates inherit",
        "parent": "E7",
        "release": "v2.27",
        "narrative": (
            "Template-packs ship generator workflow templates and transistor libraries new companies inherit "
            "on day one—organizational capital beyond prose playbooks."
        ),
        "steps": [
            "F1.9 defines pack workflows/ and transistors/ directories in pack schema.",
            "Company instantiate copies template refs into pursuit state; does not fork silently.",
            "Cross-pack import via F5.1 for micro-pack workflow fragments.",
            "Pack verify suites (F1.8) may require end-to-end template dry-run in CI.",
            "Pack ceiling F5.3 applies to transistor forks as with other artifacts.",
        ],
    },
    "E5.4": {
        "title": "staleness workflow graph transistor nodes",
        "parent": "E5",
        "release": "v2.25",
        "narrative": (
            "Staleness graph extends to workflow JSON files and transistor manifest nodes—upstream transistor "
            "version bump marks dependent workflows and active_workflow stale until reconcile."
        ),
        "steps": [
            "reconcile-stale reads transistor version edges from docs/manifest/staleness.json.",
            "Active pursuit pauses implement when active_workflow.validation_hash stale.",
            "Re-compose may patch nodes in place if backwards compatible per D5.2.",
            "Breaking transistor fork requires workflow version bump and re-validation.",
            "Platform promotion D6.5 must register staleness edges on publish.",
        ],
    },
    "F1.9": {
        "title": "pack transistors and generator workflows",
        "parent": "F1",
        "release": "v2.27",
        "narrative": (
            "Pack schema adds workflows/*.json generator templates and transistors/*.json domain blocks—"
            "game studio mesh/rig/import, data platform ingest/model/deploy, software delivery scaffold chains."
        ),
        "steps": [
            "company.yaml references default_workflow_template per pipeline_id.",
            "Roles bind to subgraphs of pack workflows via F1.2 pipeline slice fields.",
            "Pack CI validates all transistors and workflows against v1 schemas.",
            "Reference implementations in SEC-15-v2.20 and v2.21 include transistor libraries.",
            "Export upward from consumer repos via D4.6 pack fragment export.",
        ],
    },
    "F5.4": {
        "title": "shared transistors library template-packs _shared",
        "parent": "F5",
        "release": "v2.27",
        "narrative": (
            "template-packs/_shared/transistors/ holds domain-agnostic blocks: git-commit, verify-pytest, "
            "route-tier-preflight, journal-dual-write, scaffold-module—imported by all industry packs."
        ),
        "steps": [
            "F5.1 micro-pack imports may add supplemental transistors without overriding _shared ids.",
            "Shared transistor semver is organization-wide; breaking change requires migration notes.",
            "list-transistors defaults to searching _shared then pack overlay.",
            "Promotion from consumer repo targets _shared when capability is generic per D4.6 review.",
            "CATALOG.md lists _shared transistors in dedicated section.",
        ],
    },
    "G2.5": {
        "title": "per-node evidence rollup goal_verify",
        "parent": "G2",
        "release": "v2.26",
        "narrative": (
            "goal_verify aggregates evidence from each completed workflow node—transistor verify commands "
            "and evidence_path_template outputs—before G2.3 H3 transition."
        ),
        "steps": [
            "goal-verify.py accepts --workflow-evidence manifest from active_workflow.completed_nodes.",
            "Missing node evidence fails rollup even if legacy task cards marked done.",
            "Tool/MCP evidence types per I4.3 included in manifest when transistors use tool executors.",
            "Regression batch G2.4 runs transistor verify suite subset on implement batches.",
            "Evidence immutability H4 applies per node path.",
        ],
    },
    "G5.8": {
        "title": "mistake fuzzy chain lost in prose workflow control",
        "parent": "G5",
        "release": "v2.26",
        "narrative": (
            "Fuzzy-chain mistake class: long improvised edit sequences without workflow node boundaries—"
            "neutralized by mandatory workflow-compose, one-node-per-turn, and transistor verify per step."
        ),
        "steps": [
            "Detect: implement turns without workflow_node_id when C6.1 applies; divergence log count spikes.",
            "Control: block advance at preflight; require workflow bind or H2 waiver.",
            "Metrics: SEC-15-v2.28 dashboard shows fuzzy-chain incidents per goal.",
            "Related controls: G5.2 scope creep, G5.6 duplicate tooling, B4.3 compose-first.",
            "Recovery: G6.4 checkpoint replay from last verified node.",
        ],
    },
    "G6.4": {
        "title": "workflow checkpoint replay from failed node",
        "parent": "G6",
        "release": "v2.26",
        "narrative": (
            "On node verify failure, active_workflow records failed_node_id and checkpoint artifacts; "
            "resume replays from that node after H2 fix—not full workflow restart unless graph changes."
        ),
        "steps": [
            "state.pursuit.active_workflow.failed_node_id set; completed_nodes preserved.",
            "Retry increments node retry_count; gate edges handle retry vs H2 per B6.4.",
            "Graph edit invalidates downstream completed nodes via E5.4 stale mark.",
            "preCompact snapshot H6 includes active_workflow for autopilot resume.",
            "Manual operator reset requires journal entry clearing failed state.",
        ],
    },
    "H1.7": {
        "title": "state active_workflow block",
        "parent": "H1",
        "release": "v2.26",
        "narrative": (
            "Additive state block tracking generator workflow execution: workflow_id, path, current_node_id, "
            "completed_nodes[], failed_node_id, branches[], validation_hash, terminal_nodes[]."
        ),
        "steps": [
            "validate-workflow.py schema-validates active_workflow when present.",
            "Dual-write on every node completion; product workers read-only except conductor merge.",
            "Null active_workflow allowed only before C6.1 or for taxonomy-exempt goals.",
            "sync-state.py repairs partial writes from journal Workflow section.",
            "Export contract I5/J5 documents active_workflow for headless SDK consumers.",
        ],
    },
    "I4.4": {
        "title": "transistor executors MCP tool script boundary",
        "parent": "I4",
        "release": "v2.26",
        "narrative": (
            "Runtime policy for transistor executors: scripts via S0, tools via tool-operator/MCP with role "
            "allowlist (F6.3), soft via bounded workers—never bypass preToolUse hooks."
        ),
        "steps": [
            "executor.kind tool resolves to pack MCP allowlist entry; evidence via I4.3 types.",
            "Blender/UE/browser transistors in game studio pack use same boundary as I4.1.",
            "Script executors run in verifier/tool-operator shell subagents—not parent context.",
            "Cross-executor workflows must declare artifact handoff paths in transistor I/O—not chat memory.",
            "Unsafe command G5.7 applies per executor invocation.",
        ],
    },
    "SEC-15-v2.24": {
        "title": "Release v2.24 transistor schema registry list-transistors",
        "parent": "SEC-15",
        "release": "v2.24",
        "narrative": (
            "Ships transistor.v1.json schema, docs/platform/transistors/ bootstrap set, list-transistors.py, "
            "TRANSISTORS.md generation, D1.7 L6 promotion path, E6 catalog integration."
        ),
        "steps": [
            "Bootstrap transistors: validate-workflow-run, verify-router-invoke, route-tier-preflight, dual-write-journal.",
            "validate-workflow.py extended for transistor schema.",
            "SEC-18 published as design authority.",
            "Unit tests for schema and list-transistors.",
            "No workflow-compose mandatory yet—registry foundation only.",
        ],
    },
    "SEC-15-v2.25": {
        "title": "Release v2.25 workflow DAG validate-workflow-dag",
        "parent": "SEC-15",
        "release": "v2.25",
        "narrative": (
            "Ships workflow-dag.v1.json schema, validate-workflow-dag.py, C6.1 workflow-compose phase, "
            "E7.2/E7.3 composition validation, E5.4 staleness for workflows."
        ),
        "steps": [
            "workflow-compose phase inserted in software-greenfield pipeline manifest.",
            "docs/workflows/ directory convention established.",
            "CI validates workflow JSON on PR.",
            "E2.3 ranking doc updated to reference E6.5.",
            "Composer skill not required yet—manual/S2 template DAG acceptable.",
        ],
    },
    "SEC-15-v2.26": {
        "title": "Release v2.26 workflow-composer active_workflow execution",
        "parent": "SEC-15",
        "release": "v2.26",
        "narrative": (
            "Ships workflow-composer skill, B6 routing, H1.7 active_workflow state, C6.3 task card binding, "
            "one-node-per-turn execution, G2.5/G5.8/G6.4 verification and recovery."
        ),
        "steps": [
            ".cursor/skills/workflow-composer/SKILL.md and validate integration.",
            "new-task-card.py workflow_node_id field.",
            "goal-verify.py workflow evidence rollup.",
            "Autopilot respects active_workflow in check-pipeline-blocked extended.",
            "End-to-end demo: iterative feature via 5+ transistor workflow.",
        ],
    },
    "SEC-15-v2.27": {
        "title": "Release v2.27 pack workflow templates cross-domain",
        "parent": "SEC-15",
        "release": "v2.27",
        "narrative": (
            "Ships F1.9/F5.4 pack transistors and workflow templates; E7.1/E7.5 template inheritance; "
            "C6.4 parallel branches; game studio and data platform reference transistors."
        ),
        "steps": [
            "template-packs/_shared/transistors/ populated.",
            "game-asset-pipeline and data-platform packs gain workflows/ trees.",
            "list-transistors searches pack overlay.",
            "Program parallel lanes run parallel workflow branches.",
            "Pack CI transistor validation.",
        ],
    },
    "SEC-15-v2.28": {
        "title": "Release v2.28 transistor maturity dashboard metrics",
        "parent": "SEC-15",
        "release": "v2.28",
        "narrative": (
            "Operator polish: dashboard hard/soft/gate ratio, fuzzy-chain incident count, promotion debt by "
            "capability, workflow coverage percent per pack. Optional workflow DAG viewer in docs/platform/."
        ),
        "steps": [
            "generate-dashboard.py adds transistor metrics section.",
            "G5.8 fuzzy-chain counters in state.platform.metrics.",
            "Promotion debt SLA alerts when L0 waivers exceed threshold.",
            "Optional static HTML DAG viewer from workflow JSON—non-blocking.",
            "Closes SEC-18 acceptance checklist for v2.24–v2.28 transistor program.",
        ],
    },
    "SEC-17-7": {
        "title": "Decision transistor granularity one verify boundary",
        "parent": "SEC-17",
        "release": "v2.24",
        "narrative": (
            "**Resolved:** One transistor = one verify boundary. If verify cannot be expressed as a single "
            "command or predicate, split the block. Maximum soft scope = one bounded S1 job with schema output."
        ),
        "steps": [
            "Decision recorded 2026-06-28; supersedes informal larger-block proposals.",
            "Evidence: G5.4 skipped tests, G5.1 hallucinated done—per-node verify contains blast radius.",
            "Implement feature whole-task is a workflow, not one transistor.",
            "SEC-18 §Granularity references this decision.",
        ],
    },
    "SEC-17-8": {
        "title": "Decision composer S3 skill not conductor inline",
        "parent": "SEC-17",
        "release": "v2.26",
        "narrative": (
            "**Resolved:** Workflow composition runs via dedicated workflow-composer skill (S3) with catalog-only "
            "reads; genius conductor approves and dual-writes, does not compose large DAGs inline."
        ),
        "steps": [
            "Evidence: B3.1 genius thin turns, E4.3 allowed_reads cap—inline compose violates both.",
            "Composer spawn follows orchestrate-subagents contract.",
            "Economy tier forbidden for composer—graph mistakes are expensive.",
        ],
    },
    "SEC-17-9": {
        "title": "Decision JSON DAG authoritative visual editor optional",
        "parent": "SEC-17",
        "release": "v2.25",
        "narrative": (
            "**Resolved:** Machine-readable workflow JSON is required and authoritative for v2.25+; visual "
            "node editor is optional operator tooling in v2.28+, never a substitute for schema validation."
        ),
        "steps": [
            "Evidence: headless SDK (I2), export-contract (J5) require JSON; UI-only blocks automation.",
            "H1 plan may include mermaid for humans; validate-workflow-dag.py validates JSON only.",
            "Game-dev-style blocks map 1:1 to JSON nodes—same registry.",
        ],
    },
    "SEC-17-10": {
        "title": "Decision global _shared transistors plus pack overlay",
        "parent": "SEC-17",
        "release": "v2.27",
        "narrative": (
            "**Resolved:** Transistor library is two-tier: template-packs/_shared/transistors/ (global) plus "
            "pack-specific overlay; list-transistors merges with pack_id filter. No per-repo ad hoc forks."
        ),
        "steps": [
            "Evidence: F5.2 _shared pattern, F5.3 ceiling, G5.6 duplicate tooling.",
            "Consumer repo promotions target _shared when generic; domain blocks stay in pack.",
            "Compose query order: pack overlay overrides _shared on id conflict only with semver fork.",
        ],
    },
}
