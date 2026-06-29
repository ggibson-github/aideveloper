#!/usr/bin/env python3
"""Agent-authored Reader narratives for Plane H (persistence & state)."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

PLANE_H_NARRATIVES: dict[str, str] = {
    "H1.1": """\
The v2 machine router in `journal/state.json` carries legacy pursuit fields—`next_action`, `program`, `autopilot`, `evidence_required`, `model_tier`, `spawn_workers`—that route-tier.py and validate-workflow.py read every turn. These top-level keys remain the conductor's first S0 lookup before any LLM interprets progress.

Additive v2 blocks (goal, platform, pursuit, hitl, company) extend without breaking existing consumers; sync-state.py and journal-keeper dual-write both files atomically where possible. Corrupt or partial state triggers [A4.4](A4.4-stop-integrity-validate-workflow-state-corrupt.md) stop. See [APP-B-state-json-sketch](APP-B-state-json-sketch.md) and [Vision §10](../../full-automation-vision-and-hierarchy.md#10-branch-h-persistence-state-plane).""",
    "H1.2": """\
The goal block records goal id, parent goal, goal type, success criteria, verify command, budget counters, and state enum (pursuing, blocked, verifying, achieved, rejected). Goal-verify is the terminal gate—pursuit loops until `goal_verify` passes or H3 rejects per [A2.4](A2.4-goal-scope-complete-run-goal-verify.md).

Machine-checkable success criteria bind to evidence paths in Plane G; subjective criteria remain H3. Company autopilot schedules multiple goal blocks without merging their scopes ([A3.3](A3.3-company-autopilot-multi-goal-role-workstreams.md)). Only the conductor writes goal transitions after verify evidence.""",
    "H1.3": """\
The platform block tracks promotion_queue head, drain counters, maturity ladders, and platform-turn scheduling separate from consumer product pursuit. Platform workers read this block; product workers must not mutate it except via conductor-orchestrated drain ([B4.2](B4.2-platform-promotion-queue-peek-drain.md)).

Queue JSON lives under docs/automation/ with S0 peek/drain scripts; stale platform items defer with journal notes rather than silent drop. Platform idle drain when product waits on external H2 is [D3.4](D3.4-idle-drain-when-product-waits-external-h2.md). Dual-write updates platform counters alongside journal Platform section.""",
    "H1.4": """\
The pursuit block captures mode (continue, goal_autopilot, company_autopilot), step counters, capability_class, last_verify, evidence_files, and gates_pending. Autopilot loops increment steps_total until check-pipeline-blocked stops ([A3.1](A3.1-session-autopilot-max-steps-per-session.md), [A3.2](A3.2-goal-autopilot-until-goal-verify-or-hard-block.md)).

`last_verify: passed` is mandatory before advancing past implement tasks when evidence_required is true ([G4](G4-evidence-required.md)). gates_pending holds HLD/DD/feature design waits—continue does not clear them ([A5.2](A5.2-continue-not-approval-self-gate-h1-h3-only.md)). route-tier.py applies tier changes when next_action shifts.""",
    "H1.5": """\
The hitl block records pending human touchpoint class: H1 plan approval, H2 blocker, H3 sign-off—or null when pursuit is unblocked. Payload carries structured reason, goal id, missing artifact, and suggested operator action per [INTRO-1.2](INTRO-1.2-human-touchpoint-contract-h1-h2-h3.md).

Strict mode ([J3](J3-strict-hitl.md)) forces explicit clearance; default self-gate allows automatable middle gates with evidence. Observation without unblock is [A6.3](A6.3-operator-observe-without-unblocking-loop.md). Notifications on H2/H3 only pair with [I5.2](I5.2-runtime-notify-webhook-email-h2-h3-only.md)—not every pursuit step.""",
    "H1.6": """\
The company block binds pack_id, active_role, template-pack version, and multi-goal workstream leases for company autopilot. Role switches mid-goal require journal-recorded conductor decision ([B5.1](B5.1-active-role-from-template-pack.md)); workers inherit role permissions from pack schema ([B5.2](B5.2-role-to-pipeline-id-skills-tool-permissions.md)).

Integration manifest and artifact graph refs live here for program mode ([C4](C4-index.md)). pack_id null means default repo harness; instantiated packs override pipeline_id and verify suites per [F1](F1-index.md). Company block must stay consistent with journal Company section on dual-write.""",
    "H2": """\
`journal/progress.md` is the human-readable mirror of machine state—not a second router. It records phase completions, Resolved Q&A, Open questions, Blockers, Evidence files, Context files, Session summary, and Next action in prose operators can skim without parsing JSON.

Only the conductor dual-writes after each pipeline step via journal-keeper; workers return summaries but never edit the journal. Hooks inject journal summary on continue/start ([I1.4](I1.4-runtime-ide-hooks-beforesubmit-subagentstart-pretooluse-prec.md)) but agents must still read the full file. STATUS.md and dashboard.md are generated views ([I5.1](I5.1-runtime-notify-status-dashboard-generation.md)), not authoritative pursuit state.""",
    "H3": """\
Artifact graphs declare dependency edges between design nodes, task cards, pack fragments, and integration manifest entries—program mode reads the graph before parallel spawn ([B5.3](B5.3-handoff-manifest-artifact-graph.md), [C4.4](C4.4-artifact-graph-per-program-and-pack.md)).

reconcile-artifact-graph marks nodes stale when upstream changes; reconcile-stale plans re-runs ([E5.1](E5.1-staleness-design-graph-staleness-json.md)). Graph state persists in state.json program block and docs/manifest/staleness.json. Workers must not proceed on stale manifest nodes without conductor reconcile approval.""",
    "H4": """\
The `evidence/` directory holds immutable verify logs—pytest output, tool runs, checksums—written by verify-router.py or verifier shell workers before tasks complete. state.json `evidence_files` and journal Evidence files mirror paths for audit.

Non-pytest evidence types follow `docs/operator/evidence-types.md` ([I4.3](I4.3-runtime-external-evidence-types-non-pytest.md)). Evidence is append-only; failed verify retains logs for escalation ([B3.3](B3.3-escalation-loop-on-verify-fail.md)). Push and git-workflow require last_verify passed or documented journal exception per evidence-required rule.""",
    "H5": """\
`worker-runs.jsonl` append-only audit records each subagent spawn: role, model_tier, allowed_reads, task id, timestamps, and outcome summary. The conductor logs spawns; workers do not self-log journal/state changes.

Audit trail supports cost review, debugging scope bleed, and [J4](J4-audit.md) governance queries. Parallel program lanes produce interleaved lines—correlate by goal id and lane lease ([C4.1](C4.1-workstreams-lane-json-leases.md)). Retention policy belongs in operator pack; default keeps full session history locally.""",
    "H6": """\
Snapshots capture pursuit state before context compaction or session handoff—preCompact hook triggers sync-state.py to write timestamped snapshot files alongside live journal/state.json ([I1.4](I1.4-runtime-ide-hooks-beforesubmit-subagentstart-pretooluse-prec.md)).

Recovery resumes from last good dual-write if operator closes mid-loop; snapshots are recovery aids, not the primary router. SDK daemon and headless runs use the same snapshot contract ([I2.1](I2.1-runtime-sdk-run-local-pipeline-goal-autopilot.md)). validate-workflow.py rejects corrupt state before autopilot continues.""",
}


def _resolve_id_paths(base: Path, narrative_ids: set[str]) -> dict[str, Path]:
    from hierarchy_completeness import item_id_from_path  # noqa: E402

    resolved: dict[str, Path] = {}
    for p in sorted(base.glob("*.md")):
        iid = item_id_from_path(p, p.read_text(encoding="utf-8"))
        if iid not in narrative_ids:
            continue
        prev = resolved.get(iid)
        if prev is None:
            resolved[iid] = p
        elif prev.name.endswith("-index.md") and not p.name.endswith("-index.md"):
            resolved[iid] = p
    return resolved


def apply_plane_h(out_dir: Path | None = None) -> int:
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from hierarchy_agent_prose import apply_narrative  # noqa: E402

    base = out_dir or ROOT / "documents/plans/full-automation"
    id_paths = _resolve_id_paths(base, set(PLANE_H_NARRATIVES))
    applied = 0
    for iid, narrative in PLANE_H_NARRATIVES.items():
        p = id_paths.get(iid)
        if p is None:
            print(f"{iid}: no markdown path found")
            continue
        new_text, issues = apply_narrative(p, narrative, version="plane-h")
        p.write_text(new_text, encoding="utf-8")
        applied += 1
        if issues:
            print(f"{iid}: {', '.join(issues)}")
    print(f"Applied Plane H agent prose to {applied}/{len(PLANE_H_NARRATIVES)} documents")
    return 0


if __name__ == "__main__":
    raise SystemExit(apply_plane_h())
