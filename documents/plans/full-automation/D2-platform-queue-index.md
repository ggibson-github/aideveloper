# D2: Platform queue (promotion_queue)

**Parent:** D · **Branch D:** Platform evolution plane

## Purpose

Maintain a **parallel backlog of reuse work** (`state.platform.promotion_queue[]`) so the agent builds the internal platform (scripts, playbooks, skills) **without blocking product turns**. Product and platform share the conductor; scheduling policy (D3) decides when to drain the queue.

## Item schema

```json
{
  "id": "promo-001",
  "source": "task-012 / manual shell in evidence log",
  "target_level": "L2",
  "priority": 50,
  "effort_class": "S1",
  "reason": "same pytest invocation 3× in task cards",
  "created_at": "2026-06-28T12:00:00Z"
}
```

## Enqueue triggers (see child docs D2.1.x)

| Trigger | Typical target_level |
|---------|---------------------|
| Same manual command 2× | L1 playbook |
| Pattern in N task cards | L2 script |
| Worker flags repetition | L1 or L2 |
| S4 escalation post-mortem | L3 skill wrapper |

## Dequeue semantics

1. Conductor peeks head of queue (FIFO unless D3 priority override).
2. **Platform turn:** spawn economy worker or run playbook-keeper / script extraction (D4).
3. On platform DoD (D6): mark promo item done; regenerate catalog (E1.7).
4. Never dequeue platform work if product is blocked on missing catalog entry for **current** task (D3.3 priority cut).

## State fields

```json
"platform": {
  "promotion_queue": [],
  "drain_policy": { "product_steps_per_platform_turn": 5 },
  "last_drain_at": null
}
```

## Children

| Id | Topic |
|----|-------|
| [D2.1.1](D2.1.1-enqueue-repeated-manual-command-2x.md) | Repeated command |
| [D2.1.2](D2.1.2-enqueue-worker-flags-repetition.md) | Worker flag |
| [D2.1.3](D2.1.3-enqueue-verify-pattern-n-task-cards.md) | Task card pattern |
| [D2.1.4](D2.1.4-enqueue-conductor-post-mortem-escalation.md) | Escalation post-mortem |
| [D2.2](D2.2-platform-queue-item-schema.md) | Schema detail |
| [D2.3](D2.3-dequeue-platform-turn-not-product.md) | Dequeue rules |

## Acceptance criteria

- [ ] Product `next_action` never waits solely because platform queue non-empty
- [ ] Queue persisted in state.json; survives session restart
- [ ] Promotion items traceable to source task/evidence

## Open questions

- Persist queue in JSON file vs state only (proposed: state only; export in dashboard)
