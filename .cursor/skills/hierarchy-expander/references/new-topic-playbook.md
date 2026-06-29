# New topic playbook

Use when brainstorming a **new** hierarchy (not `full-automation`).

## 1. Write the hierarchy source

Create `documents/<topic>-vision-and-hierarchy.md`:

- Executive summary + north star
- ASCII tree(s) with stable node ids (`A1`, `A1.1`, … or your convention)
- Sections per branch
- Open decisions appendix (optional)

## 2. Register the topic

```bash
python scripts/automation/hierarchy-expander-run.py --topic my-product register \
  --source documents/my-product-vision-and-hierarchy.md \
  --title "My product brainstorming hierarchy"
```

This adds an entry to [hierarchy-topics.json](../../../docs/automation/hierarchy-topics.json) and scaffolds:

| Artifact | Path |
|----------|------|
| Queue | `docs/automation/my-product-expansion-queue.json` |
| Loop prompt | `docs/automation/my-product-expansion-prompt.md` |
| Output dir | `documents/plans/my-product/` |
| Ledger | `docs/automation/my-product-iteration-ledger.json` |
| Quality report | `docs/automation/my-product-quality-report.md` |

## 3. Initialize unified queue

```bash
python scripts/automation/hierarchy-expander-run.py --topic my-product init --mode bootstrap
```

**bootstrap** — queue contains `expand` nodes; agent/`/loop` adds children and leaf `document` items.

For large known trees (like full-automation), copy `hierarchy_queue_data.py` → `hierarchy_queue_data_my_product.py`, define `LEAVES`, set `queue_data_module` in registry, use `--mode full`.

## 4. Expand structure

```
/loop 3m Follow docs/automation/my-product-expansion-prompt.md
```

Or agent-driven: one queue item per turn until `EMPTY`.

## 5. Automate quality (required)

```bash
python scripts/automation/hierarchy-expander-run.py --topic my-product pipeline
python scripts/automation/hierarchy-expander-run.py --topic my-product certify
```

## 6. Human gate

Only after **certify exit 0**:

- User may read `my-product-quality-report.md`
- User sign-off on plan bundle (optional H3 pattern)

## Optional: rich leaf data module

For batch `full` mode without `/loop`:

1. Copy `scripts/automation/hierarchy_queue_data.py` → `hierarchy_queue_data_<topic>.py`
2. Fill `EXPAND_NODES`, `LEAVES`, `STANDALONE_DOCUMENTS`
3. Add `"queue_data_module": "hierarchy_queue_data_<topic>"` to topic registry
4. Wire `init-hierarchy-queue.py` to import module (future: `--queue-data-module` flag)

Until then: **bootstrap + loop + pipeline** is the supported path for new topics.
