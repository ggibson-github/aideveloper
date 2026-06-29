# Hierarchy → HTML publication rules (generic)

These rules apply to **every topic** when running:

```bash
python scripts/automation/hierarchy-expander-run.py --topic <TOPIC> publish
```

Implementation: `scripts/automation/hierarchy_html_rules.py`  
Config overlay: `default-site-config.json` + optional `<topic>-site-config.json`  
Glossary: `glossary-base.json` + optional `<topic>-glossary.json`

Publish **fails** (exit 1) if any rule violation is detected in site config, glossary definitions, or generated HTML.

---

## 1. Subject-only content

**The HTML site describes the subject of the hierarchy** (the system, product, or domain being specified) — **never** how plan markdown was produced, certified, or expanded.

| Do | Don't |
|----|-------|
| Pursuit loops, evidence, planes, capabilities | "Machine-certified before publication" |
| H1/H2/H3 as system touchpoints | Doc quality scores, iteration passes |
| Verification and release criteria | "Reading time" or hierarchy-expander process |

**Enforced by:**

- `validate_subject_only()` / `RULE_SUBJECT_ONLY`
- No quality-report data in `html-site/data/`
- `sanitize_export_record()` strips `quality`, `source_path`
- `public_behavior_steps()` removes expansion-process steps

---

## 2. No publication-format commentary

**The reader must never see commentary about the HTML site itself** — how pages are organized, where JSON files live, how to open the site, or navigation instructions framed as publication meta.

| Do | Don't |
|----|-------|
| Plane/branch purpose and behavior | "Diagrams and narratives lead; structured specifications live in linked data pages" |
| Glossary definitions of domain terms | "Open locally", "no server required", "static site" |
| Implementation contracts in collapsible blocks | "Technical appendix", footnotes pointing at `data/manifest.json` |
| Subject-oriented section subtitles | "Each branch is a chapter of the design. Select one to continue." |

**Enforced by:**

- `validate_no_publication_meta()` / `RULE_NO_PUBLICATION_META`
- `validate_site_config()` — checks all copy keys in site config and glossary JSON **before** pages are built
- `validate_pages()` — checks **every** generated HTML page before write
- `enforce_publish_rules()` — aborts publish on any violation
- Publisher never emits data-path footnotes or HTML-delivery footer copy

**Site config copy keys validated:** `hero_lead`, `story_at_a_glance`, `story_sub`, `explore_branches_sub`, chart titles/captions, stat labels, `glossary_intro`, etc. (see `SITE_CONFIG_COPY_KEYS` in rules module).

---

## 3. Glossary — every special term is clickable

First-time readers must never guess acronyms or chart labels.

**All** of these surfaces go through `link_glossary()`:

- Hero and story paragraphs
- Section and chart headings
- Chart captions (required under every chart)
- Stat card labels
- Branch stories and capability narratives
- Timeline steps

**Glossary page** (`glossary.html`):

- Grouped categories (Human touchpoints, Architecture, Charts & metrics, …)
- Plain-language definition per term (definitions also pass Rule 1 + Rule 2 validation)
- Optional "Full specification →" link to a capability page

**Extend per topic:** add `<topic>-glossary.json` with more terms; merged with base.

---

## 4. Story-first, corporate presentation

- Narrative lead, then Mermaid diagrams, then charts
- No markdown `#` headings or pipe tables in body HTML
- JSON specs in collapsible `<details>` with subject label (default: "Implementation contract"), not data-path commentary
- Static CSS/JS under `assets/`
- Brand, hero copy, and stat labels from site config (not hardcoded per topic in Python)

---

## 5. Site structure (every topic)

```
html-site/
  index.html
  glossary.html
  branches/index.html + {branchId}.html
  capabilities/{slug}.html
  data/manifest.json + nodes/{slug}.json
  assets/css/site.css + js/site.js
```

Branch metadata is **derived from leaf docs** (MASTER-* or index nodes), not hardcoded in Python.

The `data/` tree exists for integrators (nav **Data** link). Rule 2 forbids **prose** that tells readers about it.

---

## 6. Charts

Every chart panel must have:

1. **Title** — glossary-linked phrase describing what is measured
2. **Caption** — one sentence explaining how to read the chart (subject-only)
3. **Data** — counts from actual nodes (never doc-quality metrics)

Default charts: capability density by branch, architectural scope share.

---

## 7. Topic configuration

In `hierarchy-topics.json`:

```json
"html_site_dir": "documents/plans/my-topic/html-site/",
"html_site_config": "docs/automation/templates/hierarchy-html/my-topic-site-config.json",
"html_glossary": "docs/automation/templates/hierarchy-html/my-topic-glossary.json"
```

Omit optional paths to use defaults only.

---

## 9. Reader prose (writer / critic pass)

Every pipeline pass ends with a **prose editor** on all leaves (`hierarchy_prose_editor.py`):

| Fix | Example |
|-----|---------|
| Vision §N → linked reference | `vision §3` → `[Vision §3 — Branch A…](vision.md#…)` / HTML → `branches/A.html` for plane sections; §0–§2 → vision source `.md` with anchor |
| S0–S4, H1–H3 → spec or glossary links | bare `S0` → `[S0](B1.1-s0-….md)` |
| Cursor rules → capability specs | `.cursor/rules/deterministic-first.mdc` → `B1.1` spec link |
| Strip raw `**bold**` and Pass N meta steps from Behavior | expansion-process steps removed from reader timelines |

HTML publish runs the editor again, then `render_prose_html()` for capability pages.

**Timeline steps (agent-authored):** After reader narratives exist, choose one path:

| Path | When | Command |
|------|------|---------|
| **S0 (default)** | Batch regen from reader narrative; no API | `python scripts/automation/hierarchy_agent_timeline.py apply-all --force` |
| **Cursor CLI** | Per-leaf LLM when narrative→step extraction is weak | `python scripts/automation/hierarchy-expander-run.py --topic full-automation timeline-agent run-cli --group A1 --limit 5` |
| **cursor-sdk** | Same as CLI but via Python SDK | `… timeline-agent run-sdk --group INTRO` |

Requires `CURSOR_API_KEY` for CLI/SDK. Install CLI: [Headless CLI](https://cursor.com/docs/cli/headless) (`agent -p --trust`). Queue JSON: `timeline-agent queue`.

Then publish and audit:

```bash
python scripts/automation/hierarchy-expander-run.py --topic full-automation publish
python scripts/automation/audit-timeline-steps.py
```

Timeline steps describe expert-system behavior (not generic “Define and implement…” boilerplate). Front-matter pages use **What this defines** instead of **How it works**.

Tests: `tests/unit/test_hierarchy_prose.py`

---

## 10. When to run

After `certify` exit 0. Publishing does **not** require or display certification metadata.

Tests: `tests/unit/test_hierarchy_html_rules.py`
