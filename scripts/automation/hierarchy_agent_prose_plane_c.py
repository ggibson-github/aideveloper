#!/usr/bin/env python3
"""Agent-authored Reader narratives for Plane C (product execution)."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

PLANE_C_NARRATIVES: dict[str, str] = {
    "C1.1": """\
Greenfield pipeline is the initial build path: parse spec, HLD, DD, diagrams, task breakdown, scaffold, implement loop, done. Phases run in order unless the journal records prior completion; gates default to self-gate plus evidence after H1 except where strict HITL overrides.

This pipeline_id is the default for new repos without an existing delivery baseline. Pursuit attaches consumer goals to greenfield phases via state.json `next_action` and task cards. See AGENTS.md pipeline section for phase skill mapping.""",
    "C1.2": """\
Iterative feature pipeline continues development after initial delivery: gather requirements, research, feature design, approval (or self-gate), branch, implement, test, commit/PR/push. It avoids re-running full greenfield when the repo and harness already exist.

Feature design approval can self-gate when encoded in pack policy; otherwise H1-class approval applies once per feature charter. Evidence and verify-router discipline match greenfield implement phases. Use iterative-feature skill as the conductor entry point.""",
    "C1.3": """\
Multi-domain program pipeline decomposes mega-specs into milestones, workstreams, integration manifest, and parallel lanes—program-scoper first, manifest human gate, then orchestrate-program when lanes are unblocked.

Each stream runs its own phase progression under manifest dependencies; company-level goal_verify rolls up stream completion. This pipeline_id activates when spec size or cross-team coupling exceeds single-stream greenfield assumptions.""",
    "C1.4": """\
Template-packs define alternate pipeline_ids per company type: game studio, data platform, ops-only—each with phase lists, default skills, and verify suites ([F1.8 pack verify](../full-automation/MASTER-F-branch-f---organization-plane.md)). Instantiation sets active pack and pipeline_id in state.

Consumer goals inherit pack pipelines; platform evolution uses release-queue separately. Pack authors document pipeline differences in pack schema rather than forking conductor code.""",
    "C2.1": """\
Spec-parser phase extracts requirements, validates assumptions, lists open questions, and creates or refreshes journal/state via journal-keeper. Blocking questions stop downstream design until answered or deferred with rationale recorded.

Outputs feed hld-writer and program-scoper when mega-spec detected. S0 scripts validate spec structure where templates exist. This phase is the H1 input artifact generator—pursuit should not skip to implement without parsed requirements unless journal says spec phase complete.""",
    "C2.2": """\
Design phase produces HLD, DD (split api/data/ops), and diagrams from approved requirements. Default path uses self-gate plus evidence; strict HITL retains human HLD/DD approval gates from v2.13.

Diagram-generator runs after DD; staleness marks downstream task cards when design changes. Design artifacts live under docs/design/ and docs/diagrams/ per AGENTS.md paths. Conductor spawns dd-writer and diagram workers under S2 templates.""",
    "C2.3": """\
Task-breakdown and scaffold follow approved design: phased TODOS, task cards, environment-setup tasks ordered before package installs, then scaffold-project creates repo layout and CI skeleton. Missing setup tasks violate AGENTS.md rule 17—implement must not start without runnable environment.

Task cards carry verify commands and evidence paths for Plane G. Scaffold outputs are inputs to implement-feature loop; dual-write marks phase complete in journal/state.""",
    "C2.4": """\
Test and git-workflow phase covers test-writer, full suite runs before push, refactor when debt blocks features, and PR/commit when user requests. test-before-push rule applies: unit, integration, e2e when UI exists.

git-workflow runs only when last_verify passed or exceptions documented. This phase connects Plane C delivery to operator git policy without bypassing evidence gates.""",
    "C2.5": """\
Each phase declares inputs, outputs, verify commands, and catalog refs so S0 and reviewers can audit completeness. Phase contracts live in skills and playbooks; pack schema may extend with pack-specific verify.

Missing catalog refs on phase outputs trigger compose-first divergence logging ([B4.4](B4.4-divergence-log-when-not-composing.md)). Phase verify is not goal_verify—it proves phase artifacts exist before next_action advances.""",
    "C3.1": """\
Task cards are the atomic implement unit: scope, allowed_reads, files to touch, test command, evidence path, optional tool command. Components field links catalog entries; promotion_note captures platform queue candidates discovered during implement.

new-task-card.py generates consistent cards from templates. Cards must not duplicate full design docs—reference paths instead. Conductor assigns one card per implement turn when evidence_required is true.""",
    "C3.2": """\
Work orders group task cards for parallel lanes under program mode: lane json, leases, and manifest dependencies prevent two workers editing the same journal writer or conflicting branches.

Orchestrate-program spawns only when manifest gate cleared and spawn_policy allows. Single-stream greenfield uses sequential cards without work orders unless user enables program features.""",
    "C3.3": """\
Evidence per task is mandatory when evidence_required: verify-router or tool-operator writes logs under evidence/, state records evidence_files and last_verify. Implement tasks do not complete on agent assertion alone.

Evidence types include pytest logs, tool output, checksums—see docs/operator/evidence-types.md. Missing evidence blocks goal rollup in C3.4 and goal_verify in Plane A/G.""",
    "C3.4": """\
Task completion rolls up to goal percent complete and goal_verify prerequisites: queue empty, all required evidence passed, conformance green. Rollup is S0 where scripts aggregate task state from state.json and journal mirror.

False rollup—marking goal ready while tasks lack evidence—is a Plane G failure class. Dashboard may show percent for operators; pursuit uses machine checks only.""",
    "C4.1": """\
Workstreams expose lane JSON with lease fields so parallel program lanes claim work safely. Leases expire per A4.3 resource stops; stale leases return items to queue with journal note.

Lane files live under docs/manifest/ program paths; integration-manifest-keeper maintains cross-lane contracts. One conductor remains writer for journal/state even when lanes parallelize implement.""",
    "C4.2": """\
Orchestrate-program skill spawns ready lanes when manifest approved, blocking questions cleared, and spawn_workers true. Each lane worker receives allowed_reads from Librarian briefing and manifest slice only.

Parent conductor merges lane summaries, updates artifact graph, and never clears gates without approval. Failed lane blocks program goal_verify until manifest reconciliation or H2 waiver.""",
    "C4.3": """\
Integration manifest is the cross-stream contract: API surfaces, shared schemas, test harness boundaries, and completion criteria per stream. Human gate before parallel implement unless pack policy self-gates with verify suite.

Manifest changes mark artifact graph nodes stale; dependent lanes pause at preflight until reconcile completes. This document is the program-level analog of feature design approval.""",
    "C4.4": """\
Artifact graph nodes represent design, code, test, and pack artifacts with dependency edges for program and pack scopes. reconcile-artifact-graph marks stale when upstream changes; pursuit respects stale flags before spawn.

Graph complements staleness.json for platform nodes; together they prevent implement against obsolete design. Pack schema may embed graph templates per company type.""",
    "C5.1": """\
Delivery layout standardizes src (or app root), tests/unit, tests/integration, tests/e2e when UI exists, docs paths from AGENTS.md. Scaffold and implement tasks must preserve layout so verify-router and CI find tests predictably.

Pack-defined layouts extend but do not break evidence paths without manifest update. Delivery structure is verify input for goal slices and pack conformance.""",
    "C5.2": """\
Environment setup tasks—portable Python, venv, VS solution, GitHub clone—must appear in task breakdown before library install tasks. AGENTS.md rule 17 requires the agent to install and verify local runnability, not leave setup to the user.

Ordering is enforced in task-breakdown skill behavior and audited in task card dependencies. Skipping env setup causes false implement complete when code cannot run locally.""",
    "C5.3": """\
Definition of done for a goal slice: tasks complete, tests pass (or documented exceptions), evidence on disk, goal_verify ready, no unresolved blocking questions. Differs from task done and phase done—slice satisfied means rollup checks pass for that scope boundary.

H3 still required for verified goal acceptance unless policy waives. Completion status in journal and STATUS.md reflects slice and goal levels distinctly so operators see partial vs achieved accurately.""",
}


def apply_plane_c(out_dir: Path | None = None) -> int:
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from hierarchy_agent_prose import apply_narrative  # noqa: E402
    from hierarchy_completeness import item_id_from_path, list_leaf_paths  # noqa: E402

    base = out_dir or ROOT / "documents/plans/full-automation"
    applied = 0
    for p in list_leaf_paths(base):
        iid = item_id_from_path(p, p.read_text(encoding="utf-8"))
        if iid not in PLANE_C_NARRATIVES:
            continue
        new_text, issues = apply_narrative(p, PLANE_C_NARRATIVES[iid], version="plane-c")
        p.write_text(new_text, encoding="utf-8")
        applied += 1
        if issues:
            print(f"{iid}: {', '.join(issues)}")
    print(f"Applied Plane C agent prose to {applied} leaves")
    return 0


if __name__ == "__main__":
    raise SystemExit(apply_plane_c())
