#!/usr/bin/env python3
"""Glossary terms and auto-linking for hierarchy HTML publication (config-driven)."""

from __future__ import annotations

import html
import re

from hierarchy_html_config import load_glossary_config  # noqa: E402

GLOSSARY_ENTRIES: list[dict] = []
_LINK_PATTERNS: list[tuple[re.Pattern[str], str]] = []


def init_glossary(entries: list[dict] | None = None, *, topic: str = "full-automation", html_glossary: str | None = None) -> None:
    """Load glossary entries for a publish run (base JSON + topic overlay)."""
    global GLOSSARY_ENTRIES
    GLOSSARY_ENTRIES = entries if entries is not None else load_glossary_config(topic, html_glossary=html_glossary)
    _LINK_PATTERNS.clear()


def _build_patterns() -> None:
    if _LINK_PATTERNS:
        return
    seen: set[str] = set()
    ordered = sorted(
        ((t, e["id"]) for e in GLOSSARY_ENTRIES for t in e["terms"]),
        key=lambda x: -len(x[0]),
    )
    for term, entry_id in ordered:
        if term in seen:
            continue
        seen.add(term)
        if term.startswith("(") and term.endswith(")"):
            pat = re.compile(re.escape(term))
        elif " " in term or "–" in term or "-" in term or "/" in term:
            pat = re.compile(re.escape(term))
        elif re.match(r"^H[123]$", term):
            pat = re.compile(rf"(?<![.\w]){re.escape(term)}(?![.\w/–\-])")
        elif re.match(r"^S[0-4]$", term):
            pat = re.compile(rf"(?<![.\w]){re.escape(term)}(?![.\w/–\-])")
        else:
            pat = re.compile(rf"\b{re.escape(term)}\b")
        _LINK_PATTERNS.append((pat, entry_id))


def _entry_by_id(entry_id: str) -> dict:
    for e in GLOSSARY_ENTRIES:
        if e["id"] == entry_id:
            return e
    return {}


def link_glossary(text: str, depth: int = 0, *, already_html: bool = False) -> str:
    """Escape text and wrap known glossary terms with links to glossary.html#id."""
    if not text:
        return ""
    _build_patterns()
    prefix = "../" * depth
    s = text if already_html else html.escape(text, quote=True)

    def mk_link(label: str, entry_id: str) -> str:
        entry = _entry_by_id(entry_id)
        title = html.escape(entry.get("short", label), quote=True)
        href = f"{prefix}glossary.html#{entry_id}"
        return f'<a href="{href}" class="glossary-link" title="{title}">{html.escape(label, quote=True)}</a>'

    candidates: list[tuple[int, int, str, str]] = []
    for pat, entry_id in _LINK_PATTERNS:
        for m in pat.finditer(s):
            candidates.append((m.start(), m.end(), m.group(0), entry_id))
    candidates.sort(key=lambda x: (-(x[1] - x[0]), x[0]))

    chosen: list[tuple[int, int, str, str]] = []
    occupied: list[tuple[int, int]] = []
    for start, end, label, entry_id in candidates:
        if any(not (end <= a or start >= b) for a, b in occupied):
            continue
        chosen.append((start, end, label, entry_id))
        occupied.append((start, end))
    chosen.sort(key=lambda x: x[0])

    if not chosen:
        return s

    out: list[str] = []
    cursor = 0
    for start, end, label, entry_id in chosen:
        out.append(s[cursor:start])
        out.append(mk_link(label, entry_id))
        cursor = end
    out.append(s[cursor:])
    return "".join(out)


def build_glossary_page(*, shell_fn, depth: int = 0, intro: str = "") -> str:
    """Build glossary.html body using shell_fn(title, body, depth)."""
    prefix = "../" * depth
    categories: list[str] = []
    for e in GLOSSARY_ENTRIES:
        if e["category"] not in categories:
            categories.append(e["category"])

    toc = ""
    sections = ""
    for cat in categories:
        entries = [e for e in GLOSSARY_ENTRIES if e["category"] == cat]
        toc += f'<li class="glossary-cat">{html.escape(cat, quote=True)}<ul>'
        toc += "".join(
            f'<li><a href="#{html.escape(e["id"], quote=True)}">{html.escape(e["short"], quote=True)}</a></li>'
            for e in entries
        )
        toc += "</ul></li>"
        for entry in entries:
            spec_link = ""
            if entry.get("spec_slug"):
                spec_link = (
                    f'<p class="glossary-spec">'
                    f'<a href="{prefix}capabilities/{html.escape(entry["spec_slug"], quote=True)}.html">'
                    f"Full specification →</a></p>"
                )
            sections += f"""
<section class="glossary-entry" id="{html.escape(entry['id'], quote=True)}">
  <p class="glossary-cat-label">{html.escape(cat, quote=True)}</p>
  <h2>{html.escape(entry['short'], quote=True)}</h2>
  <p>{html.escape(entry['definition'], quote=True)}</p>
  {spec_link}
</section>"""

    body = f"""
<main class="glossary-page">
  <h1 class="page-title">Glossary</h1>
  <p class="section-sub">{html.escape(intro or "Definitions for specialized terms, acronyms, and metrics.", quote=True)}</p>
  <div class="glossary-toc card">
    <h3>Quick navigation</h3>
    <ul class="glossary-toc-list glossary-toc-grouped">{toc}</ul>
  </div>
  {sections}
</main>"""
    return shell_fn(title="Glossary", body=body, depth=depth)
