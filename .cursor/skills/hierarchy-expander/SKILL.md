---
name: hierarchy-expander
description: >-
  Expand and certify any brainstorming hierarchy end-to-end: register topic,
  unified queue, iterate every node, quality score per document and aggregate,
  certification report before human reading. Use for hierarchy expansion,
  vision queues, deep planning backlogs, or /expand-hierarchy.
---

# Hierarchy Expander

Turn a **brainstorming hierarchy** into a **certified plan tree on disk** — repeatable for any topic.

**Do not use** `journal/state.json` or `/autopilot` unless explicitly crossing into SDLC implement.

## When to use

- New or updated `documents/*-vision-and-hierarchy.md` (or similar)
- User asks to **expand the hierarchy**, **brainstorm to documents**, **certify the plan tree**
- User runs **`/expand-hierarchy`** or names this skill

## Guarantee model (non-negotiable)

Human reading time is allowed **only after machine certification**:

```bash
python scripts/automation/hierarchy-expander-run.py --topic <TOPIC> certify
```

Required: exit **0**, `"certified_for_human_review": true`, `"nodes_failed": 0`.

Open: `docs/automation/<topic>-quality-report.md` (or topic path in [hierarchy-topics.json](../../../docs/automation/hierarchy-topics.json)).

See [references/quality-certification.md](references/quality-certification.md).

## Agent runbook (follow in order)

When this skill is invoked, execute [references/agent-runbook.md](references/agent-runbook.md):

1. **Register or resolve topic** → `hierarchy-expander-run.py list` / `register`
2. **Init queue** (new topic) → `init --mode bootstrap|full`
3. **Structural expand** (if queue has pending) → `/loop` or batch scripts
4. **Full pipeline** → `pipeline` (**3 passes** by default; iterates **100% of leaves** each pass, then **prose editor** on every leaf)
5. **Agent prose** (book edition) → `prose-agent queue` then `prose-agent run-sdk` — or spawn Cursor workers per group with briefs from queue JSON. Template prose is fallback only; agent narratives are preserved (`<!-- prose-source: agent -->`).
6. **Certify** → `certify` — stop if not certified; re-run `pipeline` if needed
7. **Present** quality report + sign-off bundle — **never** ask user to read docs before certify passes
8. **Publish HTML** → `publish` — corporate static site in `html-site/` (after certify)

## Unified CLI (always use this)

```bash
python scripts/automation/hierarchy-expander-run.py list
python scripts/automation/hierarchy-expander-run.py --topic <TOPIC> register --source documents/<hierarchy>.md
python scripts/automation/hierarchy-expander-run.py --topic <TOPIC> init --mode bootstrap
python scripts/automation/hierarchy-expander-run.py --topic <TOPIC> pipeline
python scripts/automation/hierarchy-expander-run.py --topic <TOPIC> certify
python scripts/automation/hierarchy-expander-run.py --topic <TOPIC> publish
python scripts/automation/hierarchy-expander-run.py --topic <TOPIC> status
```

| Subcommand | Purpose |
|------------|---------|
| `list` | Registered topics |
| `register` | Add topic to `hierarchy-topics.json` + scaffold prompt |
| `init` | Create unified queue JSON |
| `pipeline` | **3 full passes** by default → ledger → score → certify |
| `certify` | Quality report only (gate before human reading) |
| `publish` | Static HTML site (corporate narrative + charts + diagrams) |
| `status` | Certification + structure summary |

## New brainstorming hierarchy

Full playbook: [references/new-topic-playbook.md](references/new-topic-playbook.md).

Short path:

1. Write hierarchy markdown (`documents/<topic>-vision-and-hierarchy.md`)
2. `register` + `init --mode bootstrap` (or `full` if `hierarchy_queue_data_<topic>.py` exists)
3. Optional `/loop` with prompt from topic registry for agent-written leaves
4. **`pipeline`** (default **3 passes**) then **`certify`**
5. Human reads **only** after `certify` exit 0

### Pass count (operator override)

Default: **3 full iterations** on every leaf (matches iteration quality score of 100).

```bash
# More passes (operator request)
python scripts/automation/hierarchy-expander-run.py --topic <TOPIC> pipeline --max-passes 5

# Unlimited until certified (after min 3)
python scripts/automation/hierarchy-expander-run.py --topic <TOPIC> pipeline --max-passes 0
```

## Reference topic (this repo)

```bash
python scripts/automation/hierarchy-expander-run.py --topic full-automation status
python scripts/automation/hierarchy-expander-run.py --topic full-automation certify
python scripts/automation/hierarchy-expander-run.py --topic full-automation publish
```

Open `documents/plans/full-automation/html-site/index.html` in a browser (no server).

- Source: `documents/full-automation-vision-and-hierarchy.md`
- Output: `documents/plans/full-automation/` (239 leaves)
- Registry: [hierarchy-topics.json](../../../docs/automation/hierarchy-topics.json)

## Quality dimensions (per node → aggregate)

| Dimension | Weight | What it measures |
|-----------|--------|------------------|
| structure | 15% | Sections, mermaid, JSON, no scaffold |
| specificity | 20% | Node id + title in behavior |
| research | 25% | Vision, scripts, skills, state, manifest refs |
| depth | 20% | Lines, words, edge cases, impl steps |
| iteration | 10% | Complete pass marker + ledger (**100 at pass 3+**) |
| review | 10% | Adversarial review + revisions |

**Per node:** all dimensions ≥ 70, aggregate ≥ 85. **Hierarchy:** mean aggregate ≥ 85, zero failures.

## One unified queue (required)

- **One** `items[]` for the entire hierarchy — never per-branch queue files
- FIFO across branches until checker `EMPTY` (structural phase)
- Certification phase uses **pipeline** (all leaves every pass)

## Files and scripts

| Path | Role |
|------|------|
| [hierarchy-topics.json](../../../docs/automation/hierarchy-topics.json) | Topic registry (paths per hierarchy) |
| `scripts/automation/hierarchy-expander-run.py` | **Entry point** — use this |
| `scripts/automation/hierarchy_topic_config.py` | Path resolution |
| `scripts/automation/run-hierarchy-full-pipeline.py` | Iterate all + prose editor + certify loop |
| `scripts/automation/hierarchy_prose_editor.py` | Writer/critic pass — links §N, S0, capability specs |
| `scripts/automation/hierarchy_prose.py` | Reader prose normalization for markdown + HTML |
| `scripts/automation/generate-hierarchy-quality-report.py` | Certification report |
| `scripts/automation/hierarchy_quality.py` | Six-dimension scoring |
| `scripts/automation/hierarchy_iteration_ledger.py` | Per-node iteration proof |
| `scripts/automation/hierarchy-html-publish.py` | Static HTML publication |
| `scripts/automation/hierarchy_html_rules.py` | Generic HTML publication rules (subject-only, glossary surfaces) |
| `scripts/automation/hierarchy_html_config.py` | Site config + branch meta (JSON overlays) |
| `scripts/automation/hierarchy_leaf_builder.py` | Node document builder |
| `docs/automation/templates/hierarchy-expansion/` | Prompt + queue templates |

## Operator setup

- Auto-run terminal for S0 scripts
- Genius-tier for `/loop` expand nodes with architectural ambiguity
- `/loop` is local IDE only

## References

- [html-publication.md](references/html-publication.md) — static corporate HTML site
- [agent-runbook.md](references/agent-runbook.md) — step-by-step when skill runs
- [new-topic-playbook.md](references/new-topic-playbook.md) — new hierarchy from scratch
- [quality-certification.md](references/quality-certification.md) — guarantee details
- [workflow.md](references/workflow.md) — phase diagram
- [queue-schema.md](references/queue-schema.md) — queue JSON schema
- [evaluation.md](references/evaluation.md) — full-automation reference run
