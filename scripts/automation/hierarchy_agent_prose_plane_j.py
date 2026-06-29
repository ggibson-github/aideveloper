#!/usr/bin/env python3
"""Agent-authored Reader narratives for Plane J (governance & operator)."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

PLANE_J_NARRATIVES: dict[str, str] = {
    "J1": """\
`docs/operator/model-policy.json` defines genius and economy tier Cursor model lists, autopilot defaults, spawn_workers policy, and capability_class routing hints. Operators update tiers as models evolve—fixed model names are not hardcoded in skills or rules.

route-tier.py reads policy plus state to set model_tier each turn ([B3.1](B3.1-genius-orchestration-only-thin-turns.md)). SDK and IDE runtimes share the same policy file ([I2.2](I2.2-runtime-sdk-cursor-api-key-autopilot-model.md)). Policy changes should run validate-workflow.py before unattended autopilot resumes. See [Vision §12](../../full-automation-vision-and-hierarchy.md#12-branch-j-governance-operator-plane).""",
    "J2": """\
`docs/decisions/automation-waivers.md` records time-bounded exceptions to default automation rules—skipped verify suites, deferred gates, manual push approvals—with operator, rationale, expiry, and affected goal ids. Waivers are not silent overrides in chat.

Expired waivers revert to strict behavior; pursuit must re-check preflight before continuing. Self-gate middle approvals may be waivable when automatable evidence exists ([A5.2](A5.2-continue-not-approval-self-gate-h1-h3-only.md)); H3 subjective sign-off is never permanently waived without explicit policy. Audit links waivers in [J4](J4-audit.md).""",
    "J3": """\
`strict_hitl` mode in state.json hitl block forces explicit human clearance for gates that default self-gate would auto-pass with evidence. Enable for regulated environments, external-audit programs, or operator preference during early pack rollout.

When strict_hitl is true, continue and autopilot stop at every pending H1/H2/H3 until journal records explicit approval phrases—observation alone does not unblock ([A6.3](A6.3-operator-observe-without-unblocking-loop.md)). Pack defaults may set strict_hitl per role ([H1.5](H1.5-state-hitl-block.md)).""",
    "J4": """\
Audit trail governance spans worker-runs.jsonl ([H5](H5-worker-runs.md)), evidence/ immutability ([H4](H4-evidence.md)), journal Resolved Q&A, waiver registry ([J2](J2-automation-waivers.md)), and export-contract snapshots for external review.

Operators query audit paths to reconstruct who spawned which worker, what verify ran, and which gates cleared. Tamper-evident logs support post-incident review; conductors must not truncate audit history without documented retention policy. CI and headless runs append to the same trails ([I3](I3-index.md)).""",
    "J5": """\
`docs/operator/export-contract.md` defines what pursuit state, evidence bundles, and dashboard artifacts may leave the repo boundary—fields redacted, formats required, and approval needed for external sharing. Export scripts follow the contract; ad-hoc copy/paste of state.json is discouraged.

Pack authors extend export profiles per company template. Export for H3 sign-off packages may include goal_verify evidence rollup ([C3.4](C3.4-task-to-goal-rollup-percent-goal-verify.md)). Contract violations surface H2 before data leaves controlled storage.""",
    "J6": """\
`docs/automation/release-queue.json` tracks harness evolution rows—v2.14 through v2.23 SEC-15 capabilities—with implement status, verify commands, and waiver links. It is the operator-facing backlog for platform maturity separate from consumer product goals.

Release queue drain promotes S0 scripts, skills, and pack fragments when rows ship; stale rows re-enqueue via hierarchy-expander audit. Pair with platform promotion_queue in state ([H1.3](H1.3-state-platform-block.md)) and SEC-15-index release checklist. Completed rows update dashboard maturity indicators ([I5.1](I5.1-runtime-notify-status-dashboard-generation.md)).""",
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


def apply_plane_j(out_dir: Path | None = None) -> int:
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from hierarchy_agent_prose import apply_narrative  # noqa: E402

    base = out_dir or ROOT / "documents/plans/full-automation"
    id_paths = _resolve_id_paths(base, set(PLANE_J_NARRATIVES))
    applied = 0
    for iid, narrative in PLANE_J_NARRATIVES.items():
        p = id_paths.get(iid)
        if p is None:
            print(f"{iid}: no markdown path found")
            continue
        new_text, issues = apply_narrative(p, narrative, version="plane-j")
        p.write_text(new_text, encoding="utf-8")
        applied += 1
        if issues:
            print(f"{iid}: {', '.join(issues)}")
    print(f"Applied Plane J agent prose to {applied}/{len(PLANE_J_NARRATIVES)} documents")
    return 0


if __name__ == "__main__":
    raise SystemExit(apply_plane_j())
