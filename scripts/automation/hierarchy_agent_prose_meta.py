#!/usr/bin/env python3
"""Agent-authored Reader narratives for meta / front-matter hierarchy leaves."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

META_NARRATIVES: dict[str, str] = {
    "INTRO-0": """\
Today's harness (v2.0–v2.13) is a verified delivery system: conductor, state machine, evidence, and autopilot-until-blocked. It still stops for Continue, treats many design gates as permanent human checkpoints, and treats platform evolution as required side work.

The target is an ultimate AI worker: organizational reliability with AI failure modes neutralized by deterministic verification, catalog composition, and parallel platform evolution—orchestrated at company scale through template-packs. Three structural shifts drive the design: a pursuit loop that runs until goals verify (not until a token burst ends); parallel product and self-improvement work—while executing the current project the system also works on itself from a queued list of improvements (scripts, playbooks, checks) discovered during real delivery, so getting better does not require stopping the product; and template-packs as reusable blueprints for a whole company slice (roles, pipelines, verification) instead of reinventing setup every time.

This executive summary orients every later chapter. Read it once to understand why the ten planes exist and why human involvement collapses to three touchpoints. See [Vision §0 — Executive summary](../../full-automation-vision-and-hierarchy.md#0-executive-summary) for the authoritative wording.""",
    "INTRO-1.1": """\
One hundred percent automation does not mean humans disappear—it means humans appear only where policy requires authority, judgment of record, or external access the system cannot obtain. After initial planning is approved, the system owns SDLC execution: implement, test, refactor, integrate, and deploy preparation.

In scope: multi-role company workflows via template-packs, blocker detection with structured escalation, and harness self-improvement through the platform queue. Out of scope: irreversible production actions without verify and rollback, silent waiver of safety gates, and subjective aesthetic approval unless encoded in acceptance tests.

Pack authors and operators use this boundary list when deciding whether a workflow belongs in autonomous pursuit or must remain H2-always. See [INTRO-1.2](INTRO-1.2-human-touchpoint-contract-h1-h2-h3.md) for where humans still interact.""",
    "INTRO-1.2": """\
The expert system recognizes exactly three human touchpoint classes. H1 is initial planning: the operator supplies a spec or company charter and receives an approved plan artifact—once per project, program, or pack instantiation. H2 is blocker assistance: triggered when preflight blocks, goal verification fails, or an external dependency is missing; the system pauses, notifies, and resumes when unblocked. H3 is final sign-off: triggered only after goal_verify passes; accept or reject with notes, where rejection re-enters pursuit.

Everything else—including HLD and DD review by default—becomes agent self-gate with evidence unless strict HITL mode is enabled. This contract is the social license for autopilot: operators know when they must act versus when they may read dashboards only.""",
    "INTRO-1.3": """\
A goal is achieved only when five conditions hold together: acceptance artifacts exist, automated goal verification passes, staleness and integration graphs are consistent, no blocking questions remain without deferred rationale, and platform debt for the goal is promoted or explicitly waived with expiry.

The agent does not stop for status theater. It stops on H1, H2, H3, unrecoverable failure, or resource budget caps. This criterion prevents the common failure mode of marking tasks done while the overarching goal remains unproven—Plane G goal_verify exists to enforce this bar.""",
    "MASTER-A": """\
Plane A is pursuit and control: the always-on loop that runs from approved intent until verification succeeds or a defined stop reason fires. It owns the goal model, preflight, one-step execution, post-step routing, goal-level verification handoff, and the semantics of Continue redefined for autonomy.

Every other plane feeds or constrains this loop—B routes execution, C performs product steps, G proves outcomes—but A is where "never stop until verified" lives. When reading A1–A6 capabilities, keep this chapter summary in mind as the architectural north star for that branch.""",
    "MASTER-B": """\
Plane B is cognition and routing: who acts on each turn (S0 scripts through S4 governance), at what model tier, and with what interleaved product-and-self-improvement schedule. The genius-tier conductor orchestrates; economy workers implement bounded task cards.

Deterministic-first is non-negotiable: if behavior exists under scripts/, S0 runs before improvisation. Plane B connects operator policy (model-policy.json) to everyday pursuit turns.""",
    "MASTER-C": """\
Plane C is product execution—the pipelines, phases, task cards, program parallelism, and feature delivery paths that turn design into shipped software with evidence. It is the familiar SDLC harness extended to run inside pursuit rather than as a separate manual workflow.

Task evidence gates remain; they feed upward into goal_verify rather than replacing it.""",
    "MASTER-D": """\
Plane D is how the system improves itself while it works. During real delivery it notices repeated mistakes, manual steps, and missing playbooks, queues them, and turns them into scripts and checks—on a schedule that runs alongside the current project so delivery keeps moving while the next project will run better.

Reuse matures from ephemeral reasoning to scripts, playbooks, and template-pack fragments—this plane owns that ladder.""",
    "MASTER-E": """\
Plane E is knowledge and composition: one catalog surface, mandatory compose-before-invent, facts and decisions, context retrieval layers, and staleness when upstream designs change.

Before any S1+ worker invents a new pattern, Plane E requires searching the catalog and binding existing components.""",
    "MASTER-F": """\
Plane F defines organization through template-packs—company schema, roles, pipelines, integrations, and example packs (game studio, data platform). A pack is a company slice the harness can instantiate and pursue goals within.

Cross-pack shared libraries and role-to-agent mapping live here as well.""",
    "MASTER-G": """\
Plane G is verification and quality: evidence gates, goal-level verification, workflow conformance, automated review triggers, mistake-class controls, and rollback. It ensures "done" means proven, not asserted.

Task-level verify-router evidence is necessary; goal_verify is sufficient for H3.""",
    "MASTER-H": """\
Plane H persists state—journal and machine state dual-write, artifact graphs, immutable evidence logs, worker audit trails, and snapshots for resume after compaction or crash.

If Plane A is the heartbeat, Plane H is the memory that makes restart safe.""",
    "MASTER-I": """\
Plane I integrates runtimes: Cursor IDE sessions, local SDK daemon, headless CI, external tools via MCP, and operator notifications on H2/H3 only.

The same pursuit semantics must hold whether the conductor runs in-editor or headless. Hooks (beforeSubmitPrompt, preToolUse, preCompact) and SDK daemon loops are part of this plane—not optional integrations.""",
    "MASTER-J": """\
Plane J governs operators—model policy, automation waivers, optional strict HITL, audit of waivers, export contracts for external orchestrators, and release-queue evolution for the harness itself (separate from consumer goals).

Operator-facing policy lives here; consumer product goals should not mutate these artifacts without platform intent.""",
    "SEC-13": """\
This chapter is the single picture of how the target system behaves end to end after H1 approves a plan. Pursuit loops: preflight, one pipeline step, optional platform queue drain every K steps, product step otherwise, repeat until scope completes, then goal_verify, then H3 on pass or H2 on failure.

The diagram in the vision document is the authoritative control flow—use it when tracing any A2 or C2 capability back to overall behavior. Project steps and self-improvement steps alternate on a fixed schedule so neither the current goal nor the improvement backlog is neglected—scheduling is explicit in the loop, not ad hoc.""",
    "SEC-14": """\
Gap analysis makes the migration from today's harness to the target architecture auditable. Each row names what v2.13 does today, what the north star requires, and which plane sections bridge the gap—pursuit loop depth, human gate reduction, platform queue, catalog compose-first, pack schema, goal_verify, role switching, and stop-reason taxonomy.

Implementers should treat this table as a program backlog ordered by SEC-15 releases rather than as prose alone.""",
    "SEC-15-v2.14": """\
Release v2.14 establishes the goal model in state.json and introduces goal_verify as a first-class field alongside extended check-pipeline-blocked semantics. Without this release, pursuit cannot attach verification to nested goals or distinguish task done from goal achieved.

Deliverables include goal-keeper behavior, additive state.goal schema, and tests that fail if goal_verify is bypassed.""",
    "SEC-15-v2.15": """\
Release v2.15 hardens the pursuit loop: goal_autopilot mode, optional uncapped session settings, and self-gate defaults for HLD/DD when strict_hitl is false. This is the release that makes "always-on" real rather than a 25-step autopilot cap.

Preflight, one-step execution, and stop-reason taxonomy from Plane A must be green before later platform work relies on them.""",
    "SEC-15-v2.16": """\
Release v2.16 introduces the platform promotion queue in state and a scheduler that processes one improvement item every K project steps. Delivery and self-improvement run on an interleaved schedule so the current goal keeps moving while the improvement backlog still makes steady progress—this release encodes that bargain in data structures and autopilot scheduling.

Task cards gain Components/Promotion notes so workers know when they must compose from catalog or enqueue promotion work.""",
    "SEC-15-v2.17": """\
Release v2.17 ships catalog discovery and compose-first enforcement: list-components.py generates docs/platform/CATALOG.md, librarian suggests components, and rules require composition before S1+ invention.

This release reduces duplicate tooling and scope creep—Plane E becomes operational, not aspirational.""",
    "SEC-15-v2.18": """\
Release v2.18 extends staleness and artifact graphs to platform nodes so design changes ripple to dependent scripts, playbooks, and pack fragments. Reconcile-stale must see platform promotions—not only product design docs.

Without this, platform queue items can promote obsolete patterns into the catalog.""",
    "SEC-15-v2.19": """\
Release v2.19 defines company pack schema v1: company.yaml, roles/*.yaml, and state.company.active_role. Template-packs become instantiable companies the harness can switch roles within during pursuit.

This bridges Plane F organization to Plane H persistence fields. Pack validation tests should fail if roles reference pipelines or tools not declared in the pack manifest.""",
    "SEC-15-v2.20": """\
Release v2.20 delivers a game studio pack reference implementation with an end-to-end demo that uses only H1 and H3 as human touchpoints. It proves the taxonomy and pursuit loop on a creative-industry shape, not only software CRUD.

Success is a reproducible demo script plus goal_verify evidence, not a slide deck.""",
    "SEC-15-v2.21": """\
Release v2.21 delivers a data platform pack reference implementation parallel to the game studio pack—different integrations and roles, same harness contracts. Multi-domain reuse validates Plane F generality.

Cross-pack lessons feed v2.22 shared library work; data-platform MCP and verify paths must appear in goal_verify for the demo goal.""",
    "SEC-15-v2.22": """\
Release v2.22 adds template-packs/_shared/ for cross-pack libraries—common roles, hooks, and verification helpers factored out of duplicate pack content. Packs should compose shared fragments rather than fork copy-paste.

Catalog entries should reference _shared components explicitly.""",
    "SEC-15-v2.23": """\
Release v2.23 polishes operator experience: H2 notifications, self-gate audit trails, and dashboard surfaces for goal depth and queue depth. Autonomy without observability erodes trust—this release makes pursuit legible from STATUS.md and dashboard.md.

It closes the initial v2.14–v2.23 roadmap; later work continues additively on state.json version 2.""",
    "SEC-17-1": """\
Open decision: how rigorous should middle design gates be when strict_hitl is off? Options span checklist-only self-gate, automated LLM reviewer, or second economy reviewer. The choice affects cost, latency, and mistake rates for HLD/DD/manifest phases.

Record the decision as an ADR when made; until then, implementers should default to checklist + evidence paths that goal_verify can audit.""",
    "SEC-17-2": """\
Open decision: what granularity triggers H3? Per task, milestone, release, or company-level goal? Finer H3 increases operator load; coarser H3 increases blast radius of acceptance.

Pack authors should declare H3 scope in company.yaml so pursuit knows when to request sign-off.""",
    "SEC-17-3": """\
Open decision: platform scheduling ratio—fixed one platform step per K product steps versus adaptive scheduling by queue depth. Fixed ratios are predictable; adaptive ratios respond to promotion backlog pressure.

Simulation on real queue depths should inform the choice before hard-coding K in autopilot.""",
    "SEC-17-4": """\
Open decision: budget caps for goal_autopilot—unlimited pursuit versus daily token/step checkpoints. Unlimited pursuit maximizes autonomy; checkpoints protect cost and surface H2 when budgets exhaust.

Budget fields in Plane A interact directly with this decision. Operators need dashboard visibility before choosing unlimited pursuit in production.""",
    "SEC-17-5": """\
Open decision: can packs mark legal/finance roles as fully automated, or must they always escalate H2? Authority-of-record work may never belong in autonomous pursuit regardless of model capability.

Pack schema should encode role_class with automation_allowed flags once decided.""",
    "SEC-17-6": """\
Open decision: single pursuit stack versus company_autopilot with prioritized multi-goal queue. Single stack simplifies state; multi-goal matches real companies running parallel initiatives.

state.goal nesting and parent_goal interact with whichever model is chosen. An ADR should specify preemption rules when two goals contend for the same active role.""",
    "APP-A-discover": """\
Discover and plan work covers requirements elicitation (with H1 assist), research, architecture tradeoffs, and milestone planning. In a template-pack, each leaf maps to pipeline phases, verification commands, and playbooks—not informal chat.

Pack authors use this taxonomy slice to ensure planning roles produce approved artifacts the pursuit loop can consume without re-asking baseline questions.""",
    "APP-A-design": """\
Design work spans UX/UI, API and data models, integration design, and security/compliance design. Autonomous execution still requires machine-checkable outputs: diagrams, schemas, and review triggers—not prose-only decisions.

Every design artifact should link forward to task cards and backward to catalog components where reuse applies.""",
    "APP-A-build": """\
Build work is implement, integrate, and refactor—the core product execution surface Plane C owns. Tasks must carry evidence commands; pursuit continues only when verify passes or structured H2 fires.

Build roles in packs should default to S0/S1-heavy routing with conductor merge at S3 boundaries.""",
    "APP-A-verify": """\
Verify work spans unit, integration, E2E, tool outputs, goal_verify, and conformance scripts. Verification is not a phase humans optionally trigger—it is the gate that separates pursuing from achieved.

Pack workflows must name verify commands explicitly so goal_verify can aggregate them.""",
    "APP-A-release": """\
Release and operate covers deploy preparation, release queues, operator dashboards, and production-adjacent automation with rollback paths. Irreversible production actions remain out of scope unless verify and rollback are defined.

This slice connects Plane I runtime integrations to Plane G rollback policies.""",
    "APP-A-organize": """\
Organize company work covers pack instantiation, role queues, active_role switching, and cross-team coordination inside template-packs. It is how a single harness pretends to be an org chart without forking state per employee.

company.yaml and roles/*.yaml from Plane F are the primary artifacts here.""",
    "APP-A-improve": """\
Improve platform work is promotion, turning repeated patterns into playbooks, script extraction, and catalog curation—Plane D and E activities that run alongside product pursuits via the platform queue.

Without this slice in packs, organizations revert to one-off heroics instead of maturing reuse.""",
    "APP-B": """\
This appendix sketches additive state.json fields for v2 goals, platform queues, pursuit counters, HITL pending markers, and company context—without breaking state.json version 2 compatibility. Implementers use it as a map when reading Plane H specs.

The sketch is not a substitute for validate-workflow.py and schema tests; it orients readers before they open individual H1.x field specs.""",
}


def apply_meta(out_dir: Path | None = None) -> int:
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from hierarchy_agent_prose import apply_narrative  # noqa: E402
    from hierarchy_completeness import item_id_from_path, list_leaf_paths  # noqa: E402

    base = out_dir or ROOT / "documents/plans/full-automation"
    applied = 0
    missing: list[str] = []
    for p in list_leaf_paths(base):
        iid = item_id_from_path(p, p.read_text(encoding="utf-8"))
        if iid not in META_NARRATIVES:
            continue
        new_text, issues = apply_narrative(p, META_NARRATIVES[iid], version="meta")
        p.write_text(new_text, encoding="utf-8")
        applied += 1
        if issues:
            print(f"{iid}: {', '.join(issues)}")
    for k in META_NARRATIVES:
        if k not in {item_id_from_path(p, p.read_text(encoding="utf-8")) for p in list_leaf_paths(base)}:
            missing.append(k)
    print(f"Applied meta agent prose to {applied} leaves")
    if missing:
        print(f"Note: narratives not matched to files: {missing[:5]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(apply_meta())
