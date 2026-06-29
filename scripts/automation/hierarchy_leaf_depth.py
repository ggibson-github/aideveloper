#!/usr/bin/env python3
"""Shared depth helpers for hierarchy leaf documents."""
from __future__ import annotations
import re
from datetime import date
def branch_for(item_id: str) -> str:
    if item_id.startswith("INTRO"):
        return "INTRO"
    if item_id.startswith("MASTER"):
        return "MASTER"
    if item_id.startswith("SEC") or item_id == "APP-B":
        return "SEC"
    if item_id.startswith("APP"):
        return "APP"
    m = re.match(r"^([A-J])", item_id)
    return m.group(1) if m else "meta"


def needs_flow_diagram(item_id: str, title: str) -> bool:
    t = title.lower()
    return any(k in t for k in ("loop", "preflight", "pursuit", "verify", "queue", "pipeline", "handoff", "dequeue", "enqueue"))


def build_mermaid(item_id: str, title: str) -> str:
    t = title.lower()
    # Example template packs only â€” NOT core system semantics (F3=game studio, F4=data platform)
    if item_id == "F3.2":
        return """```mermaid
flowchart LR
  concept[Concept] --> mesh[Mesh] --> rig[Rig] --> anim[Anim]
  anim --> ue[Engine Import] --> qa[QA] --> build[Build]
```"""
    if item_id == "F4.2":
        return """```mermaid
flowchart LR
  ingest[Ingest] --> model[Model / Transform] --> deploy[Deploy] --> monitor[Monitor / Alert]
```"""
    if item_id.startswith("F1") and "pipeline" in t:
        return """```mermaid
flowchart TD
  pack[template-packs/company/pipelines.yaml] --> manifest[Integration manifest]
  manifest --> lane[lane work orders]
  lane --> skills[Role-bound skill phases]
```"""
    if "preflight" in t or item_id == "A2.1":
        return """```mermaid
flowchart TD
  start[Conductor turn start] --> s0[check-pipeline-blocked.py]
  s0 -->|exit 0 READY| step[Execute one pipeline step]
  s0 -->|exit 1 BLOCKED| stop[Stop pursuit / H2]
  step --> post[route-tier + dual-write]
  post --> start
```"""
    if item_id == "A2.2" or ("execute" in t and "pipeline step" in t):
        return """```mermaid
flowchart TD
  ready[check-pipeline-blocked: READY] --> route[route-tier.py reads next_action]
  route --> skill[Execute exactly one skill phase]
  skill --> ev[Verify if implement task]
  ev --> dw[journal-keeper dual-write]
  dw --> inc[Increment pursuit.steps_total]
```"""
    if "goal_verify" in t or "regression" in t or item_id in ("A2.4", "A2.5", "G2.4"):
        return """```mermaid
flowchart TD
  batch[Implement batch complete] --> taskV[All task evidence passed?]
  taskV -->|no| block[Block + H2]
  taskV -->|yes| goalV[Run goal.verify_command]
  goalV -->|pass| h3[hitl.pending = H3]
  goalV -->|fail| block
```"""
    if item_id.startswith("C1") or "pipeline-" in item_id.lower():
        return """```mermaid
flowchart TD
  entry[Entry: spec or feature request] --> pick{pipeline_id}
  pick -->|greenfield| gf[spec-parser â†’ HLD â†’ DD â†’ tasks]
  pick -->|iterative_feature| it[iterative-feature â†’ design gate]
  pick -->|program| pr[program-scoper â†’ manifest gate]
  pick -->|pack| pk[company pack pipelines.yaml]
```"""
    if item_id in ("A3.4", "I2.1") or "run-local-pipeline" in t or "daemon" in t:
        return """```mermaid
flowchart TD
  daemon[run-local-pipeline.py / SDK daemon] --> poll[Poll state.json]
  poll -->|goal_autopilot + READY| step[One pursuit step]
  poll -->|BLOCKED| stop[Exit with H2 reason]
  step --> poll
```"""
    if "conformance" in t or item_id == "G3.3":
        return """```mermaid
flowchart TD
  ci[CI or pre-push] --> vw[validate-workflow.py]
  vw --> cpb[check-pipeline-blocked.py --goal-autopilot]
  cpb -->|pass| ok[Allow merge / continue pursuit]
  cpb -->|fail| fail[Block with structured reason]
```"""
    if "catalog" in t and "pipeline" in t:
        return """```mermaid
flowchart LR
  manifest[docs/manifest/pipelines/] --> idx[INDEX + pipeline_id]
  idx --> route[route-tier.py selects pipeline_id]
  route --> skills[Skill phases from manifest]
```"""
    if "role" in t and "pipeline" in t:
        return """```mermaid
flowchart TD
  role[state.company.active_role] --> pack[roles/*.yaml]
  pack --> pid[pipeline_id + allowed_skills]
  pid --> lane[lane.json work order]
```"""
    if "queue" in t or item_id.startswith("D2"):
        return """```mermaid
flowchart LR
  prod[Product turn] --> k{step mod K == 0?}
  k -->|yes| plat[Platform turn dequeue]
  k -->|no| prod
  plat --> promote[promotion_queue drain]
  promote --> prod
```"""
    if "loop" in t or item_id.startswith("A2.6") or item_id.startswith("A3"):
        return """```mermaid
flowchart TD
  start[Pursuit turn] --> pre[S0 preflight]
  pre -->|READY| step[One step]
  pre -->|BLOCKED| exit[Stop: H2 or budget]
  step --> goal{goal_scope_complete?}
  goal -->|yes| gv[goal_verify]
  goal -->|no| start
  gv -->|pass| h3[H3 pending]
  gv -->|fail| exit
```"""
    return """```mermaid
flowchart TD
  trigger[Trigger condition] --> pre[Preconditions S0]
  pre --> exec[Execute step logic]
  exec --> verify[Verify output]
  verify -->|pass| done[Mark queue item done]
  verify -->|fail| h2[H2 blocker]
```"""


def json_example(item_id: str, title: str) -> str:
    if item_id.startswith("A1"):
        return """```json
{
  "goal": {
    "id": "goal-001",
    "parent_goal": null,
    "type": "program",
    "success_criteria": ["manifest approved", "goal_verify exit 0"],
    "verify_command": "python scripts/goal-verify.py",
    "state": "pursuing"
  }
}
```"""
    if item_id.startswith("D2"):
        return """```json
{
  "platform": {
    "promotion_queue": [
      {
        "id": "promo-001",
        "source": "task-012",
        "target_level": "L2",
        "priority": 50,
        "reason": "repeated manual pytest invocation"
      }
    ],
    "drain_policy": { "product_steps_per_platform_turn": 5 }
  }
}
```"""
    if item_id.startswith("H1"):
        return """```json
{
  "goal": { "id": "g1", "state": "pursuing" },
  "platform": { "promotion_queue": [] },
  "pursuit": { "mode": "goal_autopilot", "steps_total": 0 },
  "hitl": { "pending": null },
  "company": { "pack_id": null, "active_role": null }
}
```"""
    if item_id.startswith("G2") or item_id.startswith("G1"):
        return """```json
{
  "goal": {
    "verify_command": "python scripts/goal-verify.py",
    "state": "verifying"
  },
  "last_verify": "passed",
  "evidence_required": true
}
```"""
    return f"""```json
{{
  "node": "{item_id}",
  "description": "{title[:60]}",
  "state": {{ "ref": "APP-B-state-json-sketch.md" }},
  "implemented_in_release": "v2.14+"
}}
```"""


def edge_cases(item_id: str, branch: str) -> list[str]:
    base = [
        "Operator closes laptop mid-loop â€” state.json must resume from last good dual-write.",
        "Concurrent manual edit to queue JSON â€” conductor reloads queue each wake; last writer wins with journal note.",
    ]
    if branch == "A":
        base.append("goal_verify passes but H3 rejected â€” goal.state returns to pursuing with rejection notes.")
    if branch == "G":
        base.append("Flaky test â€” escalation S4 once, then H2 with evidence log; no silent retry loop.")
    if branch == "D":
        base.append("Platform queue depth 0 but product blocked on missing playbook â€” D3.3 priority cut skips platform drain.")
    if branch == "F":
        base.append("Pack role handoff while lane lease held â€” complete-work-order releases lease before role switch.")
    return base


def failure_modes(item_id: str) -> list[str]:
    return [
        "**Silent stop:** Agent ends turn without updating queue â†’ mitigated by /loop + check-hierarchy-queue.py EMPTY gate.",
        "**False complete:** Item marked done without artifact â†’ audit-hierarchy-depth.py re-enqueues deepen pass.",
        "**Scope bleed:** Worker edits journal/state during planning-only expansion â†’ forbidden in vision-expansion-prompt.",
        "**Stale design:** Upstream vision Â§ changes â†’ reconcile-stale adds deepen items for affected ids.",
    ]


def concrete_implementation(item_id: str, title: str, branch: str) -> list[str]:
    steps = []
    if branch == "A":
        steps = [
            "Add `goal` block to state template and journal-keeper dual-write (v2.14).",
            "Extend `check-pipeline-blocked.py` with goal_autopilot stop reasons.",
            "Implement `scripts/goal-verify.py` stub aggregating task evidence paths.",
            "Add `.cursor/skills/goal-keeper/SKILL.md` for conductor H1â†’pursuit transition.",
        ]
    elif branch == "D":
        steps = [
            "Add `platform.promotion_queue[]` to state.json schema.",
            "Scheduler in autopilot workflow: `(steps_total % K) == 0` â†’ platform turn.",
            "playbook-keeper + script extraction skills dequeue promotion items.",
        ]
    elif branch == "G":
        steps = [
            "Extend verify-router for goal-level suite invocation.",
            "Wire CI: validate-workflow checks goal block when pursuit.mode=goal_autopilot.",
            "Document evidence type in docs/operator/evidence-types.md.",
        ]
    elif branch == "F":
        steps = [
            "Add `company.yaml` + `roles/*.yaml` to template-packs schema.",
            "program-scoper selects pack; sets state.company.active_role.",
            "Per-role allowed_reads in lane.json work orders.",
        ]
    else:
        steps = [
            f"Map `{item_id}` to v2.14â€“v2.23 release row in SEC-15-index.md.",
            f"Create or extend S0 script if behavior is file-derived.",
            f"Add unit test under tests/unit/test_{item_id.replace('.', '_').lower()}.py when script exists.",
        ]
    return steps


def challenge_body(existing: str, item_id: str, title: str) -> str:
    branch = branch_for(item_id)
    critiques = [
        "**Assumption:** Full autonomy before v2.15 self-gates — *Mitigation:* strict_hitl flag.",
        "**Risk:** Queue file merge conflict — *Mitigation:* one writer (conductor).",
        "**Risk:** goal_verify too weak — *Mitigation:* pack verify suites (F1.8).",
    ]
    if branch == "A":
        critiques.append("**Risk:** Infinite pursuit — *Mitigation:* pursuit.budget.max_wall_hours.")
    if branch == "D":
        critiques.append("**Risk:** Platform starvation — *Mitigation:* D3.5 force drain.")
    critique_md = "\n".join(f"- {c}" for c in critiques)
    base = re.sub(r"\n## Adversarial review.*?(?=\n## |\Z)", "\n", existing, flags=re.DOTALL)
    return base.rstrip() + f"""

## Adversarial review (pass {date.today().isoformat()})

Attempt to invalidate or tighten this design:

{critique_md}

### Revisions applied

- Acceptance requires `python scripts/automation/audit-hierarchy-depth.py --strict --ids {item_id}`.
- H3 gates are not cleared automatically by pursuit loop.
- Middle gates become self-gate + evidence where automatable.

### Remaining risks (accepted for sign-off)

- External tool/API failures require H2 when credentials or network block.
- Subjective approval must live in goal.success_criteria or remain H3.

## Sign-off readiness

Ready when strict audit passes and SEC-15 implement row is shipped or waived.
"""

