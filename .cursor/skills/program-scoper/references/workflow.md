# Program scoper workflow

1. Run `python scripts/route-tier.py --apply` after updating `next_action`.
2. Milestone gate: record approval in journal or `docs/decisions/`; clear `milestone_approved` from `gates_pending_program`.
3. Then `next_action: run integration-manifest-keeper`.
