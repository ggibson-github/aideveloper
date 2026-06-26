---
name: reconcile-artifact-graph
description: >-
  Marks program artifact graph nodes stale when dependencies change.
  Use when program.artifact_graph is set or next_action reconcile-artifact-graph.
---

# Reconcile Artifact Graph

## When to use

- Manifest or rig spec changed in program mode
- `next_action: reconcile-artifact-graph`

## Instructions

1. Read `program.artifact_graph` from state (default `program/manifest/artifact-graph.json`).
2. Run graph stale logic (extend `scripts/update-staleness.py` pattern or manual reconcile).
3. Update `stale` map in artifact graph JSON.
4. Set dependent lane `blocked_on` if integration artifacts stale.

See **reconcile-stale** for software `docs/manifest/staleness.json`.
