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

1. **Capture the content** the user pasted or provided. If the user gave a short label or category (e.g. "Slack convo", "URL", "SQL", "team contact"), use it; otherwise infer a brief label from the content (e.g. "URL", "SQL snippet", "Slack excerpt", "Team/contact") so the entry is easy to find later.
2. **Append to `docs/facts/captured.md`** using this format so entries are consistent and searchable:

   ```markdown
   ---
   ## YYYY-MM-DD [Label]
   (Optional one-line context if helpful.)

   (Pasted/content here. Preserve formatting, code blocks, and links.)
   ---
   ```

   Create `docs/facts/` and `docs/facts/captured.md` if they do not exist. If the file already has a header (e.g. "# Captured facts and snippets"), append new entries after it and any existing entries.
3. **Confirm briefly** to the user that the fact was saved and where (e.g. "Saved to docs/facts/captured.md. You can search that file later.")
4. When the user or the agent needs to find something later, search or read `docs/facts/captured.md` (and any other files in `docs/facts/`) for relevant snippets.
