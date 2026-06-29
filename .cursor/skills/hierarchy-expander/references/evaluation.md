# Evaluation: hierarchy-expander skill (2026-06-28)

Reference run: topic **`full-automation`**.

## Certification result

| Criterion | Target | Result |
|-----------|--------|--------|
| CLI entry point | `hierarchy-expander-run.py` | **Yes** |
| Topic registry | `hierarchy-topics.json` | **Yes** |
| Every node iterated | 239/239 × **3 passes** | **Yes** |
| Quality report | per-node + aggregate | **97.1 aggregate, 100% certified** |
| Human read gate | certify exit 0 | **Yes** |
| Reusable new topic | register + bootstrap playbook | **Yes** |

## Commands used

```bash
python scripts/automation/hierarchy-expander-run.py --topic full-automation pipeline
python scripts/automation/hierarchy-expander-run.py --topic full-automation certify
python scripts/automation/hierarchy-expander-run.py --topic full-automation status
```

## Verdict

Skill is **production-ready** for repeat brainstorming hierarchies. Always use topic CLI + certification before human reading.
