#!/usr/bin/env python3
"""Agent-authored Reader narratives for Plane B (cognition and routing)."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

PLANE_B_NARRATIVES: dict[str, str] = {
    "B1.1": """\
S0 is the capability class for behavior that already exists as a script under `scripts/`. Before any model improvises routing, validation, dashboard generation, or verify, the conductor must run the deterministic path and use its output.

This rule—mandatory first—prevents expensive re-derivation of state the repo already encodes. `route-tier.py`, `check-pipeline-blocked.py`, and `validate-workflow.py` are canonical S0 examples referenced throughout Plane A pursuit. When a new behavior stabilizes, promote it from S1 worker output to S0 script; do not leave file-derived logic in chat-only form. See [Vision §4 — Branch B](../../full-automation-vision-and-hierarchy.md#4-branch-b-cognition-routing-plane).""",
    "B1.2": """\
S1 covers mechanical work that still needs a model but not genius-tier judgment: bounded code edits from task cards, catalog lookups, shell verification, and bulk search. Economy workers from `model-policy.json` execute S1 under conductor contracts with `allowed_reads` caps.

S1 is the default implement tier when `spawn_workers` is true. Workers must not expand scope, dual-write journal/state, or skip evidence. The catalog in Plane E tells the conductor which worker role fits which task pattern. Mis-routing S3 architecture questions to S1 causes rework; mis-routing S1 mechanical tasks to genius tier wastes cost.""",
    "B1.3": """\
S2 is templated artifact generation: HLD sections, task cards, diagram stubs, and release rows that follow repo templates and skills rather than free-form invention. Skills like hld-writer, dd-writer, and task-breakdown are S2 surfaces—the conductor invokes them when the phase matches, then runs S0 validation on output.

Quality comes from template conformance plus critic passes, not from one-shot prose. S2 outputs feed staleness graphs in Plane E and evidence paths in Plane G. Pack authors extend templates in template-packs; consumer goals should not fork templates ad hoc.""",
    "B1.4": """\
S3 is reserved for architecture ambiguity: trade-offs without a single script answer, merge decisions after parallel workers return, gate interpretation when policy is silent, and reconciliation when design artifacts conflict. The genius-tier conductor owns S3—thin orchestration, not bulk implementation.

When ambiguity is resolvable by reading one fact file or running one script, that is S0 or S1, not S3. S3 turns should end in a recorded decision (journal Q&A or ADR) and updated routing, not open-ended exploration. Escalation to H2 belongs in S4 when external authority is required.""",
    "B1.5": """\
S4 packages governance escalation: structured H2 blockers, waiver requests, legal/finance pack authority, and multi-goal conflict resolution that cannot be self-gated. The conductor formats blockers with goal id, missing artifact, and suggested operator action—never a vague “need help.”

S4 does not mean “use the biggest model for everything.” It means human touchpoint class H2 or policy-mandated review is imminent and the loop must stop cleanly. Pair with [A4.1](A4.1-stop-human-h1-h2-h3.md) stop taxonomy and [A6.2](A6.2-notify-digest-on-h2-blocker-not-every-step.md) notification digest.""",
    "B2.1": """\
The conductor is genius-tier and thin: merge worker summaries, run S0 preflight, choose next_action, spawn workers, and route platform queue drains—it does not implement large task cards inline when `spawn_workers` is true.

Each turn may peek at or drain the platform promotion queue on the interleaved product-and-improvement schedule so self-improvement work advances alongside the current project. After workers finish, only the conductor dual-writes journal and state.json. This role separation is the core of [genius-conductor-tiered-routing.md](../../genius-conductor-tiered-routing.md).""",
    "B2.2": """\
The Librarian is a readonly explore worker that returns `allowed_reads` (max five paths), forbidden expansions, and a suggested worker role before anyone opens full design docs. It reads journal/state.json and INDEX manifests—not the entire tree.

Librarian runs before implement phases and during program orchestration to bound context cost and prevent workers from grep-ing vision monoliths. Output feeds conductor spawn contracts in orchestrate-subagents. Compose-first catalog search ([B4.3](B4.3-compose-first-catalog-before-improvise.md)) complements Librarian for Plane E.""",
    "B2.3": """\
Phase workers implement one skill phase under contract: implement-feature, dd-writer, explore, refactor—each with task card paths, evidence requirements, and no journal writes. The conductor selects the worker type from `next_action` and route-tier output.

Parallel phase workers are allowed only when the integration manifest declares independent lanes; otherwise one worker per turn preserves auditability. Workers return summaries; the conductor merges and verifies before marking progress.""",
    "B2.4": """\
Verifier and tool-operator are shell-class workers for bounded CLI runs: pytest via verify-router, Blender/Unreal export commands, checksum tools—anything with a literal command block on the task card. They write evidence logs under `evidence/` and set `last_verify` in state.

Non-pytest evidence types follow `docs/operator/evidence-types.md`. Verifier failure blocks task completion and may trigger [B3.3](B3.3-escalation-loop-on-verify-fail.md) escalation without clearing gates. Tool-operator never edits product source except via declared tool output paths.""",
    "B2.5": """\
Reviewer workers run on triggers: Bugbot after substantial implement diffs, security-review when policy flags risk, risk-class controls from Plane G. They are readonly with respect to pursuit state—findings go to the conductor for merge or H2.

Review does not replace verify-router evidence; it adds mistake-class detection before push. Strict mode may require reviewer pass before git-workflow; default self-gate records findings as waivable with expiry when automatable checks pass.""",
    "B2.6": """\
Platform workers drain the promotion queue in parallel slots scheduled by Plane D policy—turning repeated one-off reasoning into scripts, playbooks, and pack fragments while product pursuit continues on the main stack.

The conductor assigns economy-tier platform workers with queue item ids; they must not mutate consumer goal scope. Completion updates platform maturity ladders and reconciles staleness for downstream catalog nodes. See [B4.2](B4.2-platform-promotion-queue-peek-drain.md) for peek/drain semantics each K product steps.""",
    "B3.1": """\
Genius-tier models are for orchestration turns only: routing, merge, gate decisions, and spawn planning—not for writing hundreds of lines of feature code. `model-policy.json` maps tiers; route-tier.py applies capability_class S0–S4 to pick worker vs parent model.

Thin genius turns keep cost predictable and preserve worker parallelism. If the conductor implements large task cards inline while spawn_workers is true, that violates this capability and collapses tier economics.""",
    "B3.2": """\
Economy tier handles bulk mechanical work: multi-file search, repetitive refactors scoped to task cards, test fixes with clear stack traces, and catalog indexing. Bulk code search and shell subagents operate under read/write contracts stricter than the conductor’s.

Escalate to S3 when search surfaces architectural conflict or missing facts not in allowed_reads. Economy tier is not “worse quality by default”—it is narrower context and narrower write scope.""",
    "B3.3": """\
When verify fails, an escalation loop runs: capture log, classify failure (test, tool, environment, design), decide retry vs H2 vs refactor task—without silently marking the implement task complete. The conductor owns the loop; workers do not self-clear evidence gates.

Repeated verify failure on the same task card triggers S4 packaging for H2 with evidence paths attached. This prevents infinite implement→fail→implement churn without journal record.""",
    "B3.4": """\
Platform turns combine economy workers with S0 scripts: queue peek, promotion apply, staleness reconcile, and manifest validation run deterministically before any model interprets platform debt.

Product turns remain primary; platform turns interleave on schedule ([SEC-13 pursuit flow](SEC-13-pursuit-flow.md)). Platform workers use the same evidence discipline as product workers but write to platform queue state and pack fragments, not consumer feature branches.""",
    "B4.1": """\
Each product turn executes the current `next_action` task from state.json—one task card, one skill phase—aligned with Plane C pipelines. The conductor does not skip ahead to push or refactor while implement evidence is missing.

Task selection is S0 where scripts exist; otherwise conductor reads state and journal mirror. This capability binds Plane B routing to Plane C execution order so interleaved product and platform scheduling does not desynchronize project progress from recorded next_action.""",
    "B4.2": """\
Platform promotion queue peek/drain runs on a K-step cadence during pursuit: inspect head items, drain ready promotions with S0 scripts, defer blocked items with journal notes. Peek is cheap; drain commits artifacts and updates maturity.

By default the current project step and one self-improvement step from the queue run in turn—delivery does not pause entirely while the system works on itself, unless policy explicitly prioritizes clearing the improvement backlog first. Failed drain surfaces H2 when external repo access or pack authority is missing.""",
    "B4.3": """\
Compose-first requires catalog search before inventing new patterns: INDEX.md, playbooks, existing pack components, and facts files must be consulted and bound in the task or design record. Improvisation without catalog search is a divergence logged in Plane E.

This capability implements the expert-system reuse ladder—ephemeral reasoning should shrink over time as S0 scripts and pack fragments absorb repeated patterns. See [MASTER-E](../full-automation/MASTER-E-branch-e---knowledge---composition-plane.md).""",
    "B4.4": """\
When compose-first cannot find a suitable component, the conductor records a divergence log entry: what was searched, why composition failed, what was invented instead, and promotion candidate id for the platform queue.

Divergence is not failure—it is an audit trail for what was invented instead of reused, feeding future self-improvement work. Silent invention without log blocks pack maturity claims and makes SEC-14 gap analysis untrustworthy. Reviewers may sample divergence logs for duplicate patterns to prioritize promotion.""",
    "B5.1": """\
Active role comes from the instantiated template-pack: developer, operator, platform, legal reviewer—each with default pipeline_id and tool permissions. `state.json` carries active_role so pursuit, spawn policy, and HITL strictness match pack intent.

Switching roles mid-goal requires manifest or conductor decision recorded in journal; workers inherit role context in spawn contracts. Company autopilot ([A3.3](A3.3-company-autopilot-multi-goal-role-workstreams.md)) schedules across roles without merging their permissions.""",
    "B5.2": """\
Role bindings map to pipeline_id, enabled skills, MCP servers, and forbidden paths—encoded in pack schema (Plane F) and mirrored in operator policy overrides. A platform role may run promotion queue skills; a product role may not waive governance gates.

Misconfiguration here is a high-risk blocker: wrong pipeline_id routes implement into design-only phases. Pack authors validate bindings with conformance scripts before publishing pack versions.""",
    "B5.3": """\
Handoff manifest and artifact graph declare cross-workstream dependencies: which design nodes must exist before implement lanes start, which integration tests gate program completion. Program orchestration reads the manifest before parallel spawn ([orchestrate-program skill](../../../.cursor/skills/orchestrate-program/SKILL.md)).

Stale nodes in the graph trigger reconcile-artifact-graph before workers proceed. Handoff is the human-approved integration contract for multi-stream company goals.""",
    "B5.4": """\
The conductor identity persists across role switches; workers swap with fresh allowed_reads and role context per spawn. The conductor does not “become” the implement worker—it merges worker output and maintains single-writer journal/state discipline.

This separation prevents role context bleed (platform worker editing consumer tasks) and keeps H2 packaging centralized in S4. Multi-role company pursuit depends on stable conductor identity with ephemeral worker personas.""",
}


def apply_plane_b(out_dir: Path | None = None) -> int:
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from hierarchy_agent_prose import apply_narrative  # noqa: E402
    from hierarchy_completeness import item_id_from_path, list_leaf_paths  # noqa: E402

    base = out_dir or ROOT / "documents/plans/full-automation"
    applied = 0
    for p in list_leaf_paths(base):
        iid = item_id_from_path(p, p.read_text(encoding="utf-8"))
        if iid not in PLANE_B_NARRATIVES:
            continue
        new_text, issues = apply_narrative(p, PLANE_B_NARRATIVES[iid], version="plane-b")
        p.write_text(new_text, encoding="utf-8")
        applied += 1
        if issues:
            print(f"{iid}: {', '.join(issues)}")
    print(f"Applied Plane B agent prose to {applied} leaves")
    return 0


if __name__ == "__main__":
    raise SystemExit(apply_plane_b())
