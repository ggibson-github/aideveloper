#!/usr/bin/env python3
"""
Publication rules for hierarchy → HTML (generic, all topics).

Every rule here applies to every topic unless explicitly overridden in site config.
See docs/automation/templates/hierarchy-html/publication-rules.md
"""

from __future__ import annotations

import re
from typing import Any

# —— Rule 1: subject-only (no hierarchy-production meta) ——
RULE_SUBJECT_ONLY = {
    "id": "subject-only",
    "summary": "Describe the subject system — never how plan markdown was produced or certified.",
}

FORBIDDEN_THEMES = (
    "hierarchy expansion process",
    "document certification scores",
    "iteration passes on plan markdown",
    "machine-certified before publication",
    "reading time before human review",
    "quality report aggregate",
)

DOC_PRODUCTION_PHRASES = (
    ("certified for review", "doc certification banner"),
    ("machine quality gate", "doc quality gate"),
    ("iteration pass", "expansion iteration"),
    ("reading time", "human reading time meta"),
    ("hierarchy you are reading", "self-referential hierarchy meta"),
    ("quality score / 100", "doc quality score"),
)

# Strip from exported JSON:
FORBIDDEN_EXPORT_FIELDS = frozenset({"quality", "source_path", "quality_summary"})

# Do not write these data files into html-site/:
FORBIDDEN_DATA_ARTIFACTS = frozenset({"quality-summary.json", "hierarchy-quality-report.json"})

# —— Rule 2: no publication-format commentary (reader never sees HTML meta) ——
RULE_NO_PUBLICATION_META = {
    "id": "no-publication-meta",
    "summary": (
        "Reader-facing copy must never describe the HTML site itself — "
        "layout, data file locations, how to open the site, or navigation instructions."
    ),
}

PUBLICATION_META_PHRASES = (
    ("diagrams and narratives lead", "html layout commentary"),
    ("diagrams and narratives explain", "html layout commentary"),
    ("structured specifications live", "html data-path commentary"),
    ("linked data pages", "html data-path commentary"),
    ("live in linked data", "html data-path commentary"),
    ("throughout the site link", "html self-reference"),
    ("highlighted phrases throughout", "html self-reference"),
    ("used in this portfolio", "publication self-reference"),
    ("this portfolio", "publication self-reference"),
    ("open locally", "html delivery commentary"),
    ("no server required", "html delivery commentary"),
    ("static site", "html delivery commentary"),
    ("technical appendix", "html appendix commentary"),
    ("structured specifications:", "html data-path commentary"),
    ("structured specification:", "html data-path commentary"),
    ("full record:", "html data-path commentary"),
    ("select one to continue", "navigation instruction"),
    ("chapter of the system design", "html chapter metaphor"),
    ("chapter of the design", "html chapter metaphor"),
)

# HTML fragments the publisher must never emit in reader body content:
FORBIDDEN_BODY_HTML_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r'<div class="footnotes">\s*<p>\s*structured specifications', re.I | re.S),
    re.compile(r'<div class="footnotes">\s*<p><strong>\s*technical appendix', re.I | re.S),
    re.compile(r"static site — open locally", re.I),
)

# Site-config and glossary string keys checked before publish:
SITE_CONFIG_COPY_KEYS = (
    "brand_title",
    "brand_subtitle",
    "footer_label",
    "hero_eyebrow",
    "hero_lead",
    "story_at_a_glance",
    "story_sub",
    "explore_branches_heading",
    "explore_branches_sub",
    "glossary_intro",
    "json_details_summary",
)

# —— Rule 3: filter expansion-process steps from subject timelines ——
META_STEP_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"^pass \d+:", re.I),
    re.compile(r"cross-check parent index", re.I),
    re.compile(r"audit-hierarchy-depth", re.I),
    re.compile(r"hierarchy-expander", re.I),
    re.compile(r"check-hierarchy-queue", re.I),
    re.compile(r"sec-15 release row for implement", re.I),
    re.compile(r"document .+ in parent index with verify", re.I),
    re.compile(r"add checklist row in sec-15", re.I),
    re.compile(r"vision-expansion-prompt", re.I),
)


class PublishRuleViolation(Exception):
    """Raised when generated HTML or config violates publication rules."""

    def __init__(self, violations: list[tuple[str, str]]) -> None:
        self.violations = violations
        super().__init__(f"{len(violations)} publication rule violation(s)")


def is_conceptual_capability(item_id: str, branch: str) -> bool:
    """Front-matter and roadmap nodes define architecture; they are not runtime harness features."""
    if branch == "meta":
        return True
    return item_id.startswith(("INTRO", "MASTER", "APP-")) or item_id.startswith("SEC-")


def public_behavior_steps(steps: list[str], *, item_id: str = "", branch: str = "") -> list[str]:
    """Return behavior steps suitable for HTML (subject-only)."""
    out: list[str] = []
    for step in steps:
        if any(p.search(step) for p in META_STEP_PATTERNS):
            continue
        if is_conceptual_capability(item_id, branch):
            low = step.lower()
            if re.search(r"map `.+` to v2\.|sec-15-index|sec-15 release row", low):
                continue
            if "create or extend s0 script if behavior is file-derived" in low:
                continue
            if re.search(r"validate `.+` against sec-15 release checklist", low):
                continue
            if low.startswith("define and implement"):
                continue
            if "add unit test under tests/unit/" in low and "when script exists" in low:
                continue
        out.append(step)
    return out


def sanitize_export_record(data: dict[str, Any]) -> dict[str, Any]:
    """Remove fields that describe document production, not the subject."""
    clean = {k: v for k, v in data.items() if k not in FORBIDDEN_EXPORT_FIELDS}
    if "behavior_steps" in clean:
        clean["behavior_steps"] = public_behavior_steps(
            clean.get("behavior_steps") or [],
            item_id=str(clean.get("id", "")),
            branch=str(clean.get("branch", "")),
        )
    return clean


def _phrase_violations(text: str, phrases: tuple[tuple[str, str], ...]) -> list[str]:
    lower = text.lower()
    return [f"{reason}: contains '{phrase}'" for phrase, reason in phrases if phrase in lower]


def validate_no_publication_meta(text: str) -> list[str]:
    """Rule 2: no HTML/publication self-commentary in reader-visible copy."""
    warnings = _phrase_violations(text, PUBLICATION_META_PHRASES)
    for pat in FORBIDDEN_BODY_HTML_PATTERNS:
        if pat.search(text):
            warnings.append(f"forbidden body HTML: matches {pat.pattern[:48]}…")
    return warnings


def validate_subject_only(text: str) -> list[str]:
    """Rule 1: no doc-production or certification meta in reader-visible copy."""
    return _phrase_violations(text, DOC_PRODUCTION_PHRASES)


def validate_visible_copy(text: str) -> list[str]:
    """Return warnings if visible copy violates any publication rule."""
    return validate_subject_only(text) + validate_no_publication_meta(text) + validate_no_reference_blob(text)


def _story_block_inner(html: str) -> str:
    m = re.search(r'class="story-block"[^>]*>(.*?)</div>', html, re.S)
    return m.group(1) if m else ""


def validate_no_reference_blob(html: str) -> list[str]:
    """Rule 6: no comma-separated reference inventories — use clickable lists."""
    warnings: list[str] = []
    story = _story_block_inner(html)
    if not story.strip():
        return warnings
    plain_parts = [
        re.sub(r"<[^>]+>", " ", p)
        for p in re.findall(r"<p[^>]*>(.*?)</p>", story, re.S)
    ]
    for plain in plain_parts:
        p = re.sub(r"\s+", " ", plain).strip()
        if not p:
            continue
        if re.search(r"read in this order:", p, re.I):
            warnings.append("reference blob: 'Read in this order' must be a reading-order list, not prose")
        if re.search(r"capabilities:\s*.+,", p, re.I):
            warnings.append("reference blob: inline capability enumeration (use list below)")
        if len(re.findall(r"\(§\d+\)", p)) >= 3:
            warnings.append("reference blob: comma-separated section inventory in prose (use list)")
        if re.search(r"topic groups:", p, re.I) and p.count(",") >= 3:
            warnings.append("reference blob: inline topic-group inventory (use cap-group sections)")
        if re.search(r"organized into \d+ topic groups:", p, re.I) and p.count(",") >= 3:
            warnings.append("reference blob: inline group enumeration (use list below)")
    if re.search(r"read in this order:", story, re.I) and "reading-order-list" not in html:
        warnings.append("reference blob: missing reading-order-list for reading-order section")
    return warnings


def _site_config_strings(site: dict[str, Any]) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    for key in SITE_CONFIG_COPY_KEYS:
        val = site.get(key)
        if isinstance(val, str) and val.strip():
            out.append((f"site-config:{key}", val))
    for i, chart in enumerate(site.get("charts") or []):
        if isinstance(chart, dict):
            for sub in ("title", "caption"):
                val = chart.get(sub)
                if isinstance(val, str) and val.strip():
                    out.append((f"site-config:charts[{i}].{sub}", val))
    for i, stat in enumerate(site.get("index_stats") or []):
        if isinstance(stat, dict):
            val = stat.get("label")
            if isinstance(val, str) and val.strip():
                out.append((f"site-config:index_stats[{i}].label", val))
    return out


def validate_site_config(site: dict[str, Any], glossary_entries: list[dict] | None = None) -> list[tuple[str, str]]:
    """Validate topic site config and glossary definitions before building pages."""
    violations: list[tuple[str, str]] = []
    for loc, text in _site_config_strings(site):
        for msg in validate_visible_copy(text):
            violations.append((loc, msg))
    for entry in glossary_entries or []:
        eid = entry.get("id", "?")
        for field in ("short", "definition"):
            text = entry.get(field)
            if isinstance(text, str) and text.strip():
                for msg in validate_visible_copy(text):
                    violations.append((f"glossary:{eid}.{field}", msg))
    return violations


def validate_pages(pages: dict[str, str]) -> list[tuple[str, str]]:
    """Validate all generated HTML pages (Rule 1 + Rule 2)."""
    violations: list[tuple[str, str]] = []
    for path, html in pages.items():
        for msg in validate_visible_copy(html):
            violations.append((path, msg))
    return violations


def enforce_publish_rules(violations: list[tuple[str, str]]) -> None:
    """Fail publish if any rule violation exists."""
    if violations:
        raise PublishRuleViolation(violations)


# —— Rule 4: glossary ——
GLOSSARY_REQUIRED_SURFACES = (
    "hero_lead",
    "story_at_a_glance",
    "section_subtitles",
    "chart_titles",
    "chart_captions",
    "stat_labels",
    "branch_stories",
    "capability_narratives",
    "capability_timelines",
    "index_section_headings",
)

# —— Rule 5: presentation ——
PRESENTATION_RULES = {
    "story_before_data": True,
    "diagrams_primary": True,
    "charts_require_caption": True,
    "json_in_collapsible": True,
    "no_markdown_pipe_tables_in_body": True,
    "corporate_static_css": True,
    "glossary_in_nav": True,
    "no_publication_meta_in_body": True,
    "no_data_path_footnotes": True,
    "no_html_delivery_commentary": True,
}

BRANCH_COLOR_PALETTE = (
    "#1e40af", "#4338ca", "#7c3aed", "#0d9488", "#0891b2",
    "#ca8a04", "#dc2626", "#475569", "#0369a1", "#64748b", "#334155",
)

PUBLICATION_RULES = (RULE_SUBJECT_ONLY, RULE_NO_PUBLICATION_META)
