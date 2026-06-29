#!/usr/bin/env python3
"""Pilot agent-authored Reader narratives (A1 goal model + A2 pursuit loop)."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

PILOT_NARRATIVES: dict[str, str] = {
    "A1.1": """\
Every pursuit in the expert system begins with a goal record that can be found again after restarts, nested under the right parent, and classified by type. This capability defines the three identity fields that make that possible: a unique goal_id, an optional parent_goal for tree structure, and goal_type (app, feature, milestone, or company_ops).

The type enum is not cosmetic. It tells preflight, routing, and verification which contracts apply—a milestone goal may require manifest approval while a feature goal binds to task cards and evidence paths. Nesting via parent_goal lets a program decompose into parallel streams without losing roll-up status at H3.

Operators set these fields at H1 when approving a plan; afterward the conductor and S0 scripts maintain them through dual-write to journal and state.json. If identity drifts (duplicate ids, wrong parent), pursuit turns attach evidence to the wrong scope and goal_verify cannot succeed. See [Vision §3 — Branch A](../../full-automation-vision-and-hierarchy.md#3-branch-a-pursuit-control-plane) for how the goal model anchors Plane A.""",
    "A1.2": """\
A goal that cannot be checked mechanically is not a goal the system can pursue autonomously. This capability requires success_criteria that scripts or tests can evaluate—clear predicates, exit codes, or artifact checks—not subjective “looks good” language.

Success criteria are the bridge between intent (approved at H1) and [goal verification](A1.3-goal-verify-command-meta-test.md). Each criterion should map to a command, file presence, or metric the verifier can run without asking a human. Vague criteria force H2 blockers and stall the always-on loop.

When criteria change mid-pursuit, the conductor must dual-write the update and re-run preflight so downstream steps do not assume an obsolete definition of done. Poor criteria are a common root cause of false “achieved” states; this spec exists to prevent that class of failure.""",
    "A1.3": """\
Task-level tests prove a step ran; goal-level verification proves the entire pursuit succeeded. This capability defines goal_verify_command—the meta-test that runs when scope is complete and must pass before the system requests H3 sign-off.

The command is typically a wrapper (for example `python scripts/goal-verify.py`) that aggregates checks across criteria, evidence logs, and conformance scripts. It is stricter than a single pytest file: failing goal_verify blocks transition to H3 pending even if individual tasks passed.

Designers should treat goal_verify as the contract between Plane A (pursuit) and Plane G (verification). Without it, operators would manually reconcile journals—a violation of the 100% automation scope except at H1, H2, and H3.""",
    "A1.4": """\
Autonomous pursuit without bounds can consume unbounded tokens, steps, and wall-clock time. This capability defines deadline and budget fields—steps, tokens, wall clock—so the loop can stop cleanly with a recorded reason instead of running indefinitely.

Budgets are enforced at preflight and after each turn. When a budget is exhausted, pursuit stops, dual-writes a structured stop reason, and surfaces H2 only if human intervention can extend the budget. Deadlines align with operator expectations for time-sensitive milestones.

These fields turn “always-on” into “always-on until provably done or bounded.” They also inform Plane D scheduling so self-improvement work stays bounded and does not displace the current project goal. Incorrect budget configuration is an operational edge case: too tight causes false stops; too loose wastes resources.""",
    "A1.5": """\
Operators and dashboards need a single, honest lifecycle state for each goal. This capability defines the goal state enum: pursuing, blocked, verifying, achieved, and rejected—transitions driven by preflight, step execution, goal_verify, and H3 outcomes.

The enum prevents ambiguous records such as “done” without verification or “in progress” while H3 is pending. Blocked correlates with H2 assistance; verifying means scope is complete and goal_verify is running; rejected captures H3 denial with notes so pursuit can resume with corrected criteria.

State must stay synchronized across journal/progress.md and state.json. Resume after laptop sleep or daemon restart relies on this enum being authoritative. See the A2 pursuit loop for when each transition fires in sequence.""",
    "A2.1": """\
Every pursuit turn starts with a question: is it safe to act? This capability extends preflight via `check-pipeline-blocked.py` so the conductor never executes a pipeline step while gates, blockers, budgets, or missing evidence would make that step invalid.

Exit code semantics are strict: READY (0) means exactly one skill phase may run; BLOCKED (1) means stop, dual-write a structured H2 or stop reason, and do not advance next_action. Preflight is S0—deterministic, cheap, and mandatory before any model-heavy work ([B1.1 S0 rule](../full-automation/B1.1-s0-deterministic-mandatory-first.md)).

Skipping preflight is how autonomous systems waste tokens on work that cannot commit. This step is the first node in the A2 pursuit loop and re-runs after every completed turn.""",
    "A2.2": """\
When preflight reports READY, the system executes exactly one pipeline skill phase—never a batch of design, implement, and verify in a single turn. This capability encodes that discipline so evidence, routing, and journal entries stay aligned with a single next_action.

One step per turn preserves auditability: each wake cycle produces one ledger entry, one evidence slot, and one dual-write. It also prevents partial state where implement ran but verify did not. The conductor reads next_action from state.json, invokes the matching skill, and stops.

This is the operational heart of “continue means one step,” redefined in Plane A. Violating one-step semantics breaks autopilot loops and makes H2 recovery ambiguous.""",
    "A2.3": """\
After a step completes, the system must re-route capability tier, persist results, and advance counters before the next preflight. This capability covers post-step housekeeping: route-tier.py, dual-write to journal and state, and increment pursuit counters (steps, tokens, wall clock).

Post-step work is still S0 where scripts exist. It ensures the next wake sees updated next_action, model_tier, and budget fields. Missing dual-write here is a critical failure mode—resume after crash would repeat or skip work.

This step closes the turn opened by A2.2 and prepares A2.1 to run again on fresh state.""",
    "A2.4": """\
When all in-scope work for the goal is complete, pursuit shifts from step execution to goal-level proof. This capability defines the handoff: detect scope completion, then run goal_verify_command rather than another implement task.

Scope completion is machine-checkable—queue empty, task cards done, evidence present—not a conductor guess. Running goal_verify too early produces false failures; running it never leaves goals stuck in pursuing forever.

This node connects Plane A to Plane G. It is the pivot from “doing work” to “proving the goal.” Operators should expect a visible state transition to verifying before H3 is requested.""",
    "A2.5": """\
Passing goal_verify is necessary but not sufficient for closure. This capability defines transition to H3 pending: verification succeeded, human final sign-off is required, and the goal state reflects verifying → awaiting H3.

The system notifies the operator; it does not block the world indefinitely unless strict HITL mode demands it. H3 is the third human touchpoint—accept or reject verified outcomes. Rejection returns the goal to pursuing with structured notes.

Automating everything except H3 is the INTRO contract; this step enforces that boundary in the pursuit loop.""",
    "A2.6": """\
Pursuit is a loop, not a single shot. This capability states the termination conditions: continue looping through preflight → step → post-step until blocked, budget exhausted, goal achieved, or H3 rejected.

Each iteration is bounded by A2.1–A2.5. The loop may run in IDE autopilot, local SDK daemon, or headless CI depending on Plane I runtime—but the control flow is identical.

Without an explicit loop spec, implementers build ad-hoc while-loops that diverge across runtimes. This document is the canonical cycle for always-on operation.""",
    "A2.7": """\
Earlier automation models asked humans to type “continue” after every step. This capability forbids intermediate wait-for-continue: the loop runs autonomously between H1, H2, and H3 touchpoints.

“Continue” in operator language now means one pipeline step when manually invoked—not a prompt between every phase inside autopilot. That redefinition is what makes 100% automation between touchpoints achievable.

Confusion here causes products to re-introduce manual babysitting. This spec is the guardrail against regressing to burst-and-wait workflows.""",
}


def apply_pilot(out_dir: Path | None = None) -> int:
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from hierarchy_agent_prose import apply_narrative  # noqa: E402
    from hierarchy_completeness import item_id_from_path, list_leaf_paths  # noqa: E402

    base = out_dir or ROOT / "documents/plans/full-automation"
    applied = 0
    for p in list_leaf_paths(base):
        iid = item_id_from_path(p, p.read_text(encoding="utf-8"))
        if iid not in PILOT_NARRATIVES:
            continue
        new_text, issues = apply_narrative(p, PILOT_NARRATIVES[iid], version="pilot")
        p.write_text(new_text, encoding="utf-8")
        applied += 1
        if issues:
            print(f"{iid}: {', '.join(issues)}")
    print(f"Applied agent pilot prose to {applied} leaves")
    return 0


if __name__ == "__main__":
    raise SystemExit(apply_pilot())
