# Model tier (/model)

Show **capability class**, **model tier**, **spawn_workers**, and policy recommendation from `journal/state.json` and `docs/operator/model-policy.json`.

Run deterministic routing:

```bash
python scripts/route-tier.py
python scripts/route-tier.py --apply
```

## Operator guidance

- **Genius session recommended** when `genius_session_recommended` is true—stay on Fable (or top tier) as conductor; spawn economy workers for implement.
- **model_escalation** true after failed verify—parent handles retry; do not spawn economy worker for same failure without review.
- Parent Composer model is **not** auto-switched; pick Genius once per orchestration session.

See `documents/genius-conductor-tiered-routing.md`.
