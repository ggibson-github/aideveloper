# HTML publication

Static, corporate-style HTML site from certified hierarchy markdown.

## Command

```bash
python scripts/automation/hierarchy-expander-run.py --topic <TOPIC> publish
```

Run **after** `certify` exit 0.

## Generic rules (all topics)

Publication behavior is **not** hardcoded per topic. Rules live in:

| Artifact | Purpose |
|----------|---------|
| `scripts/automation/hierarchy_html_rules.py` | Subject-only, **no publication meta** (Rule 2), forbidden fields, meta-step filters |
| `docs/automation/templates/hierarchy-html/publication-rules.md` | Human-readable rule reference |
| `docs/automation/templates/hierarchy-html/default-site-config.json` | Default brand, hero, charts, stats |
| `docs/automation/templates/hierarchy-html/glossary-base.json` | Shared glossary terms (branch, capability, chart labels) |

Per-topic overlays (optional, auto-discovered by slug if omitted from registry):

- `<topic>-site-config.json` — brand copy, branch labels, HITL callout node IDs, index stats
- `<topic>-glossary.json` — domain terms (H1–H3, S0–S4, etc.)

Register optional paths in `docs/automation/hierarchy-topics.json`:

```json
"html_site_config": "docs/automation/templates/hierarchy-html/my-topic-site-config.json",
"html_glossary": "docs/automation/templates/hierarchy-html/my-topic-glossary.json"
```

Publish **fails** (exit 1) if site config, glossary definitions, or any generated page violates the rules.

## Output layout

```
<output-dir>/html-site/
  index.html              Executive overview + charts + branch map
  glossary.html           Clickable term definitions (linked from all prose)
  branches/
    index.html            Branch picker
    <branch>.html         Branch narrative + capability index
  capabilities/
    <slug>.html           One page per leaf
  data/
    manifest.json         Machine index (no quality/cert metadata)
    nodes/<slug>.json     Sanitized node records (subject-only fields)
  assets/css/site.css
  assets/js/site.js
```

**Not emitted:** quality reports, certification banners, iteration-pass metadata, reading-time stats.

## Design intent (enforced by rules module)

- **Subject only** — content describes the system under design, never hierarchy expansion or doc certification
- **Glossary links** — terms in hero, stories, chart titles/captions, stat labels, and timelines auto-link to `glossary.html`
- **Story first** — hero narrative, branch chapters, capability summaries before raw data
- **Diagrams primary** — Mermaid flowcharts from each spec; overview graph on index
- **Charts** — capability density + scope charts (Chart.js) with captions from site config
- **No publication meta** — never describe how the HTML site is laid out, where JSON files live, or how to open the site locally

## Viewing

Open `html-site/index.html` in any browser. No web server required.

Mermaid and Chart.js load from jsDelivr CDN (internet on first view). CSS/JS assets are local.

## Scripts

| Script | Role |
|--------|------|
| `scripts/automation/hierarchy-html-publish.py` | Main publisher (also `--output-dir`, `--html-dir`, config overrides) |
| `scripts/automation/hierarchy_html_rules.py` | Generic publication rules |
| `scripts/automation/hierarchy_html_config.py` | Site config + branch meta derivation |
| `scripts/automation/hierarchy_html_glossary.py` | Glossary loading + auto-linking |
