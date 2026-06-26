---
name: remember
description: >-
  Captures fact snippets the user wants stored with the project when they say
  "remember this", "note this down", "save this", or similar and paste text.
  Use to store Slack excerpts, URLs, SQL snippets, team names and notes, etc.
---

# Remember / Note down

## When to use

- User says "remember this", "note this down", "save this", "capture this", "note that", or similar and provides or pastes text to store
- User wants to store a fact, snippet, URL, conversation excerpt, SQL, team contact, or other project-related note for later

## Instructions

1. **Capture the content** the user pasted or provided. If the user gave a short label or category (e.g. "Slack convo", "URL", "SQL", "team contact"), use it; otherwise infer a brief label from the content.
2. **Infer topics** from label, user hint, or content (e.g. `api`, `staging`, `db`, `team`). Use lowercase topic tokens.
3. **Route to the correct file** using `docs/facts/INDEX.md`:
   - If a topic matches an INDEX row → append to that file (e.g. `docs/facts/api.md`)
   - If the topic is new → create `docs/facts/<topic>.md` with a header and add a row to INDEX.md
   - If no topic matches → append to `docs/facts/captured.md`
4. **Append using this entry format** (consistent and searchable):

   ```markdown
   ---
   date: YYYY-MM-DD
   label: Short label
   topics: [api, staging]
   phase: implementation
   ---

   (Optional one-line context if helpful.)

   (Pasted/content here. Preserve formatting, code blocks, and links.)
   ```

   `phase` is optional (`spec`, `hld`, `implement`, `deploy`, etc.). Create `docs/facts/` and target files if they do not exist.
5. **Update INDEX.md** when you create a new topic file: add a table row with topic, file path, and keywords.
6. **Confirm briefly** to the user where the fact was saved (file path).
7. When the user or agent needs facts later: read `docs/facts/INDEX.md` first, then the listed file(s)—not only `captured.md`.
