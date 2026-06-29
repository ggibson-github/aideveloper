# Expand hierarchy (/expand-hierarchy)

Uses the **hierarchy-expander** skill and unified CLI.

## Certified topic (read only after certify)

```bash
python scripts/automation/hierarchy-expander-run.py --topic full-automation certify
```

## New brainstorming session

```bash
python scripts/automation/hierarchy-expander-run.py --topic <TOPIC> register --source documents/<hierarchy>.md
python scripts/automation/hierarchy-expander-run.py --topic <TOPIC> init --mode bootstrap
# /loop expand until EMPTY (optional)
python scripts/automation/hierarchy-expander-run.py --topic <TOPIC> pipeline
python scripts/automation/hierarchy-expander-run.py --topic <TOPIC> certify
python scripts/automation/hierarchy-expander-run.py --topic <TOPIC> publish
```

## Status

```bash
python scripts/automation/hierarchy-expander-run.py --topic <TOPIC> status
python scripts/automation/hierarchy-expander-run.py list
```

Full skill: `.cursor/skills/hierarchy-expander/SKILL.md`
