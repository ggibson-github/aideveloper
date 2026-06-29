#!/usr/bin/env python3
"""Agent-authored Reader narratives for Plane A groups A3–A6 (autopilot, stops, continue, notify)."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

PLANE_A_REST_NARRATIVES: dict[str, str] = {
    "A3.1": """\
Session autopilot is the in-IDE mode most operators use first: the conductor loops pursuit steps inside one Cursor session until a cap, a block, or goal completion. This capability defines `max_steps_per_session`—a safety valve so a single chat cannot run unbounded turns if preflight mis-reads state or a worker hangs.

The limit is not a product goal; goal autopilot (A3.2) and the SDK daemon (A3.4) lift it for long-running work. When the cap is hit, pursuit dual-writes a structured stop reason and exits cleanly so the next wake—manual Continue or daemon poll—resumes from the last good journal/state snapshot. See [A2.6 loop until blocked](A2.6-loop-until-blocked-budget-achieved-h3-reject.md) for the inner loop this mode wraps.""",
    "A3.2": """\
Goal autopilot is the north-star run mode: after H1 approves a plan, pursuit continues automatically until `goal_verify` passes, a hard block fires, or a budget from [A1.4](A1.4-deadline-budget-steps-tokens-wall-clock.md) is exhausted. Unlike session autopilot, there is no arbitrary per-chat step ceiling—the stop taxonomy in A4 decides termination.

Each iteration still runs exactly one pipeline phase ([A2.2](A2.2-if-ready-execute-one-pipeline-step.md)) after S0 preflight ([A2.1](A2.1-preflight-check-pipeline-blocked-extended.md)). Scope completion triggers goal-level verification ([A2.4](A2.4-goal-scope-complete-run-goal-verify.md)), not another implement task. Operators enable this via `autopilot.active` in state.json or the `/autopilot` skill once the goal model from A1 is populated.""",
    "A3.3": """\
Company autopilot extends single-goal pursuit to a multi-goal queue across roles and workstreams defined by an active template-pack ([Plane F](../full-automation/MASTER-F-branch-f---organization-plane.md)). The scheduler picks the next ready goal—respecting dependencies, platform slots, and role bindings—rather than assuming one `state.json` goal forever.

This mode is how “organizational reliability” scales: product, platform, and ops pursuits interleave without manual tab-switching, while H2 still pauses only the blocked stream. Conductor remains one writer; workers never dual-write journal/state. When one goal reaches H3 pending, others may continue if preflight allows. See [SEC-17.6 decision on multi-goal stacks](SEC-17-6-decision-multi-goal-single-stack-vs-company-autopilot.md) for deployment choices.""",
    "A3.4": """\
The SDK daemon turns goal autopilot into an always-on local worker: `run-local-pipeline.py` polls `state.json`, runs preflight, executes one pursuit step when READY, and sleeps when BLOCKED—24/7 on the operator PC without keeping Cursor open.

This is Plane I runtime integration with Plane A semantics identical to in-IDE autopilot. Requires `cursor-sdk`, `CURSOR_API_KEY`, and a genius-tier model id from operator policy. Laptop sleep or crash recovery depends on Plane H dual-write: the daemon resumes from the last committed state, not from chat memory. Pair with [A6.2](A6.2-notify-digest-on-h2-blocker-not-every-step.md) so operators learn about blockers without watching logs.""",
    "A4.1": """\
Human stop reasons are intentional, policy-driven pauses—not failures. H1 stops pursuit until an approved plan exists; H2 stops until a blocker is resolved (credentials, external access, ambiguous requirement); H3 stops after goal_verify passes until the operator accepts or rejects verified outcomes.

Each stop dual-writes to journal and `hitl` fields in state.json with a typed reason so dashboards and daemons do not guess why the loop exited. Pursuit must never auto-clear H3 or treat silence as approval. This capability is the exhaustive taxonomy entry for touchpoint-class stops—see [INTRO-1.2](INTRO-1.2-human-touchpoint-contract-h1-h2-h3.md) for the contract operators see.""",
    "A4.2": """\
Verification stops protect quality when evidence or goal-level proof fails. Task evidence missing, `verify-router` failure, goal_verify regression, or conformance script exit non-zero all produce a hard stop with structured H2—not a silent retry loop.

Fail-closed behavior prevents false “achieved” states that would reach H3 without proof. The conductor records which command failed and which evidence paths were absent so the operator or a resumed pursuit knows exactly what to fix. This stop class connects Plane A to Plane G; it is distinct from resource exhaustion (A4.3) and integrity corruption (A4.4).""",
    "A4.3": """\
Resource stops bound autonomous pursuit in measurable units: max steps per session or goal, token budgets, cost caps, and lease expiry on shared runners. When a budget is exhausted, pursuit halts with a stop reason that operators can extend at H2 if policy allows.

These limits implement [A1.4](A1.4-deadline-budget-steps-tokens-wall-clock.md) in the stop taxonomy so “always-on” never means “unbounded.” Scheduling in Plane D may reprioritize work when leases expire, but the stop record must remain auditable. Too-tight budgets cause false stops; too-loose budgets waste spend—pack authors set defaults per goal_type.""",
    "A4.4": """\
Integrity stops fire when the harness cannot trust its own state: `validate-workflow.py` fails, state.json is corrupt or schema-invalid, dual-write mismatch between journal and state, or artifact graph references missing nodes. Pursuit must not continue on ambiguous memory.

Recovery is deterministic-first: repair scripts, restore snapshot from Plane H, or escalate H2 with the validation log attached. Continuing pursuit on corrupt state duplicates work or attaches evidence to the wrong goal. This stop class is rare in production but critical for restart safety after manual edits or merge conflicts.""",
    "A4.5": """\
Completion stops are successful termination: goal_verify passed, H3 accepted (or waived under policy), program manifest complete, or company_ops goal criteria satisfied per [INTRO-1.3](INTRO-1.3-goal-completion-criterion.md). The goal state transitions to achieved or program_done with timestamps and evidence pointers.

Unlike H3-pending ([A2.5](A2.5-goal-verify-pass-transition-h3-pending.md)), this stop closes pursuit for that goal id. Multi-goal company autopilot ([A3.3](A3.3-company-autopilot-multi-goal-role-workstreams.md)) may immediately advance to the next queued goal. Operators should see completion on dashboard/STATUS without parsing journals.""",
    "A5.1": """\
“Continue” in the target architecture means resume the pursuit loop if preflight reports READY—not approval of design gates, not answers to open questions, and not permission to skip evidence. Manual `/continue` invokes one step when autopilot is off; daemons invoke the same semantics on poll.

This capability prevents the v2.13 failure mode where operators typed Continue dozens of times per feature. Blocked preflight must re-prompt for H2 assistance instead of advancing `next_action`. See [A5.2](A5.2-continue-not-approval-self-gate-h1-h3-only.md) for what Continue explicitly does not mean.""",
    "A5.2": """\
Continue is not approval. Typing Continue or running `/continue` does not waive HLD, DD, feature design, or manifest gates—those become self-gate plus evidence where automatable, with H1 and H3 remaining the only default human approvals unless strict HITL is enabled.

Misreading Continue as “yes, proceed anyway” reintroduces silent gate skips. The conductor and S0 scripts treat unresolved blocking questions and pending human gates as BLOCKED preflight outcomes. Only explicit approval phrases or recorded waivers in the journal clear design gates.""",
    "A5.3": """\
After H1 approves a plan, the default transition is automatic entry into goal autopilot—no manual “start pursuit” step. The goal-keeper skill (or equivalent conductor path) sets `autopilot.active`, populates goal fields from A1, and runs the first preflight in the same session when possible.

This default encodes “100% automation between touchpoints”: the operator supplies intent once, then observes until H2 or H3. Opt-out remains for strict HITL packs or debugging single steps. Pair with [A3.2](A3.2-goal-autopilot-until-goal-verify-or-hard-block.md) for the run mode entered here.""",
    "A6.1": """\
Notifications inform; they do not block pursuit. Phase completion—design artifact published, implement task verified, goal transition—updates `docs/operator/dashboard.md`, `STATUS.md`, and optional webhooks so operators have situational awareness without approving each step.

Regeneration is S0 where `generate-dashboard.py` exists. Webhooks fire on meaningful milestones, not every token, to avoid alert fatigue. This capability satisfies observability for unattended runs while preserving [A6.3](A6.3-operator-observe-without-unblocking-loop.md): reading STATUS never substitutes for H2 resolution.""",
    "A6.2": """\
H2 blockers deserve prompt, consolidated notification; routine pursuit steps do not. This capability defines digest-style alerts on blocker detection—structured reason, goal id, suggested operator action—rather than per-step pings that train operators to ignore the channel.

The pursuit loop continues to dual-write blockers to journal/state; notification is an Plane I integration layer. Pair with session and daemon modes (A3) so unattended runs surface only actionable interruptions. Every-step notifications violate the minimal-HITL contract and recreate babysitting by another name.""",
    "A6.3": """\
Operators may inspect dashboards, journals, evidence logs, and queue depth while pursuit remains blocked without that inspection counting as “unblocking.” Read-only observation must not clear H2, advance `next_action`, or waive gates.

This separation prevents accidental resume when an operator opens STATUS to diagnose a failure. Explicit unblock actions—supplying credentials, answering a blocking question, approving H3—are distinct events recorded in journal Q&A. Autonomous loops remain paused until preflight passes on the actual fix.""",
}


def apply_plane_a_rest(out_dir: Path | None = None) -> int:
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from hierarchy_agent_prose import apply_narrative  # noqa: E402
    from hierarchy_completeness import item_id_from_path, list_leaf_paths  # noqa: E402

    base = out_dir or ROOT / "documents/plans/full-automation"
    applied = 0
    for p in list_leaf_paths(base):
        iid = item_id_from_path(p, p.read_text(encoding="utf-8"))
        if iid not in PLANE_A_REST_NARRATIVES:
            continue
        new_text, issues = apply_narrative(p, PLANE_A_REST_NARRATIVES[iid], version="plane-a")
        p.write_text(new_text, encoding="utf-8")
        applied += 1
        if issues:
            print(f"{iid}: {', '.join(issues)}")
    print(f"Applied Plane A (A3-A6) agent prose to {applied} leaves")
    return 0


if __name__ == "__main__":
    raise SystemExit(apply_plane_a_rest())
