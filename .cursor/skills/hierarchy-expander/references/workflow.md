# Hierarchy expander workflow

See [agent-runbook.md](agent-runbook.md) for agent steps. Summary:

```
register → init → [loop expand until EMPTY] → pipeline (3 passes) → certify → human read
```

**Entry point:** `python scripts/automation/hierarchy-expander-run.py --topic <TOPIC> <subcommand>`

Certification gate: [quality-certification.md](quality-certification.md)

New topics: [new-topic-playbook.md](new-topic-playbook.md)
