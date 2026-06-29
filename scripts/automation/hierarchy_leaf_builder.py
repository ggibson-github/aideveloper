#!/usr/bin/env python3
"""Build complete hierarchy leaf documents (enrich + deepen, node-specific)."""

from __future__ import annotations

import importlib.util
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from hierarchy_completeness import item_id_from_path, list_leaf_paths, title_from_path  # noqa: E402
from hierarchy_queue_data import LEAVES, slug  # noqa: E402
from hierarchy_vision_context import find_tree_context, load_vision_lines, section_for_branch  # noqa: E402

_enrich_path = Path(__file__).resolve().parent / "enrich-hierarchy-docs.py"
_spec = importlib.util.spec_from_file_location("enrich_hierarchy_docs", _enrich_path)
_enrich = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(_enrich)

BRANCH_ARTIFACTS = _enrich.BRANCH_ARTIFACTS
BRANCH_PURPOSE = _enrich.BRANCH_PURPOSE
branch_for = _enrich.branch_for
generate_expanded_body = _enrich.generate_expanded_body
infer_state_fields = _enrich.infer_state_fields

from hierarchy_leaf_depth import (  # noqa: E402
    build_mermaid,
    challenge_body,
    concrete_implementation,
    edge_cases,
    failure_modes,
    json_example,
    branch_for,
)


def leaf_item(item_id: str, title: str | None = None) -> dict:
    t = title or LEAVES.get(item_id, item_id.replace("-", " "))
    parent = ".".join(item_id.split(".")[:-1]) if "." in item_id else item_id.rstrip("0123456789")
    if item_id.startswith("SEC-") or item_id.startswith("INTRO") or item_id.startswith("MASTER"):
        parent = item_id.split("-")[0] if "-" in item_id else "—"
    return {
        "id": item_id,
        "title": t,
        "parent": parent if parent != item_id else "—",
        "action": "document",
    }


def node_specific_behavior(item_id: str, title: str, branch: str, pass_num: int) -> list[str]:
    """Domain behavior for the node — never meta-expansion-process steps."""
    t = title.lower()
    steps: list[str] = []

    def add(*lines: str) -> None:
        steps.extend(lines)

    if item_id.startswith("A2.1") or "preflight" in t:
        add(
            "At pursuit turn start, run `python scripts/automation/check-pipeline-blocked.py`.",
            "Exit 0 (READY): proceed to execute exactly one pipeline skill phase.",
            "Exit 1 (BLOCKED): stop pursuit; dual-write structured H2 with stop reason.",
        )
    elif item_id == "A2.2" or ("execute" in t and "step" in t):
        add(
            "When preflight is READY, read `next_action` and `capability_class` via `route-tier.py`.",
            "Invoke the mapped skill once (implement, design, verify, etc.) — never batch multiple phases.",
            "Run task verify when `next_action` is implement-feature; write evidence via verify-router.",
            "Dual-write journal + state; increment `pursuit.steps_total`.",
        )
    elif "goal_verify" in t or item_id.startswith("G2"):
        add(
            "Resolve `goal.verify_command` from `state.goal` or active pack `F1.8` verify suite.",
            "Aggregate task evidence paths; fail closed if any required evidence missing.",
            "On exit 0: set `goal.state=verifying` then `hitl.pending=H3` when scope complete.",
            "On failure: block pursuit with H2; do not clear H3 automatically.",
        )
    elif item_id.startswith("D2") or "promotion_queue" in t:
        add(
            "Product turn completes → evaluate scheduler (K product steps per platform turn).",
            "Platform turn dequeues head of `platform.promotion_queue` unless D3.3 product blocked.",
            "Execute promotion work (playbook-keeper, script extraction, catalog row) to L1–L5 done.",
            "Dual-write queue drain result; re-enqueue if promotion partially complete.",
        )
    elif item_id.startswith("C1"):
        add(
            f"Register pipeline behavior for `{title}` in `docs/manifest/pipelines/`.",
            "Map `pipeline_id` to ordered skill phases and gates in manifest JSON/YAML.",
            "program-scoper or route-tier selects this pipeline for matching specs/features.",
        )
    elif item_id.startswith("F1") or (branch == "F" and "pack" in t):
        add(
            f"Define pack artifact for `{item_id}` under `template-packs/<pack-id>/`.",
            "Schema must be composable: company.yaml references roles, pipelines, verify suites.",
            "program-scoper binds pack; sets `state.company.pack_id` and `active_role`.",
        )
    elif item_id.startswith("E2") or "compose" in t:
        add(
            "Before S1+ work, Librarian/compose resolves capability to catalog components.",
            "Task card lists `Components used`; missing L0 triggers promotion_queue enqueue.",
            "Record divergence when not composing from catalog (B4.4).",
        )
    elif item_id.startswith("INTRO"):
        add(
            "At H1, the operator supplies a spec or charter; the approved plan reflects this summary—north star, scope, and minimal HITL (H1/H2/H3).",
            "All pursuit and plane specs assume three structural shifts: always-on pursuit until goals verify, parallel product and self-improvement work, and template-packs at company scale.",
            "When scope or stop behavior is ambiguous, agents resolve conflicts using this summary before inventing new policy.",
            "Downstream capabilities reference this framing so “done” means verified outcomes, not task theater.",
        )
    elif item_id.startswith("MASTER"):
        add(
            f"Plane {branch} groups related capabilities; this master summary orients readers before opening {branch}1–{branch}6 detail pages.",
            f"Each child capability under Plane {branch} must stay consistent with this plane’s role in pursuit, routing, or verification.",
            "Operators use master pages as reading order hints—not as separate runtime state.",
        )
    elif item_id.startswith("SEC-"):
        add(
            "This section documents cross-cutting architecture: pursuit flow, migration gaps, or release sequencing for the expert system.",
            "Implementers treat SEC rows as program backlog ordering, not as ad hoc prose.",
            "Release slices (SEC-15) map harness versions to shippable capability bundles.",
        )
    elif item_id.startswith("APP-"):
        add(
            "Appendix material sketches state fields, taxonomies, or operator views that support the planes without duplicating them.",
            "Readers consult appendices when implementing state.json, work classification, or operator dashboards.",
        )
    elif item_id.startswith("G1") or (branch == "G" and "verify" in t):
        add(
            "Run verify-router for task-level commands; persist log under `evidence/`.",
            "Set `last_verify=passed|failed` in state before advancing implement tasks.",
            "Block git-workflow push when evidence_required and verify not passed.",
        )
    else:
        # Timeline author derives steps from reader narrative; avoid generic implement boilerplate here.
        return []

    if pass_num >= 2:
        add(f"Pass {pass_num}: expand acceptance tests and named file paths for `{item_id}`.")
    if pass_num >= 3:
        add(f"Pass {pass_num}: cross-check parent index and SEC-15 release row for implement ordering.")

    add("On failure: structured H2 in journal; do not mark related queue item done.")
    return steps


def build_complete_leaf(item_id: str, title: str, vision_lines: list[str], pass_num: int = 1) -> str:
    """Full knowledge document: enrich base + deepen sections with node-specific behavior."""
    branch = branch_for(item_id)
    section = section_for_branch(item_id)
    tree = find_tree_context(item_id, vision_lines)
    parent = ".".join(item_id.split(".")[:-1]) if "." in item_id else "—"
    item = leaf_item(item_id, title)

    purpose = BRANCH_PURPOSE.get(branch, BRANCH_PURPOSE.get("meta", ""))
    artifacts = BRANCH_ARTIFACTS.get(branch, [])
    state_fields = infer_state_fields(item_id, title)
    behavior = node_specific_behavior(item_id, title, branch, pass_num)
    mermaid = build_mermaid(item_id, title)
    jex = json_example(item_id, title)
    edges = edge_cases(item_id, branch)
    while len(edges) < 4:
        edges.append(f"Edge case `{item_id}` variant {len(edges) + 1}: verify state dual-write before continuing pursuit.")
    fails = failure_modes(item_id)
    impl = concrete_implementation(item_id, title, branch)
    while len(impl) < 4:
        impl.append(f"Validate `{item_id}` against SEC-15 release checklist and parent index links.")

    if pass_num >= 2:
        impl.append(f"Document `{item_id}` in parent index with verify command and release tag.")
        edges.append(f"Pass {pass_num}: add regression test or evidence path specific to `{item_id}`.")
    if pass_num >= 3:
        impl.append(f"Add checklist row in SEC-15 release doc for `{item_id}`.")
        edges.append(f"Pass {pass_num}: cross-link related nodes in same branch index.")

    state_table = ""
    if state_fields:
        rows = "\n".join(f"| `{f}` | {typ} | {desc} |" for f, typ, desc in state_fields)
        state_table = f"""
## State / data fields

| Field | Type | Description |
|-------|------|-------------|
{rows}
"""

    art_list = "\n".join(f"- `{a}`" for a in artifacts[:6])
    behavior_md = "\n".join(f"{i}. {s}" for i, s in enumerate(behavior, 1))
    edge_md = "\n".join(f"- {e}" for e in edges)
    fail_md = "\n".join(f"- {f}" for f in fails)
    impl_md = "\n".join(f"{i}. {s}" for i, s in enumerate(impl, 1))

    release = (
        "v2.14" if branch == "A"
        else "v2.16" if branch == "D"
        else "v2.17" if branch == "E"
        else "v2.19" if branch == "F"
        else "v2.15"
    )

    if item_id.startswith("SEC-15"):
        deliverables = f"""
## Release deliverables (SEC-15)

- Schema: additive `state.json` fields only
- Scripts: S0 tools for {item_id}
- Skills/tests/docs per vision roadmap row
"""
    else:
        deliverables = ""
    parent_link = f"[{parent}-index]({parent}-index.md)" if parent and parent != "—" else parent

    body = f"""# {item_id}: {title}

**Parent:** {parent_link} · **Branch {branch}** · **Vision {section}** · **Release:** {release}

## Purpose

**{item_id}** defines **{title}** for the agent-driven expert system. {purpose}

## Scope

- Owns `{item_id}` only; siblings under `{parent}` must not duplicate this spec.
- Aligns with minimal HITL: H1 plan, H2 blocker, H3 sign-off ([INTRO-1.2](INTRO-1.2-human-touchpoint-contract-h1-h2-h3.md)).
- Conflicts resolve in favor of [full-automation-vision-and-hierarchy.md](../../full-automation-vision-and-hierarchy.md) {section}.

## Hierarchy context

```
{tree or f"{item_id} {title}"}
```

## Behavior / step logic

{behavior_md}

{mermaid}

## JSON example

{jex}

{state_table}
## Repo artifacts (this branch)

{art_list}

## Edge cases

{edge_md}

## Failure modes

{fail_md}

## Concrete implementation

{impl_md}
{deliverables}
## Verification

| Check | Command |
|-------|---------|
| Completeness | `python scripts/automation/audit-hierarchy-depth.py --strict --ids {item_id}` |
| Conformance | `python scripts/validate-workflow.py` |
| Task evidence | `python scripts/verify-router.py` when implement task exists |

## Dependencies

| Link | Why |
|------|-----|
| [full-automation-vision-and-hierarchy.md](../../full-automation-vision-and-hierarchy.md) {section} | Master hierarchy |
| [{parent}-index]({parent}-index.md) | Parent grouping |
| [genius-conductor-tiered-routing.md](../../genius-conductor-tiered-routing.md) | S0–S4 routing |

## Acceptance criteria

- [ ] `python scripts/automation/audit-hierarchy-depth.py --strict --ids {item_id}` passes
- [ ] Named script, skill, or test path exists or is listed in SEC-15 release row
- [ ] Linked from [{parent}-index]({parent}-index.md)
- [ ] `python scripts/validate-workflow.py` passes after implement

## Cross-links

- [hierarchy-expander SKILL](../../../.cursor/skills/hierarchy-expander/SKILL.md)
"""
    return body


def _append_depth_sections(body: str, item_id: str, title: str, branch: str, pass_num: int) -> str:
    mermaid = build_mermaid(item_id, title)
    extra = f"""
## Edge cases

{chr(10).join(f"- {e}" for e in edge_cases(item_id, branch))}

## Failure modes

{chr(10).join(f"- {f}" for f in failure_modes(item_id))}

## Concrete implementation

{chr(10).join(f"{i}. {s}" for i, s in enumerate(concrete_implementation(item_id, title, branch), 1))}

{mermaid}

## JSON example

{json_example(item_id, title)}
"""
    return body.rstrip() + extra


def write_leaf(path: Path, item_id: str, title: str, pass_num: int, *, challenge: bool = True, ledger_path: Path | None = None) -> None:
    from hierarchy_iteration_ledger import DEFAULT_LEDGER, record_node_iteration  # noqa: WPS433

    ledger = ledger_path or DEFAULT_LEDGER
    vision_lines = load_vision_lines()
    today = date.today().isoformat()
    body = build_complete_leaf(item_id, title, vision_lines, pass_num)
    if challenge:
        body = challenge_body(body, item_id, title)
    path.write_text(f"<!-- Complete pass {pass_num} {today} {item_id} -->\n\n{body}", encoding="utf-8")

    branch = branch_for(item_id)
    sources = [
        f"vision:{section_for_branch(item_id)}",
        f"branch:{branch}",
        "hierarchy_queue:LEAVES",
        "hierarchy_vision_context",
    ]
    if branch in BRANCH_ARTIFACTS:
        sources.extend(BRANCH_ARTIFACTS[branch][:3])
    record_node_iteration(
        item_id,
        pass_num=pass_num,
        sources=sources,
        path=str(path.relative_to(ROOT)),
        ledger_path=ledger,
    )


def resolve_leaf_path(out_dir: Path, item_id: str) -> Path | None:
    matches = list(out_dir.glob(f"{item_id}-*.md"))
    return matches[0] if matches else None
