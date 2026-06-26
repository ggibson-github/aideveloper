# Facts index

Topic → file mapping for project facts (URLs, SQL, contacts, Slack excerpts, etc.). The agent and hooks use this file to find facts without searching the whole repo.

| Topic | File | Keywords |
|-------|------|----------|
| Misc / uncategorized | [captured.md](captured.md) | misc, snippet, note |
| API / endpoints | api.md | api, endpoint, staging, prod, auth, base url |
| Database | db.md | db, database, sql, schema, connection |
| Team / contacts | team.md | team, slack, contact, on-call |

**Notes**

- Rows for `api.md`, `db.md`, and `team.md` are created when the first fact for that topic is saved (see **remember** skill).
- Each fact entry uses YAML frontmatter with `topics: [api, staging]` for routing and hook matching.
- Search keywords in this table and in journal **Context files** before guessing external configuration.
