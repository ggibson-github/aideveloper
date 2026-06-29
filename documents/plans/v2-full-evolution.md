# v2 Full Evolution (v2.4–v2.28)



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

| v2.14.0 | Goal model, goal_verify, extended state.goal |

| v2.15.0 | goal_autopilot pursuit loop, self-gate HLD/DD |

| v2.16.0 | Platform promotion_queue, scheduler K-turn drain |

| v2.17.0 | Catalog compose-first, list-components, CATALOG.md |

| v2.18.0 | Staleness graph platform nodes |

| v2.19.0 | Company pack schema, active_role |

| v2.20.0 | Game studio pack reference |

| v2.21.0 | Data platform pack reference |

| v2.22.0 | Cross-pack `_shared` library |

| v2.23.0 | Operator polish, H2 audit, dashboard goal + queue |

| v2.24.0 | **Transistor** schema, registry, list-transistors, L6 promotion |

| v2.25.0 | Workflow DAG schema, validate-workflow-dag, workflow-compose phase |

| v2.26.0 | workflow-composer skill, active_workflow state, one-node-per-turn |

| v2.27.0 | Pack workflow templates, _shared transistors, parallel branches |

| v2.28.0 | Transistor maturity dashboard, fuzzy-chain metrics |



## Schema



`journal/state.json` remains `version: 2` with optional `program` object, tier fields, and `pursuit.active_workflow` (v2.26+).



## Transistor model



Authoritative A–Z: [full-automation/SEC-18-transistor-model-a-to-z-reference.md](full-automation/SEC-18-transistor-model-a-to-z-reference.md)  

North star: [full-automation/INTRO-2-transistor-building-blocks-north-star.md](full-automation/INTRO-2-transistor-building-blocks-north-star.md)



See `documents/spec-to-artifacts-agent-skills-system.md` §10 and `documents/genius-conductor-tiered-routing.md`.

