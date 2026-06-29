#!/usr/bin/env python3
"""Agent-authored Reader narratives for Plane I (runtime & integration)."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

PLANE_I_NARRATIVES: dict[str, str] = {
    "I1.1": """\
The in-IDE conductor session is genius-tier and thin: the operator selects the orchestration model once per session from `docs/operator/model-policy.json`, then the parent agent runs S0 preflight, spawns economy workers, and dual-writes journal/state—never bulk-implementing when spawn_workers is true.

This is the primary runtime for v2 pursuit: continue, autopilot, gate, and verify commands all assume a Cursor IDE session with AGENTS.md and rules loaded. See [genius-conductor-tiered-routing.md](../../genius-conductor-tiered-routing.md) and [Vision §11](../../full-automation-vision-and-hierarchy.md#11-branch-i-runtime-integration-plane).""",
    "I1.2": """\
Local subagents run as economy-tier Task/explore/shell workers under conductor contracts with capped allowed_reads. The IDE runtime spawns them via orchestrate-subagents; workers return summaries without touching journal or state.json.

Parallel local subagents are allowed only when integration manifest declares independent lanes ([C4.2](C4.2-orchestrate-program.md)). Model tier comes from route-tier.py output, not ad-hoc per spawn. Failed worker runs log to [H5](H5-worker-runs.md) audit trail.""",
    "I1.3": """\
Slash commands—/continue, /autopilot, /status, /gate, /task, /verify, /lane, /program—map to skills in `.cursor/skills/` and inject deterministic behavior before the LLM turn. Commands are the operator's control surface; they do not substitute for H2 answers or H3 approval.

/continue performs exactly one pipeline step; /autopilot loops until check-pipeline-blocked ([A3](A3-index.md)). Command definitions live under `.cursor/commands/` and must stay aligned with skill contracts. SDK and headless runners invoke equivalent script entry points ([I2.1](I2.1-runtime-sdk-run-local-pipeline-goal-autopilot.md)).""",
    "I1.4": """\
Cursor hooks—beforeSubmit, subagentStart, preToolUse, preCompact—inject journal summary, state snapshot, and context files on continue/start and trigger sync-state snapshots before compaction. Hooks are S0-thin scripts referenced from `.cursor/hooks.json`.

Failed hook injection surfaces H2 when state.json is corrupt. preCompact pairs with [H6](H6-snapshots.md) snapshot writes. Hooks complement always-on rules ([E4.1](E4.1-context-always-on-rules-agents-md.md)) but do not replace reading journal/progress.md per continue skill.""",
    "I2.1": """\
`scripts/automation/run-local-pipeline.py` is the SDK/local daemon entry for goal_autopilot—repeated continue steps without manual /continue, using the same journal/state contract as IDE pursuit ([A3.4](A3.4-sdk-daemon-run-local-pipeline-24-7.md)).

The daemon runs S0 check-pipeline-blocked before each iteration and stops on gates, budget exhaustion, or integrity failures. It spawns Cursor agents or SDK equivalents per model-policy; unattended 24/7 operation still respects H2/H3 stops. Pair with worker-runs audit ([H5](H5-worker-runs.md)).""",
    "I2.2": """\
SDK runtime requires `CURSOR_API_KEY` and optional `AUTOPILOT_MODEL` override for headless or remote worker sessions. Secrets never commit to repo; operators configure via environment or local secrets store documented in facts INDEX.

Model override must still conform to model-policy.json tier mapping—daemon does not bypass genius/economy routing for conductor vs worker roles. Missing credentials produce structured H2 with setup instructions, not silent fallback to unauthenticated calls.""",
    "I2.3": """\
Operator PC as worker server extends SDK daemon: a dedicated machine drains work-order lanes, runs verify suites, or hosts GPU/tool workloads while the conductor IDE session stays thin. Lease semantics follow [C4.1](C4.1-workstreams-lane-json-leases.md) lane JSON.

Network partition between conductor and worker server triggers H2 with last-known lease state—workers must not assume conductor is reachable for journal writes. Evidence and logs write to shared evidence/ paths or sync back on completion.""",
    "I3.1": """\
`scripts/headless-verify.py` runs verify-router and validate-workflow without an IDE session—used locally and as the pattern for CI verify steps. Headless mode reads state.json and task cards from disk; it does not spawn conductor LLM turns unless explicitly configured.

Output writes to evidence/ with the same immutability contract as IDE verifier ([H4](H4-evidence.md)). Failures set last_verify failed in state for conductor resume on next IDE session.""",
    "I3.2": """\
GitHub Actions (or equivalent CI) runs validate-workflow.py and headless-verify on pull requests—deterministic gates before merge without human babysitting each test. CI does not clear H3 sign-off or design gates in state.json; it validates repo conformance and task evidence where configured.

Workflow definitions should mirror local verify commands from task cards and pack verify suites ([F1.8](F1.8-pack-verify-suites.md)). CI failure comments link to evidence logs; passing CI is necessary but not sufficient for goal_verify.""",
    "I3.3": """\
Headless lane workers pull ready work orders from lane JSON when leases expire or slots open—complete-work-order scripts mark lane progress without IDE conductor presence ([C3.2](C3.2-work-orders-parallel-lanes.md)).

Pull-ready semantics require integration manifest approval and unblocked dependencies in artifact graph ([H3](H3-artifact-graphs.md)). Headless lanes dual-write outcomes to journal/state via S0 scripts only; LLM workers return artifacts to queue for conductor merge.""",
    "I4.1": """\
External MCP servers—browser automation, DCC tools, cloud APIs—extend worker capability per pack configuration. MCP tools appear in worker spawn contracts with explicit permission boundaries; the conductor approves which servers are active for active_role ([B5.2](B5.2-role-to-pipeline-id-skills-tool-permissions.md)).

Auth failures and rate limits surface H2 with credential pointers in facts INDEX. MCP is integration runtime, not pursuit router—state transitions remain conductor-owned. Browser MCP follows lock/navigate/unlock discipline to avoid rabbit-hole automation.""",
    "I4.2": """\
Tool-operator shell workers execute literal Tool command blocks from task cards—Blender batch exports, Unreal commandlet runs, custom CLIs—writing outputs only to declared paths. tool-operator skill bounds writes; product source edits happen only via normal implement workers.

Tool failures attach logs to evidence/ and trigger verify escalation ([B2.4](B2.4-verifier-tool-operator-evidence.md)). Pack authors declare tool patterns in task card templates; ad-hoc tool invocation without card binding is forbidden during evidence-gated implement.""",
    "I4.3": """\
Non-pytest evidence types—checksum files, screenshot paths, export manifests, linter reports—follow `docs/operator/evidence-types.md` so verify-router and headless-verify accept them alongside test logs. Task cards declare evidence type explicitly.

Mixed evidence bundles reference all paths in state evidence_files and journal Evidence files ([H4](H4-evidence.md)). Operators extending evidence types update the manifest and add S0 validation where machine-checkable.""",
    "I5.1": """\
STATUS.md and `docs/operator/dashboard.md` regenerate from state.json and staleness manifest via generate-dashboard skill—S0 where script exists. Dashboards inform operators; they do not unblock pursuit ([A6.3](A6.3-operator-observe-without-unblocking-loop.md)).

Session end and phase completion trigger regeneration in journal-keeper. Dashboard rows link to goal id, next_action, blockers, and evidence status for at-a-glance resume without opening full journal.""",
    "I5.2": """\
Optional webhook and email notifications fire on H2 blocker detection and H3 sign-off events only—not every pursuit step ([A6.2](A6.2-notify-digest-on-h2-blocker-not-every-step.md)). Payloads carry structured blocker reason, goal id, and suggested operator action.

Notification failure must not block pursuit; missed alerts are recoverable from journal Blockers section. Strict environments may disable outbound notify entirely; observation remains via dashboard ([I5.1](I5.1-runtime-notify-status-dashboard-generation.md)).""",
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


def apply_plane_i(out_dir: Path | None = None) -> int:
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from hierarchy_agent_prose import apply_narrative  # noqa: E402

    base = out_dir or ROOT / "documents/plans/full-automation"
    id_paths = _resolve_id_paths(base, set(PLANE_I_NARRATIVES))
    applied = 0
    for iid, narrative in PLANE_I_NARRATIVES.items():
        p = id_paths.get(iid)
        if p is None:
            print(f"{iid}: no markdown path found")
            continue
        new_text, issues = apply_narrative(p, narrative, version="plane-i")
        p.write_text(new_text, encoding="utf-8")
        applied += 1
        if issues:
            print(f"{iid}: {', '.join(issues)}")
    print(f"Applied Plane I agent prose to {applied}/{len(PLANE_I_NARRATIVES)} documents")
    return 0


if __name__ == "__main__":
    raise SystemExit(apply_plane_i())
