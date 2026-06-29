#!/usr/bin/env python3
"""Agent-authored Reader narratives for Plane D (platform evolution)."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

PLANE_D_NARRATIVES: dict[str, str] = {
    "D1.1": """\
L0 is the bottom rung of the promotion ladder: reasoning that lives only in the current agent turn—useful once, not yet captured as a reusable artifact. Every pursuit session starts here for novel problems; the platform queue exists so repeated L0 patterns can graduate upward instead of being re-derived every sprint.

L0 work is legitimate product progress but a liability for scale. When the same manual sequence, explanation, or routing choice appears twice, enqueue a promotion item with target_level above L0. Pair with [D2.1 enqueue triggers](D2.1-index.md) and [Vision §6 — Branch D](../../full-automation-vision-and-hierarchy.md#6-branch-d-platform-evolution-plane-parallel-queue) for the parallel-queue model.""",
    "D1.2": """\
L1 promotes distilled procedure into `docs/playbooks/<slug>.md`: step lists, constraints, and pointers that humans and agents can follow without re-reading full design monoliths. Playbook-keeper skill ([D4.1](D4.1-platform-work-playbook-keeper.md)) is the primary platform worker for L1 creation from divergence logs and task post-mortems.

An L1 playbook is not a script—it encodes intent and ordering while leaving file-derived steps to future L2 extraction. INDEX rows and task-card references ([D6.1](D6.1-platform-done-catalog-index-row.md), [D6.3](D6.3-platform-done-task-card-references.md)) prove the playbook is discoverable. Stale upstream design should bump dependents via Plane E staleness, not silent drift.""",
    "D1.3": """\
L2 moves repeatable behavior into S0 scripts under `scripts/`: deterministic, testable, and mandatory-first per [B1.1](B1.1-s0-deterministic-mandatory-first.md). Script extraction ([D4.2](D4.2-platform-work-script-extraction.md)) promotes playbook steps that no longer need model judgment—routing, validation, queue peek, verify dispatch.

Each L2 artifact needs a unit test path and, when it replaces manual verify, a verify-router hook ([D6.2](D6.2-platform-done-verify-script-l2.md)). The conductor runs scripts before improvising; workers must not re-implement script logic in chat. Failed promotion leaves the queue item open with H2 packaging, not a false done mark.""",
    "D1.4": """\
L3 wraps orchestration into Cursor skills and slash commands under `.cursor/skills/` and `.cursor/commands/`: bounded prompts, allowed tool sets, and phase entry points the conductor invokes by name. Skills sit above scripts—they compose S0 calls and journal-keeper behavior rather than replacing them.

Platform work type [D4.3](D4.3-platform-work-skill-command-wrapper.md) produces L3 wrappers from stabilized playbooks. Pack consumers inherit skills through template-pack fragments ([D1.6](D1.6-l5-template-pack-fragment.md)); ad hoc skill forks without catalog provenance violate [D5.3](D5.3-fork-new-catalog-entry-provenance.md). Skill promotion should include a smoke verify in SEC-15 release rows.""",
    "D1.5": """\
L4 is ambient automation: hooks in `.cursor/hooks.json`, CI workflows, and scheduled jobs that run without a conductor turn—staleness checks, dashboard regeneration, queue EMPTY gates, and validate-workflow on push. Ambient layers enforce invariants the pursuit loop might skip under token pressure.

Hook and CI extensions are platform work ([D4.4](D4.4-platform-work-hook-validate-workflow.md)) and must stay backwards-compatible or follow [D5.2](D5.2-extend-backwards-compatible-staleness-bump.md) staleness rules. L4 does not dequeue product next_action; it guards repo health while [D3.1](D3.1-1-platform-turn-per-k-product-turns.md) interleaves explicit platform turns. See [Vision §6](../../full-automation-vision-and-hierarchy.md#6-branch-d-platform-evolution-plane-parallel-queue) for maturity ordering L0→L5.""",
    "D1.6": """\
L5 is the top rung: template-pack fragments in `template-packs/` that ship with company instantiation—default pipelines, role bindings, verify suites, and catalog components new goals inherit on day one. Fragments export upward from consumer repo promotions ([D4.6](D4.6-platform-work-pack-fragment-export.md)), not one-off edits inside a single product branch.

Pack authors validate fragments against pack schema (Plane F) before publish. An L5 promotion closes the loop started at L0 ephemeral reasoning: the pattern is now organizational capital. Definition-of-done for L5 includes [D6.4](D6.4-platform-done-staleness-node-wired.md) graph wiring so downstream goals know when fragments change.""",
    "D2.1.1": """\
When an operator or agent runs the same manual shell command twice in pursuit—pytest with identical flags, a export script, a validate call—the system enqueues a promotion candidate instead of tolerating endless repetition. The trigger is observation of duplicated manual invocation, not a guess after one run.

Enqueue attaches source task or journal context, suggested target_level (often L2 script), and priority per [D2.2](D2.2-platform-queue-item-schema.md). Processing happens on platform turns ([D2.3](D2.3-dequeue-platform-turn-not-product.md)) under [D3.1](D3.1-1-platform-turn-per-k-product-turns.md) scheduling—the project schedule does not defer all delivery until every improvement is finished unless [D3.3](D3.3-priority-cut-product-blocked-missing-tool.md) inverts priority.""",
    "D2.1.2": """\
Economy workers can flag repetition: when implement or verify subagents detect the same file pattern, test fix, or catalog miss across turns, they emit a promotion signal to the conductor—workers do not write queue JSON directly. The conductor merges flags, deduplicates by fingerprint, and enqueues one item per pattern.

This trigger catches repetition invisible to shell history—structural rework, not just duplicate commands. Pair with [B4.4](B4.4-divergence-log-when-not-composing.md) divergence logs when compose-first failed before invention. False positives defer enqueue until a second independent flag or manual 2× command ([D2.1.1](D2.1.1-enqueue-repeated-manual-command-2x.md)) confirms the pattern.""",
    "D2.1.3": """\
If the same verify or test command shape appears on N task cards—default N from pack policy—the pattern is mature enough for script or playbook promotion without waiting for manual duplication. Task-breakdown and verify-router logs supply evidence: identical command blocks, same failure class, same evidence path template.

Enqueue records N, sample task ids, and target_level. Platform drain executes script extraction or playbook-keeper per target level ([D4.2](D4.2-platform-work-script-extraction.md), [D4.1](D4.1-platform-work-playbook-keeper.md)). Premature enqueue (N too low) wastes platform slots; pack authors tune N in template-pack drain policy alongside K product steps.""",
    "D2.1.4": """\
After S3 merge or S4 H2 escalation, the conductor runs a short post-mortem: what repeated, what was improvised, what catalog entry was missing. Concrete improvement candidates from that review go on the promotion queue—especially when escalation root cause was absent playbook, script, or skill.

Post-mortem enqueue is conductor-only; it captures institutional learning from failure, not happy-path optimization. Items may target L1 playbook first even when L2 script is eventual goal. Scheduling still follows platform turns; urgent product blockers on missing artifacts can raise priority via [D3.3](D3.3-priority-cut-product-blocked-missing-tool.md) without skipping H2 resolution.""",
    "D2.2": """\
Each `platform.promotion_queue[]` entry follows a strict schema: `id`, `source` (task, divergence log, or post-mortem ref), `target_level` (L1–L5), `priority`, and `effort_class` so schedulers and workers estimate drain cost. Optional fields capture reason text, fingerprint, and partial promotion state.

Schema conformance is S0-validatable; malformed items must not dequeue. Priority overrides FIFO when [D3.2](D3.2-priority-boost-queue-depth-threshold.md) or [D3.5](D3.5-max-platform-backlog-age-force-drain.md) fire. The conductor is sole writer—concurrent manual JSON edits reload each wake with a journal note. See [APP-B-state-json-sketch](APP-B-state-json-sketch.md) for platform block shape.""",
    "D2.3": """\
Dequeue consumes the queue head on a platform turn, not a product turn: `next_action` for consumer goals is untouched while platform workers run playbook-keeper, script extraction, or catalog regeneration. One platform item per platform turn preserves auditability unless parallel platform slots are explicitly enabled in policy.

After drain, dual-write marks item done only when [D6 definition of done](D6-index.md) passes—catalog row, verify script if L2+, task reference, staleness node. Partial work re-enqueues with updated state rather than false completion. Product pursuit resumes on the following turn unless scheduler inserted platform turn mid-autopilot ([D3.1](D3.1-1-platform-turn-per-k-product-turns.md)).""",
    "D3.1": """\
Default scheduling grants one platform turn every K product turns—commonly K=5—encoded in `platform.drain_policy.product_steps_per_platform_turn`. Autopilot evaluates `(steps_total % K) == 0` after each product phase completes; when true, the next iteration is platform dequeue instead of implement or design.

If the improvement queue is empty, the platform turn is skipped and the project continues—delivery does not sit idle waiting for self-improvement work. K is pack-configurable ([D5.1](D5.1-configure-task-level-params-only.md)) without forking schedulers. Overrides from [D3.2](D3.2-priority-boost-queue-depth-threshold.md), [D3.4](D3.4-idle-drain-product-waits-h2.md), and [D3.5](D3.5-max-platform-backlog-age-force-drain.md) layer on this baseline.""",
    "D3.2": """\
When promotion queue depth exceeds a configured threshold, priority boost accelerates platform drains—extra platform turns or elevated head priority—so backlog cannot grow unbounded during heavy implement phases. Boost is a pressure valve, not the default cadence; it complements [D3.1](D3.1-1-platform-turn-per-k-product-turns.md) rather than replacing K-step interleaving.

Threshold and boost factor live in drain_policy beside K. Boost must not defer the current project goal when next_action is evidence-blocked; [D3.3](D3.3-priority-cut-product-blocked-missing-tool.md) can temporarily suspend boost to favor enqueue-and-drain of the missing artifact class. Track depth in state.json for operator dashboard visibility and SEC-15 audit rows.""",
    "D3.3": """\
Priority cut inverts normal scheduling when product pursuit is blocked on a missing playbook, script, or catalog entry: platform drain targeting that artifact class jumps ahead of routine K-step interleaving. The product goal stays blocked on H2 or internal wait until the promoted artifact exists or operator waives.

Cut prevents absurd ordering—five implement turns while the very playbook needed for implement sits queued at priority 50. Cut does not clear human gates; it only reprioritizes platform work that unblocks product. Enqueue triggers ([D2.1](D2.1-index.md)) may fire during the same blocked window; verify [D6](D6-index.md) checklist before marking promotion done.""",
    "D3.4": """\
When product pursuit waits on external H2—credentials, legal approval, operator answer—CPU and conductor attention would otherwise idle. Idle drain spends that wait on platform queue processing: dequeue and promote without advancing product next_action or clearing gates.

Idle drain respects H2 semantics: no silent gate clearance, no fake implement progress. It maximizes parallel platform evolution during human latency and pairs naturally with autopilot loops that would otherwise spin on blocked checks. When H2 clears, product turns resume on prior next_action; platform backlog should be thinner than if waits were pure no-ops. See [A4.1](A4.1-stop-human-h1-h2-h3.md) stop taxonomy.""",
    "D3.5": """\
Each promotion item carries age; when oldest backlog exceeds max_platform_backlog_age, force drain policy schedules platform turns until age falls or queue empties—even if K-step cadence would defer drain. This prevents the improvement backlog from rotting during long project-only sprints.

Force drain is the adversarial-review backstop cited across D-branch specs. It does not override active product evidence gates; it prevents promotion debt from rotting. Age resets on partial promotion with re-enqueue; false done still fails [D6](D6-index.md) audit. Operator may tune age and force intensity per pack.""",
    "D4.1": """\
Playbook-keeper is the primary L1 platform work type: distill repeated reasoning, divergence log entries, or task post-mortems into `docs/playbooks/<slug>.md` with INDEX registration planned. Economy platform workers run under conductor contract with queue item id; they do not edit consumer feature scope or dual-write pursuit state.

Output feeds script extraction ([D4.2](D4.2-platform-work-script-extraction.md)) when steps stabilize. Playbook-keeper follows compose-first ([B4.3](B4.3-compose-first-catalog-before-improvise.md))—extend existing playbooks before new slugs. Completion requires playbook path, word-quality bar, and enqueue downstream promotion if L2 candidate steps are identified.""",
    "D4.2": """\
Script extraction promotes L1 playbook steps—or verified manual commands—into S0 Python under `scripts/` with tests. Extraction is platform work: changes tooling for all future goals, not the current consumer feature branch unless explicitly shared.

Extracted scripts must be idempotent, CLI-invokable, and referenced from playbook diff. Wire verify-router when script replaces task-card Test command. Backwards-compatible extensions use [D5.2](D5.2-extend-backwards-compatible-staleness-bump.md); behavior breaks require [D5.3](D5.3-fork-new-catalog-entry-provenance.md) fork with new catalog id. [B1.1](B1.1-s0-deterministic-mandatory-first.md) mandates conductor runs script before model re-derivation.""",
    "D4.3": """\
Skill and command wrapper work packages L2 scripts plus journal-keeper hooks into L3 `.cursor/skills/` or `/commands` entry points—thin orchestration surfaces the conductor invokes by name. Wrappers encode allowed_reads, evidence requirements, and forbidden paths consistent with active role ([B5.1](B5.1-active-role-from-template-pack.md)).

Wrapper promotion does not duplicate script logic inside SKILL.md; it calls S0 scripts and cites playbook paths. New commands register in operator dashboard docs when user-facing. Failed wrapper verify leaves queue item open; partial SKILL without command or vice versa re-enqueues until both surfaces exist or pack policy declares skill-only.""",
    "D4.4": """\
Hook and validate-workflow extension is L4 platform work: extend `.cursor/hooks.json` or CI steps so validate-workflow, check-pipeline-blocked, or staleness scripts run on session events without conductor turns. Changes must pass `python scripts/validate-workflow.py` on the PR that introduces them.

Hooks are not pursuit loops—they fail closed into journal notes when scripts error. Extend-only hook changes follow [D5.2](D5.2-extend-backwards-compatible-staleness-bump.md); hook behavior that alters gate semantics needs explicit pack review. Successful promotion moves ambient enforcement up the [D1.5](D1.5-l4-ambient-hooks-ci-scheduled.md) ladder so S0 scripts run even when the conductor forgets.""",
    "D4.5": """\
Catalog and INDEX regeneration is platform work after new playbooks, scripts, skills, or pack fragments land: update `docs/playbooks/INDEX.md`, manifest catalog nodes, and operator discovery rows so compose-first search finds fresh artifacts ([B4.3](B4.3-compose-first-catalog-before-improvise.md)).

Regeneration is S0 where scripts exist; otherwise economy worker with allowed_reads on new artifact paths only. Regeneration without artifact creation is invalid—INDEX must point to real files. Librarian and implement workers depend on fresh INDEX rows; skipping regeneration breaks [B4.3](B4.3-compose-first-catalog-before-improvise.md) and fails [D6.1](D6.1-platform-done-catalog-index-row.md).""",
    "D4.6": """\
Pack fragment export is upward promotion: vetted repo artifacts become `template-packs/` fragments new instantiations inherit—default skills, pipeline stubs, verify suites, glossary rows. Export is organizational, not a hotfix to one consumer repo.

Export requires pack-author authority or H2 when external pack repo access is missing. Fragments version semver-style; provenance links to source promotion id ([D5.3](D5.3-fork-new-catalog-entry-provenance.md)). This is the L5 capstone work type paired with [D1.6](D1.6-l5-template-pack-fragment.md); consumer goals should reference pack version, not fork fragments inline. Plane F pack verify suites gate publish.""",
    "D5.1": """\
Configure is the lightest platform change class: adjust task-level or drain_policy parameters—K, N, thresholds, role flags—without new catalog entries or code forks. Configuration lives in state.json, pack YAML, or task-card params explicit in journal decisions.

Configure promotions do not bump staleness graph nodes because behavior artifacts are unchanged—only their invocation parameters. Misapplied configure (wrong K) is reversible via journal Q&A. When parameter change implies new tool behavior, escalate to [D5.2](D5.2-extend-backwards-compatible-staleness-bump.md) or [D5.3](D5.3-fork-new-catalog-entry-provenance.md) instead of configure. Pack authors document tunables in template-pack schema comments.""",
    "D5.2": """\
Extend means backwards-compatible improvement to an existing catalog artifact—add optional flag to script, append playbook section, extend skill without breaking callers. Extension triggers staleness bump on dependent design nodes and task cards per Plane E reconcile rules.

Platform queue items targeting extend must cite parent catalog id and compatibility proof—tests green, validate-workflow passes. Extend is preferred over fork when compose-first can absorb the change ([B4.3](B4.3-compose-first-catalog-before-improvise.md)). Non-compatible behavior change is fork, not extend, even if filename stays the same—semver and provenance matter.""",
    "D5.3": """\
Fork creates a new catalog entry with provenance link to the source promotion or parent artifact—used when behavior diverges, pack boundary requires isolation, or extend would break consumers. Fork records why compose-first failed ([B4.4](B4.4-divergence-log-when-not-composing.md)) and what was invented.

New id, new INDEX row, new staleness node ([D6.4](D6.4-platform-done-staleness-node-wired.md)) are mandatory. Fork without provenance blocks SEC-14 gap analysis trust. Downstream task cards migrate explicitly; silent alias is forbidden. Pack fragments ([D4.6](D4.6-platform-work-pack-fragment-export.md)) may fork upward into template-pack namespace.""",
    "D6.1": """\
Platform promotion is not done until a catalog entry exists and INDEX row points to it—playbook slug, script path, skill name, or pack fragment id discoverable from compose-first search. INDEX regeneration ([D4.5](D4.5-platform-work-catalog-regeneration.md)) is often the completing step of another work type.

Missing INDEX row fails audit-hierarchy-depth strict checks and leaves queue item reopenable. Row includes maturity level, verify command reference, and optional promotion id trace. Consumer goals should never hunt ad hoc paths omitted from INDEX; Librarian allowed_reads assume INDEX is authoritative for playbook discovery.""",
    "D6.2": """\
For L2 and above promotions, definition of done requires a verify path—unit test, verify-router command, or validate-workflow hook—that proves the script or tool behaves as specified. L1 playbooks may cite manual verify until scripted; L2+ without automated verify fails platform done.

Evidence discipline mirrors product tasks but writes platform-appropriate logs under `evidence/` or unit test output. Script promotion pairs extraction ([D4.2](D4.2-platform-work-script-extraction.md)) with test file in `tests/unit/`. False done without verify triggers audit re-enqueue and blocks [D2.3](D2.3-dequeue-platform-turn-not-product.md) head advance.""",
    "D6.3": """\
At least one task card—or playbook procedure consumed by task cards—must reference the promoted artifact so future implement turns exercise it under evidence gates. Orphan scripts unused by pursuit are platform debt, not maturity.

Reference can be Components field, Test command, or explicit allowed_reads entry on a template task card. Playbook-keeper should add reference guidance when capturing patterns from a source task. D6.3 closes the loop from product repetition to reusable tooling back to product—without reference, promotion did not enter the delivery loop and [C3.1](C3.1-task-cards-components-promotion-note.md) promotion_note intent is unfulfilled.""",
    "D6.4": """\
Staleness graph wiring completes platform done: promoted artifact registers as a node in program or manifest staleness with upstream dependencies so reconcile-stale and reconcile-artifact-graph mark downstream design and tasks when the artifact changes ([D5.2](D5.2-extend-backwards-compatible-staleness-bump.md) extends bump this graph).

Missing staleness node means silent consumer drift after platform edit. Wire node id, dependency edges, and pack scope in manifest JSON. Together with [D6.1](D6.1-platform-done-catalog-index-row.md)–[D6.3](D6.3-platform-done-task-card-references.md), D6.4 is the audit gate before queue item done—see [D6-index](D6-index.md).""",
}


def apply_plane_d(out_dir: Path | None = None) -> int:
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from hierarchy_agent_prose import apply_narrative  # noqa: E402
    from hierarchy_completeness import item_id_from_path, list_leaf_paths  # noqa: E402

    base = out_dir or ROOT / "documents/plans/full-automation"
    applied = 0
    for p in list_leaf_paths(base):
        iid = item_id_from_path(p, p.read_text(encoding="utf-8"))
        if iid not in PLANE_D_NARRATIVES:
            continue
        new_text, issues = apply_narrative(p, PLANE_D_NARRATIVES[iid], version="plane-d")
        p.write_text(new_text, encoding="utf-8")
        applied += 1
        if issues:
            print(f"{iid}: {', '.join(issues)}")
    print(f"Applied Plane D agent prose to {applied} leaves")
    return 0


if __name__ == "__main__":
    raise SystemExit(apply_plane_d())
