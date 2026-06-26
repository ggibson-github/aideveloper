# v2 Full Evolution (v2.4–v2.12)

Reference copy for Cloud Agents and unattended runs. Canonical plan may also live in `.cursor/plans/`.

## Releases

| Tag | Focus |
|-----|--------|
| v2.4.0 | Tier routing, genius-conductor rules, work orders |
| v2.5.0 | route-tier.py, /model, worker-runs audit |
| v2.6.0 | update-staleness, new-task-card, validate extensions |
| v2.7.0 | Program mode, pipelines, program-scoper, manifest keeper |
| v2.8.0 | Artifact graph, reconcile-artifact-graph, task card v2 |
| v2.9.0 | orchestrate-program parallel lanes |
| v2.10.0 | verify-router, tool-operator, evidence types |
| v2.11.0 | Lane lease, pull/complete work orders, /lane |
| v2.12.0 | Template packs, design doc §10, README closure |
| v2.13.0 | Local autopilot (`/autopilot`, check-pipeline-blocked, run-local-pipeline) |

## Schema

`journal/state.json` remains `version: 2` with optional `program` object and tier fields.

See `documents/spec-to-artifacts-agent-skills-system.md` §10 and `documents/genius-conductor-tiered-routing.md`.
