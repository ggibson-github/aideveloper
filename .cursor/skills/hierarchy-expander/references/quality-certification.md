# Hierarchy quality certification

Human reading time is **only** warranted when the machine issues **CERTIFIED**.

## One command before you read (any topic)

```bash
python scripts/automation/hierarchy-expander-run.py --topic <TOPIC> certify
```

Exit **0** + `certified_for_human_review: true` + `nodes_failed: 0` = guarantee met.

Open the topic's quality report (paths in [hierarchy-topics.json](../../../docs/automation/hierarchy-topics.json)):

- `docs/automation/<topic>-quality-report.md` — human summary
- `docs/automation/<topic>-quality-report.json` — every node scored

Reference topic:

```bash
python scripts/automation/hierarchy-expander-run.py --topic full-automation certify
```

## What is guaranteed (machine-enforced)

| Guarantee | How |
|-----------|-----|
| **Every node iterated** | **3 full passes** by default; ledger records pass count + sources |
| **Every node researched** | `research` dimension scores repo paths, vision links, skills, scripts, state schema refs |
| **Every node scored** | Six dimensions × weights → per-node aggregate |
| **Hierarchy aggregate** | Mean of all node aggregates; must be ≥ 85 |
| **No weak nodes** | Each dimension ≥ 70 on **every** leaf; zero failed nodes |

### Quality dimensions (weights)

| Dimension | Weight | Measures |
|-----------|--------|----------|
| structure | 15% | Required sections, mermaid, JSON, no meta-scaffold |
| specificity | 20% | Node id + title terms in behavior; no generic fallback |
| research | 25% | Vision, scripts, skills, state, manifest refs gathered |
| depth | 20% | Lines, words, edge cases, implementation steps |
| iteration | 10% | `Complete pass N` marker + ledger (**100 at pass 3+**) |
| review | 10% | Adversarial review + revisions applied |

## Full pipeline (default 3 passes)

```bash
python scripts/automation/hierarchy-expander-run.py --topic <TOPIC> pipeline
```

Each pass:

1. **Iterate 100% of leaves**
2. **Record ledger** (sources per node)
3. **Generate quality report** at topic-specific paths
4. Exit when **certified** and **passes ≥ 3** (default max 3)

Operator override: `--max-passes N` (use `0` for unlimited until certified after min 3).

## If not certified

Do **not** read dozens of docs. Fix:

```bash
python scripts/automation/hierarchy-expander-run.py --topic <TOPIC> pipeline
python scripts/automation/hierarchy-expander-run.py --topic <TOPIC> certify
```

Failed nodes listed in report → `failed_nodes[]` with `gaps[]`.

## Re-certify after vision changes

Re-run `pipeline` then `certify`. Only read when certified again.

## New topics

See [new-topic-playbook.md](new-topic-playbook.md).
