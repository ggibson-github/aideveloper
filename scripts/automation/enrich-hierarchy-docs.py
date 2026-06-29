#!/usr/bin/env python3
"""Fully expand all hierarchy leaf docs — replaces scaffolds with detailed plan content."""

from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from hierarchy_queue_data import EXPAND_NODES, LEAVES, STANDALONE_DOCUMENTS, slug  # noqa: E402
from hierarchy_vision_context import find_tree_context, load_vision_lines, section_for_branch  # noqa: E402

QUEUE = ROOT / "docs/automation/vision-expansion-queue.json"
INDEX = ROOT / "documents" / "plans" / "full-automation" / "INDEX.md"

BRANCH_PURPOSE = {
    "A": "Pursuit & control plane — autonomous loops until goal verified.",
    "B": "Cognition & routing — S0–S4, conductor, workers, dual-stack.",
    "C": "Product execution — pipelines, tasks, program, delivery.",
    "D": "Platform evolution — promotion ladder, parallel queue, reuse.",
    "E": "Knowledge & composition — catalog, compose-first, staleness.",
    "F": "Organization — template-packs as whole-company ceiling.",
    "G": "Verification & quality — evidence, goal_verify, anti-mistake.",
    "H": "Persistence — journal, state.json, graphs, evidence.",
    "I": "Runtime & integration — IDE, SDK, headless, MCP tools.",
    "J": "Governance — policy, waivers, audit, export contract.",
    "INTRO": "North star, scope, minimal HITL (H1/H2/H3).",
    "MASTER": "Top-level decomposition into ten planes.",
    "SEC": "Roadmap, gap analysis, pursuit flow, decisions.",
    "APP": "Human job taxonomy → pack workflows.",
    "meta": "Cross-cutting meta sections.",
}

# Concrete repo touchpoints per branch for implementers
BRANCH_ARTIFACTS = {
    "A": ["journal/state.json `goal`, `pursuit`, `hitl`", "scripts/automation/check-pipeline-blocked.py", "scripts/automation/run-local-pipeline.py", ".cursor/skills/autopilot/"],
    "B": ["docs/operator/model-policy.json", "scripts/route-tier.py", ".cursor/skills/librarian/", ".cursor/rules/genius-conductor.mdc"],
    "C": ["docs/tasks/", "docs/manifest/pipelines/", ".cursor/skills/implement-feature/", "program/workstreams/"],
    "D": ["docs/playbooks/", "scripts/", ".cursor/skills/playbook-keeper/", "state.platform.promotion_queue"],
    "E": ["docs/facts/INDEX.md", "docs/playbooks/INDEX.md", "docs/manifest/staleness.json", "allowed_reads"],
    "F": ["template-packs/", "program/integration/manifest.md", ".cursor/skills/program-scoper/"],
    "G": ["scripts/verify-router.py", "scripts/validate-workflow.py", "evidence/", ".cursor/skills/verifier/"],
    "H": ["journal/state.json", "journal/progress.md", "evidence/", "docs/manifest/staleness.json"],
    "I": ["docs/automation/", ".cursor/hooks/", "docs/operator/export-contract.md"],
    "J": ["docs/operator/model-policy.json", "docs/decisions/automation-waivers.md", "docs/automation/release-queue.json"],
}


def branch_for(item_id: str) -> str:
    if item_id.startswith("INTRO"):
        return "INTRO"
    if item_id.startswith("MASTER"):
        return "MASTER"
    if item_id.startswith("SEC") or item_id.startswith("APP-B"):
        return "SEC"
    if item_id.startswith("APP"):
        return "APP"
    m = re.match(r"^([A-J])", item_id)
    return m.group(1) if m else "meta"


def infer_state_fields(item_id: str, title: str) -> list[tuple[str, str, str]]:
    """Return (field, type, description) tuples when inferrable."""
    fields: list[tuple[str, str, str]] = []
    t = title.lower()
    if "goal" in t and item_id.startswith("A1"):
        fields = [
            ("goal.id", "string", "Unique goal identifier"),
            ("goal.parent_goal", "string|null", "Parent for nested goals"),
            ("goal.type", "enum", "app | feature | milestone | company_ops"),
        ]
    elif item_id.startswith("A1.2"):
        fields = [("goal.success_criteria", "string[]", "Machine-checkable acceptance bullets")]
    elif item_id.startswith("A1.3"):
        fields = [("goal.verify_command", "string", "Shell command; exit 0 = goal met")]
    elif item_id.startswith("A1.5"):
        fields = [("goal.state", "enum", "pursuing | blocked | verifying | achieved | rejected")]
    elif item_id.startswith("H1."):
        block = item_id.replace("H1.", "")
        fields = [(f"state block H1.{block}", "object", f"See APP-B-state-json-sketch.md H1.{block}")]
    elif "platform queue" in t or item_id.startswith("D2"):
        fields = [("platform.promotion_queue", "array", "Promotion items FIFO with priority overrides")]
    elif item_id.startswith("D3.1"):
        fields = [("platform.drain_policy.product_steps_per_platform_turn", "number", "Default K=5")]
    return fields


def step_logic_for(item_id: str, title: str, branch: str) -> list[str]:
    """Concrete step logic bullets."""
    steps = [
        f"Conductor reads `{item_id}` context from master vision {section_for_branch(item_id)}.",
        "Run applicable S0 script before any LLM turn ([deterministic-first](../../../.cursor/rules/deterministic-first.mdc)).",
    ]
    if branch == "A" and "preflight" in title.lower():
        steps.append("Execute `python scripts/automation/check-pipeline-blocked.py`; abort turn if exit 1.")
    elif branch == "A" and "goal_verify" in title.lower():
        steps.append("When `goal.scope_complete`, run `goal.verify_command`; set `hitl.pending=H3` on pass.")
    elif branch == "D" and "enqueue" in title.lower():
        steps.append("Append item to `platform.promotion_queue` with source task id and target_level L1–L5.")
    elif branch == "D" and "dequeue" in title.lower():
        steps.append("Platform turn: dequeue head unless D3.3 product blocked on missing catalog entry.")
    elif branch == "E" and "compose" in title.lower():
        steps.append("Librarian returns `suggested_components`; task card lists Components used.")
    elif branch == "G" and "verify" in title.lower():
        steps.append("Verifier runs test/tool command; writes `evidence/<task>-test.log`; sets `last_verify`.")
    elif branch == "F" and "pack" in title.lower():
        steps.append("Artifact lives under `template-packs/<pack-id>/`; program-scoper selects by keywords.")
    else:
        steps.append(f"Implement '{title}' per parent index; add tests or scripts where behavior is deterministic.")
    steps.append("On failure: structured H2 blocker in journal; do not advance `next_action` or queue item.")
    return steps


def generate_expanded_body(item: dict, vision_lines: list[str]) -> str:
    iid = item["id"]
    title = item["title"]
    parent = item.get("parent") or "—"
    branch = branch_for(iid)
    purpose = BRANCH_PURPOSE.get(branch, BRANCH_PURPOSE.get("meta", ""))
    tree_ctx = find_tree_context(iid, vision_lines)
    section = section_for_branch(iid)
    artifacts = BRANCH_ARTIFACTS.get(branch, [])
    state_fields = infer_state_fields(iid, title)
    steps = step_logic_for(iid, title, branch)

    # Release / decision specials (keep rich templates)
    if iid.startswith("SEC-15-v2."):
        ver = iid.replace("SEC-15-", "")
        return f"""# {iid}: {title}

**Parent:** [SEC-15-index](SEC-15-index.md) · **Vision:** [§15](../../full-automation-vision-and-hierarchy.md)

## Purpose

Ship harness release **{ver}** as an incremental step toward full automation.

## Deliverables

| Area | Expected artifacts |
|------|-------------------|
| Schema | Additive `state.json` fields only (`version` stays 2) |
| Scripts | S0 tools listed in vision §15 row for {ver} |
| Skills | New or updated `.cursor/skills/*` |
| Tests | `tests/unit/` for new scripts |
| Docs | export-contract, dashboard, journal-keeper |

## Implementation sequence

1. Read §15 row for {ver} in [full-automation-vision-and-hierarchy.md](../../full-automation-vision-and-hierarchy.md).
2. Implement vertical slice; run `python scripts/validate-workflow.py`.
3. Run full unit/integration suite per [test-before-push](../../../.cursor/rules/test-before-push.mdc).
4. Update operator dashboard generator if new state fields.

## Acceptance criteria

- [ ] Every bullet in §15 for {ver} has a matching file or journal note
- [ ] Conformance CI green
- [ ] No regression to v2.13 autopilot/program/evidence paths

## Dependencies

Prior releases in v2.14–v2.23 chain; [genius-conductor-tiered-routing.md](../../genius-conductor-tiered-routing.md).
"""

    if iid.startswith("SEC-17-"):
        return f"""# {iid}: {title}

**Parent:** [SEC-17-index](SEC-17-index.md)

## Decision

{title}

## Proposed default

| Choice | Recommendation |
|--------|----------------|
| SEC-17-1 self-gate | Checklist + automated `validate-workflow.py` + optional economy reviewer on large diffs |
| SEC-17-2 H3 scope | Per **goal** (milestone/release), not per task |
| SEC-17-3 platform K | Adaptive: 1 platform turn per 5 product turns; boost when queue depth > 10 |
| SEC-17-4 budget | `pursuit.budget.max_wall_hours` with checkpoint notify, not hard stop mid-task |
| SEC-17-5 pack authority | Packs may mark roles `hitl: always` (legal/finance); default automated |
| SEC-17-6 multi-goal | `company_autopilot` prioritized goal queue in `state.pursuit` |

Record final choice in `docs/decisions/full-automation-{iid.lower()}.md`.

## Acceptance

- [ ] ADR exists; downstream leaves reference decision
"""

    state_table = ""
    if state_fields:
        rows = "\n".join(f"| `{f}` | {typ} | {desc} |" for f, typ, desc in state_fields)
        state_table = f"""
## State / data fields

| Field | Type | Description |
|-------|------|-------------|
{rows}
"""
    elif branch in ("A", "H", "D"):
        state_table = """
## State / data fields

See [APP-B-state-json-sketch.md](APP-B-state-json-sketch.md) and v2.14+ additive schema. Map fields to this leaf during implement of the named release.
"""

    art_list = "\n".join(f"- `{a}`" for a in artifacts[:6])
    step_list = "\n".join(f"{i}. {s}" for i, s in enumerate(steps, 1))

    tree_block = ""
    if tree_ctx:
        tree_block = f"""
## Hierarchy context (vision doc)

```
{tree_ctx}
```
"""

    parent_link = f"[{parent}-index]({parent}-index.md)" if parent and parent != "—" else f"`{parent}`"
    return f"""# {iid}: {title}

**Parent:** {parent_link} · **Branch {branch}:** {purpose} · **Vision {section}**

## Purpose

Authoritative design for **{title}** (`{iid}`). Part of the full-automation target; implements one leaf of the brainstorming hierarchy.

## Scope

- Owns behavior for `{iid}` only; siblings under `{parent}` must not duplicate this spec.
- Must align with minimal HITL: H1 plan, H2 blocker, H3 sign-off ([INTRO-1.2](INTRO-1.2-human-touchpoint-contract-h1-h2-h3.md)).
{tree_block}
## Behavior / step logic

{step_list}

## Repo artifacts (this branch)

{art_list}

{state_table}
## Verification

| Check | Command / artifact |
|-------|-------------------|
| Conformance | `python scripts/validate-workflow.py` |
| Task-level | `python scripts/verify-router.py` when implement task exists |
| Goal-level | `goal.verify_command` when applicable (A1.3, G2.x) |

## Dependencies

| Link | Why |
|------|-----|
| [full-automation-vision-and-hierarchy.md](../../full-automation-vision-and-hierarchy.md) {section} | Master hierarchy |
| [{parent}-index]({parent}-index.md) | Parent grouping |
| [genius-conductor-tiered-routing.md](../../genius-conductor-tiered-routing.md) | S0–S4 routing |

## Acceptance criteria

- [ ] Behavior is testable (script, test, or checklist)—not prose-only
- [ ] Linked from parent `{parent}-index.md`
- [ ] Composes with catalog/playbooks where reuse exists (branch E, D)

## Deferred questions

- Exact ship release (v2.14–v2.23) unless already implemented in baseline v2.13
"""


def slug_path(item: dict) -> Path:
    out = item.get("output")
    if out:
        return ROOT / out
    iid = item["id"]
    title = item.get("title", iid)
    return ROOT / "documents" / "plans" / "full-automation" / f"{iid}-{slug(title)}.md"


def main() -> int:
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--incomplete-only", action="store_true", help="Skip leaves that pass strict audit")
    ap.add_argument("--threshold", type=int, default=90)
    ap.add_argument("--ids", nargs="*")
    args = ap.parse_args()

    if not QUEUE.is_file():
        print(f"Missing {QUEUE}", file=sys.stderr)
        return 1

    from hierarchy_completeness import score_doc_completeness, item_id_from_path, title_from_path  # noqa: E402

    data = json.loads(QUEUE.read_text(encoding="utf-8"))
    today = date.today().isoformat()
    vision_lines = load_vision_lines()
    index_rows: list[str] = []
    written = 0

    skipped = 0
    for item in data["items"]:
        if item.get("action") != "document":
            continue
        iid = item["id"]
        if args.ids and not any(iid == x or iid.startswith(x + ".") or iid.startswith(x) for x in args.ids):
            continue
        path = slug_path(item)
        if args.incomplete_only and path.is_file():
            text = path.read_text(encoding="utf-8")
            title = title_from_path(path, iid)
            _, _, ok = score_doc_completeness(text, iid, title, threshold=args.threshold)
            if ok:
                skipped += 1
                continue
        path.parent.mkdir(parents=True, exist_ok=True)
        body = generate_expanded_body(item, vision_lines)
        path.write_text(
            f"<!-- Expanded {today} hierarchy item {item['id']} -->\n\n{body}",
            encoding="utf-8",
        )
        item["status"] = "done"
        item["expanded_at"] = today
        if "completed_at" not in item:
            item["completed_at"] = today
        rel = path.relative_to(ROOT / "documents" / "plans" / "full-automation").as_posix()
        index_rows.append(f"| {item['id']} | [{item['title']}]({rel}) | expanded |")
        written += 1

    data["expansion_status"] = "complete"
    data["expanded_at"] = today
    QUEUE.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    index_content = f"""# Vision expansion output

Fully expanded plan documents from the unified hierarchy queue.

Master hierarchy: [full-automation-vision-and-hierarchy.md](../../full-automation-vision-and-hierarchy.md)

**Expanded:** {today} · **Leaf documents:** {written} · **Status:** complete

## Branch indexes

| Branch | Index |
|--------|-------|
| A | [A1-index](A1-index.md) … [A6-index](A6-index.md) |
| B–J | See `*-index.md` files in this directory |
| Meta | [INTRO-index](INTRO-index.md), [SEC-15-index](SEC-15-index.md), [SEC-17-index](SEC-17-index.md) |

## Full index

| Id | Document | Status |
|----|----------|--------|
"""
    index_content += "\n".join(sorted(index_rows, key=lambda r: r.split("|")[1].strip())) + "\n"
    INDEX.write_text(index_content, encoding="utf-8")

    # Refresh branch indexes
    import subprocess
    subprocess.run([sys.executable, str(ROOT / "scripts/automation/write-vision-branch-indexes.py")], check=False)

    scaffolds = sum(
        1 for p in (ROOT / "documents/plans/full-automation").glob("*.md")
        if p.name not in ("INDEX.md",) and "TBD for `" in p.read_text(encoding="utf-8")
    )
    print(f"Expanded {written} documents (skipped {skipped} complete). Remaining scaffolds (TBD): {scaffolds}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
