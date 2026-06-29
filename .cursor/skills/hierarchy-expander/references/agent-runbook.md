# Agent runbook — hierarchy expander

Execute these steps when the **hierarchy-expander** skill is active. Do not skip certification.

## 0. Resolve topic

```bash
python scripts/automation/hierarchy-expander-run.py list
```

Use `--topic <id>` from registry, or `register` for new hierarchies.

## 1. New hierarchy only — register + init

```bash
python scripts/automation/hierarchy-expander-run.py --topic <TOPIC> register \
  --source documents/<hierarchy>.md \
  --title "Human title"

python scripts/automation/hierarchy-expander-run.py --topic <TOPIC> init --mode bootstrap
```

- **`bootstrap`**: expand nodes only; `/loop` or agent appends leaves at runtime (most new topics)
- **`full`**: pre-seed all leaves (requires `queue_data_module` in registry, e.g. `full-automation`)

## 2. Structural expand (if queue has pending items)

Preflight:

```bash
python scripts/automation/check-hierarchy-queue.py --queue <queue-from-registry>
```

**Option A — `/loop` (highest quality per node during expand):**

```
/loop 3m Follow <prompt-from-registry> — one queue item per wake. Run check-hierarchy-queue.py first.
```

Stop when checker prints `EMPTY` or agent says `HIERARCHY_EXPANSION_COMPLETE`.

**Option B — batch (full-automation topic only):**

```bash
python scripts/automation/generate-vision-expansion-docs.py
python scripts/automation/enrich-hierarchy-docs.py
```

## 3. Full pipeline — three passes by default

```bash
python scripts/automation/hierarchy-expander-run.py --topic <TOPIC> pipeline
```

Default: **3 full iterations** on every leaf. Operator may request more: `--max-passes 5` or unlimited `--max-passes 0`.

Each pass:

1. Rebuilds **100% of leaf documents**
2. Records **iteration ledger** (sources gathered per node)
3. Runs **six-dimension quality scoring**
4. Exits when **certified** and **passes ≥ min_passes** (default 3)

**Do not** tell the user to read plan documents before this completes with exit 0.

## 4. Certify (gate)

```bash
python scripts/automation/hierarchy-expander-run.py --topic <TOPIC> certify
```

If exit **non-zero**:

- Open `<topic>-quality-report.json` → `failed_nodes[]`
- Re-run `pipeline`
- Do **not** advance to human sign-off

## 5. Deliver to user

Present:

1. **Quality report markdown** (certificate)
2. **Aggregate score** + branch table
3. **Sign-off bundle** path (if topic has one)
4. **HTML site** path (`html-site/index.html`) — corporate narrative edition
5. Statement: *"Certified — safe to read; N nodes, aggregate score X"*

## 6. Publish HTML (after certify)

```bash
python scripts/automation/hierarchy-expander-run.py --topic <TOPIC> publish
```

Output: `<output-dir>/html-site/` — open `index.html` locally, no server.

## 7. Re-brainstorm / vision changed

After hierarchy source edit:

```bash
python scripts/automation/hierarchy-expander-run.py --topic <TOPIC> pipeline
python scripts/automation/hierarchy-expander-run.py --topic <TOPIC> certify
```

Certification must pass again before human reading.

## Anti-patterns

- Reading dozens of docs before `certify` exit 0
- Separate queues per branch
- Using `journal/state.json` / implement pipeline for planning-only work
- Skipping pipeline because structural `EMPTY` is true (structure ≠ quality)
