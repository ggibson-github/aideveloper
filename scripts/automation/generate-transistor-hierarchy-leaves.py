#!/usr/bin/env python3
"""Generate transistor hierarchy leaf markdown files from transistor_hierarchy_data.py."""

from __future__ import annotations

import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from hierarchy_queue_data import slug  # noqa: E402
from transistor_hierarchy_data import TRANSISTOR_LEAVES  # noqa: E402

OUT = ROOT / "documents" / "plans" / "full-automation"
TODAY = date.today().isoformat()

BRANCH_VISION = {
    "INTRO": "§19",
    "SEC": "§19",
    "B": "§4",
    "C": "§5",
    "D": "§6",
    "E": "§7",
    "F": "§8",
    "G": "§9",
    "H": "§10",
    "I": "§11",
}


def branch_for(item_id: str) -> str:
    if item_id.startswith("INTRO"):
        return "INTRO"
    if item_id.startswith("SEC"):
        return "SEC"
    if item_id.startswith("APP"):
        return "APP"
    if item_id.startswith("MASTER"):
        return "MASTER"
    return item_id[0]


def parent_link(parent: str) -> str:
    if parent in ("INTRO", "SEC", "MASTER", "APP-A", "—"):
        if parent == "—":
            return "—"
        return f"[{parent}-index]({parent}-index.md)"
    return f"[{parent}-index]({parent}-index.md)"


def vision_anchor(branch: str) -> str:
    section = BRANCH_VISION.get(branch, "§19")
    names = {
        "INTRO": "Transistor & generator workflow model",
        "SEC": "Transistor & generator workflow model",
        "B": "Branch B — Cognition & routing plane",
        "C": "Branch C — Product execution plane",
        "D": "Branch D — Platform evolution plane",
        "E": "Branch E — Knowledge & composition plane",
        "F": "Branch F — Organization plane",
        "G": "Branch G — Verification & quality plane",
        "H": "Branch H — Persistence & state plane",
        "I": "Branch I — Runtime & integration plane",
    }
    name = names.get(branch, "Transistor model")
    anchor = name.lower().replace(" ", "-").replace("—", "").replace("&", "")
    anchor = re.sub(r"[^a-z0-9-]", "", anchor)
    return f"[Vision {section} — {name}](../../full-automation-vision-and-hierarchy.md#{anchor})"


def build_leaf(item_id: str, data: dict) -> str:
    title = data["title"]
    parent = data["parent"]
    release = data.get("release", "v2.24")
    branch = branch_for(item_id)
    narrative = data["narrative"]
    steps = data["steps"]
    slug_part = slug(title)
    parent_ref = parent_link(parent)

    steps_md = "\n".join(f"{i}. {s}" for i, s in enumerate(steps, 1))
    hierarchy_line = f"│   └── {item_id} {title}" if "." in item_id else f"{item_id} {title}"

    release_section = ""
    if item_id.startswith("SEC-15"):
        release_section = """
## Release deliverables (SEC-15)

- Schema: additive `state.json` and workflow/transistor schemas
- Scripts: S0 tools listed in behavior steps
- Skills/tests/docs per SEC-18 roadmap row
"""

    return f"""# {item_id}: {title}

**Parent:** {parent_ref} · **Branch {branch}** · **Vision §19** · **Release:** {release}

## Reader narrative
<!-- prose-source: agent transistor-expansion {TODAY} -->

{narrative}

See {vision_anchor(branch)} and [SEC-18-transistor-model-a-to-z](SEC-18-transistor-model-a-to-z.md).

## Purpose

{item_id} defines {title.lower()} for the agent-driven expert system. Transistor & generator workflow model (§19).
## Scope

- Owns `{item_id}` only; siblings under `{parent}` must not duplicate this spec.
- Aligns with minimal HITL: H1 plan, H2 blocker, H3 sign-off ([INTRO-1.2](INTRO-1.2-human-touchpoint-contract-h1-h2-h3.md)).
- Conflicts resolve in favor of {vision_anchor(branch)}.
## Hierarchy context

```
{hierarchy_line}
```

## Behavior / step logic
<!-- timeline-source: agent transistor-expansion {TODAY} -->

{steps_md}

```mermaid
flowchart TD
  compose[Compose workflow] --> validate[validate-workflow-dag S0]
  validate -->|pass| exec[Execute one node]
  exec --> nodeVerify[Transistor verify]
  nodeVerify -->|pass| next[Advance active_workflow]
  nodeVerify -->|fail| h2[H2 or retry gate]
  next --> goalVerify[goal_verify rollup]
```

## JSON example

```json
{{
  "node": "{item_id}",
  "description": "{title.lower()}",
  "state": {{ "ref": "APP-B-state-json-sketch.md", "active_workflow": "H1.7" }},
  "implemented_in_release": "{release}+"
}}
```

## Repo artifacts (this branch)

- `docs/platform/transistors/`
- `docs/platform/schemas/transistor.v1.json`
- `docs/platform/schemas/workflow-dag.v1.json`
- `docs/workflows/`
- `scripts/automation/list-transistors.py`
- `scripts/automation/validate-workflow-dag.py`
{release_section}
## Edge cases

- Operator closes laptop mid-loop — state.json must resume from last good dual-write including active_workflow.
- Transistor version bump mid-pursuit — E5.4 marks workflow stale; re-validate before next node.
- L0 waiver node without promotion progress — D3.3 priority boost then H2 if threshold exceeded.
- Pack overlay id collision — F5.4 semver fork per D5.3, not silent overwrite.
- Parallel branch join missing typed input — validate-workflow-dag fails at compose time.

## Failure modes

- **Fuzzy chain:** Implement without workflow_node_id when C6.1 applies → G5.8 blocks at preflight.
- **False complete:** Node marked done without transistor verify evidence → G2.5 goal_verify fails closed.
- **Stale workflow:** active_workflow.validation_hash mismatch → E5.4 reconcile before advance.
- **Duplicate transistor:** G5.6 list-transistors --check-duplicates rejects promotion.
- **Scope bleed:** Worker runs transistors outside bound node → C6.3 conformance failure.

## Concrete implementation

1. Map `{item_id}` to release row in [SEC-15-index](SEC-15-index.md) ({release}).
2. Implement behavior per [SEC-18](SEC-18-transistor-model-a-to-z.md) acceptance checklist.
3. Add or extend S0 script when behavior is file-derived.
4. Add unit test under `tests/unit/` when script exists.
5. Link from [{parent}-index]({parent}-index.md).
6. Run `python scripts/validate-workflow.py` after implement.

## Verification

| Check | Command |
|-------|---------|
| Completeness | `python scripts/automation/audit-hierarchy-depth.py --strict --ids {item_id}` |
| Conformance | `python scripts/validate-workflow.py` |
| DAG validity | `python scripts/automation/validate-workflow-dag.py` when workflow exists |
| Task evidence | `python scripts/verify-router.py` when implement task exists |

## Dependencies

| Link | Why |
|------|-----|
| [SEC-18-transistor-model-a-to-z](SEC-18-transistor-model-a-to-z.md) | A–Z authority |
| [full-automation-vision-and-hierarchy.md](../../full-automation-vision-and-hierarchy.md) §19 | Master hierarchy |
| [{parent}-index]({parent}-index.md) | Parent grouping |
| [genius-conductor-tiered-routing.md](../../genius-conductor-tiered-routing.md) | S0–S4 routing |

## Acceptance criteria

- [ ] `python scripts/automation/audit-hierarchy-depth.py --strict --ids {item_id}` passes
- [ ] Named script, skill, or test path exists or is listed in SEC-15 release row
- [ ] Linked from [{parent}-index]({parent}-index.md)
- [ ] Aligned with SEC-18 transistor model
- [ ] `python scripts/validate-workflow.py` passes after implement

## Cross-links

- [hierarchy-expander SKILL](../../../.cursor/skills/hierarchy-expander/SKILL.md)
- [INTRO-2-transistor-building-blocks-north-star](INTRO-2-transistor-building-blocks-north-star.md)
"""


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for item_id, data in sorted(TRANSISTOR_LEAVES.items()):
        title = data["title"]
        filename = f"{item_id}-{slug(title)}.md"
        path = OUT / filename
        body = build_leaf(item_id, data)
        path.write_text(f"<!-- Complete pass 1 {TODAY} {item_id} -->\n\n{body}", encoding="utf-8")
        print(f"Wrote {path.relative_to(ROOT)}")
    print(f"Generated {len(TRANSISTOR_LEAVES)} leaf documents.")


if __name__ == "__main__":
    main()
