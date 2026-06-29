#!/usr/bin/env python3
"""Agent-authored Reader narratives for Plane G (verification and quality)."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

PLANE_G_NARRATIVES: dict[str, str] = {
    "G1.1": """\
Task-level verification runs through `scripts/verify-router.py` and the verifier skill: the conductor or shell worker executes the literal Test or Tool command from the task card, writes `evidence/task-NNN-test.log`, and sets `last_verify` in state.json before any implement task advances.

This is the bottom evidence gate—no narrative “tests pass” substitutes for a log file. Non-pytest evidence types follow `docs/operator/evidence-types.md`. Pair with [G1.2](G1.2-evidence-required-state.md) and [B2.4](B2.4-verifier-tool-operator-evidence.md). See [Vision §9 — Branch G](../../full-automation-vision-and-hierarchy.md#9-branch-g-verification-quality-plane-anti-mistake).""",
    "G1.2": """\
When `evidence_required: true` in state.json, the pursuit loop must not advance past the current implement task until `evidence_files` exist and `last_verify` is `passed`. The conductor and workers treat this flag as fail-closed policy, not a journal suggestion.

Git-workflow push is blocked while evidence is missing or verify failed—documented exceptions belong in the journal with operator approval. This capability encodes the evidence-required workspace rule for every pack that ships with verification discipline.""",
    "G1.3": """\
`last_verify` is the machine-readable latch between verify-router output and next_action progression: only `passed` clears the implement gate; `failed` or absent values keep the conductor on the same task card and may trigger [B3.3](B3.3-escalation-loop-on-verify-fail.md) escalation.

Dual-write `last_verify` in the same turn as evidence log creation so resume after laptop close or session compact restores truthful state. Never advance next_action in chat while state still shows failed verify— that is the hallucinated-done mistake class ([G5.1](G5.1-mistake-hallucinated-done-evidence-gate.md)).""",
    "G2.1": """\
Goal-level verification begins with `goal.verify_command` resolved from `state.goal` or the active template-pack verify suite ([F1.8](F1.8-pack-verify-goal-verify-suites.md)). Pack authors declare the command once; consumer goals inherit it on instantiation rather than improvising per sprint.

The command is the contract for H3 readiness: unit, integration, e2e, and tool checks roll up under one invocable entry point (`scripts/goal-verify.py` or pack override). Missing or empty verify_command when goal scope is complete is an H2 blocker, not a silent skip.""",
    "G2.2": """\
Goal verify aggregates evidence from every task tier: unit tests under `tests/unit/`, integration under `tests/integration/`, e2e/UI under `tests/e2e/` when the app has a UI, plus tool-command logs referenced on task cards. verify-router task passes must all be `passed` before goal verify runs.

Fail closed if any required evidence path is absent from state—even when the latest task alone passed. This prevents partial batches from reaching H3 while earlier tasks lack logs. Regression scope follows pack policy and [C5.1](C5.1-src-tests-e2e-delivery.md) delivery layout.""",
    "G2.3": """\
Human H3 sign-off stays blocked until `goal.verify_command` exits zero. Passing task-level evidence alone does not set `hitl.pending=H3`; goal verify success transitions `goal.state` through verifying and only then surfaces H3 for operator acceptance.

Automatic H3 clearance on implement completion is forbidden—operators sign verified outcomes, not assumed ones ([INTRO-1.2](INTRO-1.2-human-touchpoint-contract-h1-h2-h3.md)). Failed goal verify packages structured H2 with aggregated log paths; pursuit resumes only after fix and re-run.""",
    "G2.4": """\
Every implement batch ends with regression coverage: after the batch’s task evidence passes, run goal verify (or an intermediate regression slice when pack policy requires) so prior features stay proven before new tasks start. This implements test-before-push at goal cadence, not only at git-workflow time.

Autopilot loops honor the same batch boundary—no stacking implement tasks across batches without regression when `evidence_required` is true. Flaky failures escalate once per [G4.3](G4.3-review-escalation-s4-repeated-verify-fail.md), then H2 with logs attached.""",
    "G3.1": """\
`scripts/validate-workflow.py` is the conformance gate for journal/state shape, required fields, and pursuit invariants. CI and optional pre-push hooks run it so corrupt dual-writes fail before merge, not mid-autopilot.

validate-workflow complements verify-router: the former checks workflow schema and routing consistency; the latter runs product tests. Both are S0-first ([B1.1](B1.1-s0-deterministic-mandatory-first.md)). Failures block continue/autopilot until the conductor repairs state or records an operator exception.""",
    "G3.2": """\
route-tier conformance ensures `next_action`, `capability_class`, `spawn_workers`, and model tier align whenever the conductor changes pursuit direction. `python scripts/route-tier.py --apply` is the canonical apply path; validate-workflow cross-checks tier output against state.json.

Mis-routed genius implement or missing spawn_workers when task cards expect workers is a conformance failure, not a soft warning. Pack role bindings ([B5.2](B5.2-role-to-pipeline-id-skills-tool-permissions.md)) feed expected tier patterns for validation.""",
    "G3.3": """\
`check-pipeline-blocked.py` with goal_autopilot semantics defines when pursuit must stop: human gates (H1/H2/H3), budget exhaustion, corrupt state, and verify regressions. Autopilot and run-local-pipeline consult this script each iteration instead of inferring stop conditions in chat.

Conformance means autopilot cannot override a would-stop result—gates_pending and blocking_questions remain until explicit operator action. Pair with [A2.6](A2.6-loop-until-blocked-budget-achieved-h3-reject.md) and [A4](A4-index.md) stop taxonomy.""",
    "G4.1": """\
Security-review triggers when implement diffs touch auth, crypto, credentials paths, dependency manifests, or other pack-flagged risk surfaces. The reviewer subagent is readonly—findings merge through the conductor, not direct journal writes ([B2.5](B2.5-reviewer-bugbot-security-risk-triggers.md)).

Strict packs may require security-review pass before git-workflow; default self-gate records waivable findings with expiry when automated checks pass. Touch-path detection uses task card declared files plus diff stats, not conductor memory.""",
    "G4.2": """\
Bugbot review triggers on large implement diffs—line-count and file-count thresholds from operator policy or pack overrides. Substantial feature work gets mistake-class scanning before push even when task verify passed, catching logic errors tests may miss.

Bugbot does not replace verify-router evidence; it adds review signal. Failed or blocking Bugbot outcomes route to conductor merge or H2; repeated issues on the same task pattern may enqueue platform promotion ([D2.1](D2.1-index.md)).""",
    "G4.3": """\
Repeated verify failure on the same task card escalates to S4 H2 packaging: attach evidence logs, failure class, retry count, and suggested operator action—never silent retry loops ([B3.3](B3.3-escalation-loop-on-verify-fail.md)). One structured escalation per task before human assist is mandatory.

This review trigger prevents autopilot from burning budget on flaky or mis-specified tests. Conductor records escalation in journal Last failure for rollback and audit ([G6.2](G6.2-rollback-journal-last-failure-structured-h2.md)).""",
    "G4.4": """\
Before merge or program integration, staleness reconciliation must show design artifacts current: `docs/manifest/staleness.json` and reconcile-stale/reconcile-artifact-graph outputs gate git-workflow when upstream HLD, DD, or manifest nodes changed.

Review at merge time catches implement against stale specs—a mistake class mapped in [G5.5](G5.5-mistake-stale-design-staleness-reconcile.md). Conductor runs S0 staleness scripts; workers do not waive merge on stale graph nodes without operator approval.""",
    "G5.1": """\
Hallucinated done is declaring a task or goal complete without evidence files and passed verify—a common agent failure mode. Controls: `evidence_required`, mandatory verify-router runs, validate-workflow checks on `last_verify`, and conductor discipline never marking TODOS complete in prose alone.

Audit and hierarchy quality scripts re-enqueue deepen when queue items close without artifacts. This mistake class is the philosophical core of Plane G: success is demonstrated, not assumed.""",
    "G5.2": """\
Scope creep is editing paths outside `allowed_reads` or beyond the task card boundary—often from workers opening full design trees or “helpful” refactors. Controls: Librarian caps ([B2.2](B2.2-librarian-allowed-reads-catalog-composition.md)), spawn contracts, and conductor merge that rejects out-of-scope diffs.

Task cards list explicit file targets; implement-feature workers must not expand. Violations trigger rework, not silent acceptance; repeated creep may escalate H2 with diff evidence.""",
    "G5.3": """\
Wrong architecture is merging large structural choices without design gate or goal verify coverage—implementing S3 trade-offs as S1 edits. Controls: HLD/DD/feature gates ([A4.1](A4.1-stop-human-h1-h2-h3.md)), self-gate only where policy allows, and goal verify regression that fails when tests or architecture invariants break.

When ambiguity is architectural, stop for S3 conductor decision recorded in journal Q&A or ADR—not economy worker improvisation. Goal verify failure after architectural drift blocks H3 until design and code realign.""",
    "G5.4": """\
Skipped tests is bypassing verify-router or marking tasks done without running the task card Test command—often under token pressure or “tests are slow.” Controls: mandatory verify-router dispatch, evidence path requirements, and git-workflow blocked when `last_verify` is not passed.

Headless and CI paths use the same commands via verify-router/headless-verify.py—no alternate “trust me” path. Skipping is indistinguishable from hallucinated done for audit purposes.""",
    "G5.5": """\
Stale design is implementing against outdated HLD, DD, or integration manifest while staleness graph marks dependents stale. Controls: reconcile-stale skill, reconcile-artifact-graph in program mode, and [G4.4](G4.4-review-staleness-reconciliation-before-merge.md) merge gate.

Upstream vision or spec changes bump staleness; implement must pause or re-run design phases per journal next_action. Silent implement on stale nodes violates compose-first and expert-system integrity.""",
    "G5.6": """\
Duplicate tooling is inventing a second script, skill, or queue handler when catalog or platform queue already provides one—often after skipped compose-first ([B4.3](B4.3-compose-first-catalog-before-improvise.md)). Controls: divergence logs ([B4.4](B4.4-divergence-log-when-not-composing.md)), platform promotion queue, and conformance checks for duplicate command shapes.

New tooling requires catalog entry or promotion item, not ad hoc `scripts/` forks. Duplicate verify or routing scripts confuse route-tier and validate-workflow expectations.""",
    "G5.7": """\
Unsafe commands are shell invocations outside role allowlists—destructive rm, credential exfiltration patterns, or network calls forbidden by pack policy. Controls: preToolUse hooks in `.cursor/hooks.json`, per-role tool permissions from template-pack ([B5.2](B5.2-role-to-pipeline-id-skills-tool-permissions.md)), and conductor rejection of worker-proposed commands not on the task card.

Tool-operator and verifier workers run bounded literal commands only; economy search must not escalate to unapproved system commands. Hook deny is fail-closed with journal note, not silent strip.""",
    "G6.1": """\
Rollback at the git layer uses a branch per goal slice so failed pursue paths can revert without contaminating main or sibling goals. Git-workflow creates and tracks feature branches; goal completion merges only after goal verify and gates clear.

Operator-initiated rollback checks out the last known-good branch tip for that slice; conductor records branch name in journal handoff. Multi-goal company autopilot ([A3.3](A3.3-company-autopilot-multi-goal-role-workstreams.md)) isolates slices to limit blast radius.""",
    "G6.2": """\
Structured `last_failure` in journal and state captures verify regressions, conformance failures, and H2 blockers with goal id, evidence paths, and suggested operator action—enabling resume without re-deriving context. Rollback decisions read this block before rewinding git or resetting next_action.

Empty or vague failure notes violate S4 packaging ([B1.5](B1.5-s4-governance-escalation-h2-packaging.md)). Dual-write failure metadata in the same turn as stop so [G6.3](G6.3-rollback-autopilot-resume-precompact-snapshot.md) snapshots remain trustworthy.""",
    "G6.3": """\
Autopilot resume after session compact or IDE restart reloads preCompact snapshot plus last good dual-write of journal/state.json—never chat memory. Hooks may inject a summary; conductor still reads full journal and Context files before continue.

Snapshot includes next_action, evidence_files, last_verify, gates_pending, and autopilot.active so check-pipeline-blocked reproduces the same stop/continue decision. Corrupt snapshot triggers validate-workflow failure and H2, not best-effort guess.""",
}


def apply_plane_g(out_dir: Path | None = None) -> int:
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from hierarchy_agent_prose import apply_narrative  # noqa: E402
    from hierarchy_completeness import item_id_from_path, list_leaf_paths  # noqa: E402

    base = out_dir or ROOT / "documents/plans/full-automation"
    applied = 0
    for p in list_leaf_paths(base):
        iid = item_id_from_path(p, p.read_text(encoding="utf-8"))
        if iid not in PLANE_G_NARRATIVES:
            continue
        new_text, issues = apply_narrative(p, PLANE_G_NARRATIVES[iid], version="plane-g")
        p.write_text(new_text, encoding="utf-8")
        applied += 1
        if issues:
            print(f"{iid}: {', '.join(issues)}")
    print(f"Applied Plane G agent prose to {applied} leaves")
    return 0


if __name__ == "__main__":
    raise SystemExit(apply_plane_g())
