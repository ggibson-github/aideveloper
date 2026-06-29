# Hierarchy quality certification report

**Generated:** 2026-06-28  
**Status:** CERTIFIED — safe for human review  
**Source:** [documents/full-automation-vision-and-hierarchy.md](../../documents/full-automation-vision-and-hierarchy.md)

## Executive guarantee

Human reading time is warranted **only** when `certified_for_human_review: true`.
That requires **every leaf** to pass **all six quality dimensions** and the **aggregate score**.

## Hierarchy structure

| Metric | Value |
|--------|-------|
| Top-level branches | 10 (A, B, C, D, E, F, G, H, I, meta) |
| Expand nodes | 50 |
| Leaf documents | 239 / 228 expected |
| Index files | 57 |
| Max node id depth | 5 |
| Total markdown files | 298 |

## Iteration proof (every node processed)

| Metric | Value |
|--------|-------|
| Nodes in iteration ledger | 224 |
| Documents with Complete pass marker | 239 |
| Pipeline passes recorded | 3 |
| Missing from ledger | 0 |
| Never iterated | 0 |

## Aggregate quality

**Hierarchy aggregate score: 99.6/100** (min 85)

| Dimension | Avg score | Min required | Weight |
|-----------|-----------|--------------|--------|
| structure | 100.0 | 70 | 15% |
| specificity | 99.8 | 70 | 20% |
| research | 98.5 | 70 | 25% |
| depth | 100.0 | 70 | 20% |
| iteration | 100.0 | 70 | 10% |
| review | 100.0 | 70 | 10% |

- **Nodes certified:** 239 / 239
- **Certification rate:** 100.0%

## Branch breakdown

| Branch | Nodes | Avg aggregate | Research avg | Certified |
|--------|-------|---------------|--------------|-----------|
| A | 27 | 98.5 | 94.1 | 27/27 |
| B | 23 | 100.0 | 100.0 | 23/23 |
| C | 20 | 100.0 | 100.0 | 20/20 |
| D | 30 | 99.7 | 99.4 | 30/30 |
| E | 18 | 99.9 | 100.0 | 18/18 |
| F | 25 | 99.5 | 98.4 | 25/25 |
| G | 24 | 99.6 | 98.8 | 24/24 |
| H | 11 | 99.8 | 100.0 | 11/11 |
| I | 15 | 100.0 | 100.0 | 15/15 |
| J | 6 | 99.8 | 100.0 | 6/6 |
| meta | 40 | 99.2 | 97.0 | 40/40 |

## Verify

```bash
python scripts/automation/generate-hierarchy-quality-report.py
python scripts/automation/run-hierarchy-full-pipeline.py --verify-only
```

Full per-node scores: `docs/automation/hierarchy-quality-report.json` → `all_nodes[]`.
