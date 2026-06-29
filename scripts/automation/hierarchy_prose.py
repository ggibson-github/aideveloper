#!/usr/bin/env python3
"""Reader-facing prose normalization for hierarchy leaves and HTML publication."""

from __future__ import annotations

import html
import re
from dataclasses import dataclass, field
from pathlib import Path

from hierarchy_completeness import item_id_from_path, list_leaf_paths  # noqa: E402
from hierarchy_html_rules import META_STEP_PATTERNS  # noqa: E402
from hierarchy_vision_context import section_for_branch  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent.parent

# Cursor rules → capability spec (reader-facing, not repo paths)
RULE_TO_SPEC: dict[str, tuple[str, str]] = {
    "deterministic-first": ("B1.1", "Deterministic-first rule"),
    "evidence-required": ("G1.1", "Evidence-required rule"),
    "conductor": ("B2.1", "Conductor rule"),
    "genius-conductor": ("B3.1", "Genius conductor rule"),
}

EXTERNAL_DOC_TO_SPEC: dict[str, tuple[str, str]] = {
    "genius-conductor-tiered-routing.md": ("B3.1", "Genius conductor tiered routing"),
}

SKILL_TO_SPEC: dict[str, tuple[str, str]] = {
    "orchestrate-program": ("C4.2", "Orchestrate-program"),
    "hierarchy-expander": ("E1.3", "Catalog skills index"),
    "goal-keeper": ("A5.3", "Goal keeper"),
    "autopilot": ("A3.2", "Autopilot"),
}

BRANCH_FOR_SECTION: dict[str, str] = {
    "§3": "A",
    "§4": "B",
    "§5": "C",
    "§6": "D",
    "§7": "E",
    "§8": "F",
    "§9": "G",
    "§10": "H",
    "§11": "I",
    "§12": "J",
}


def github_anchor(title: str) -> str:
    s = title.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"\s+", "-", s)
    return s


def load_vision_sections(vision_path: Path | None = None) -> dict[str, dict[str, str]]:
    """Map §N → {title, anchor, branch_id}."""
    path = vision_path or ROOT / "documents/full-automation-vision-and-hierarchy.md"
    sections: dict[str, dict[str, str]] = {}
    if not path.is_file():
        return sections
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^##\s+(\d+)\.\s+(.+)$", line.strip())
        if not m:
            continue
        num, title = m.group(1), m.group(2).strip()
        key = f"§{num}"
        sections[key] = {
            "title": title,
            "anchor": github_anchor(f"{num} {title}"),
            "branch_id": BRANCH_FOR_SECTION.get(key, ""),
        }
    sections["§0"] = {"title": "Executive summary", "anchor": github_anchor("0 Executive summary"), "branch_id": ""}
    sections["§1"] = {"title": "North star definition", "anchor": github_anchor("1 North star definition"), "branch_id": ""}
    sections["§2"] = {"title": "Master hierarchy (top level)", "anchor": github_anchor("2 Master hierarchy top level"), "branch_id": ""}
    return sections


@dataclass
class ProseContext:
    slug_by_id: dict[str, str] = field(default_factory=dict)
    slug_by_file: dict[str, str] = field(default_factory=dict)
    vision_sections: dict[str, dict[str, str]] = field(default_factory=dict)
    vision_href_md: str = "../../full-automation-vision-and-hierarchy.md"
    plan_dir: Path | None = None

    def vision_md_link(self, section_key: str) -> str:
        info = self.vision_sections.get(section_key, {})
        title = info.get("title", section_key)
        anchor = info.get("anchor", "")
        href = self.vision_href_md
        if anchor:
            href += f"#{anchor}"
        return f"[Vision {section_key} — {title}]({href})"

    def vision_doc_href(self, depth: int) -> str:
        """Relative href from html-site page at *depth* to the vision markdown source."""
        return f"{'../' * (depth + 3)}full-automation-vision-and-hierarchy.md"

    def vision_html_link(self, section_key: str, depth: int) -> str:
        prefix = "../" * depth
        info = self.vision_sections.get(section_key, {})
        title = info.get("title", section_key)
        branch = info.get("branch_id", "")
        anchor = info.get("anchor", "")
        visible = f"Vision {section_key} — {title}" if title else f"Vision {section_key}"
        label = html.escape(visible, quote=True)
        if branch:
            href = f"{prefix}branches/{html.escape(branch, quote=True)}.html"
            return f'<a href="{href}" class="spec-link">{label}</a>'
        href = self.vision_doc_href(depth)
        if anchor:
            href += f"#{anchor}"
        return f'<a href="{html.escape(href, quote=True)}" class="spec-link">{label}</a>'

    def spec_md_link(self, item_id: str, label: str | None = None) -> str:
        slug = self.slug_by_id.get(item_id, "")
        if not slug:
            return label or item_id
        text = label or item_id
        return f"[{text}]({slug}.md)"

    def spec_html_link(self, item_id: str, label: str, depth: int) -> str:
        prefix = "../" * depth
        slug = self.slug_by_id.get(item_id, "")
        if not slug:
            return html.escape(label, quote=True)
        href = f"{prefix}capabilities/{html.escape(slug, quote=True)}.html"
        return f'<a href="{href}" class="spec-link">{html.escape(label, quote=True)}</a>'

    def resolve_md_href(self, href: str) -> str:
        href = href.strip()
        if href.startswith("http://") or href.startswith("https://"):
            return href
        name = Path(href).name
        if name in self.slug_by_file:
            return f"{self.slug_by_file[name]}.md"
        stem = Path(href).stem
        if f"{stem}.md" in self.slug_by_file:
            return f"{self.slug_by_file[f'{stem}.md']}.md"
        return href


def build_prose_context(out_dir: Path, vision_path: Path | None = None) -> ProseContext:
    slug_by_id: dict[str, str] = {}
    slug_by_file: dict[str, str] = {}
    for p in list_leaf_paths(out_dir):
        raw = p.read_text(encoding="utf-8")
        iid = item_id_from_path(p, raw)
        slug_by_id[iid] = p.stem
        slug_by_file[p.name] = p.stem
        slug_by_file[p.stem] = p.stem
    return ProseContext(
        slug_by_id=slug_by_id,
        slug_by_file=slug_by_file,
        vision_sections=load_vision_sections(vision_path),
        plan_dir=out_dir,
    )


def is_meta_step(step: str) -> bool:
    if re.match(r"^pass \d+:", step.strip(), re.I):
        return True
    return any(p.search(step) for p in META_STEP_PATTERNS)


def critique_prose(text: str) -> list[str]:
    """Return human-readable issues for critic pass."""
    issues: list[str] = []
    if "**" in text:
        issues.append("raw markdown bold (**)")
    if re.search(r"vision\s*§\d+(?![^\s]*\])", text, re.I):
        issues.append("bare vision § reference without link")
    if ".cursor/rules/" in text:
        issues.append("cursor rule path link")
    if re.search(r"(?<![A-Z0-9])s0(?![A-Z0-9])", text):
        issues.append("lowercase s0 without glossary link")
    if re.search(r"`[^`]+`", text) and "scripts/" in text:
        pass  # code paths ok
    return issues


def _replace_bare_vision_md(text: str, ctx: ProseContext) -> str:
    """Replace `vision §N` phrases with markdown links to the vision document."""

    def repl_phrase(m: re.Match[str]) -> str:
        key = f"§{m.group(1)}"
        if key not in ctx.vision_sections:
            return m.group(0)
        return ctx.vision_md_link(key)

    return re.sub(r"vision\s+§(\d+)", repl_phrase, text, flags=re.I)


def repair_corrupted_links(text: str, ctx: ProseContext) -> str:
    """Fix nested / duplicated vision markdown links from non-idempotent editor passes."""
    if "[[Vision" not in text and text.count("](..") < 2:
        return text

    def single_vision(m: re.Match[str]) -> str:
        sec = m.group(1)
        key = f"§{sec}"
        return ctx.vision_md_link(key) if key in ctx.vision_sections else m.group(0)

    text = re.sub(
        r"\[+Vision \[Vision §(\d+) — [^\]]+\]\([^)]+\)(?:[^\[]*\[[^\]]+\]\([^)]+\))+",
        single_vision,
        text,
    )
    text = re.sub(
        r"(\[Vision §(\d+) — [^\]]+\]\([^)]+\))(?: — [^\[]+\]\([^)]+\))+",
        r"\1",
        text,
    )
    text = re.sub(r"\[\[+", "[", text)
    text = re.sub(r"\]\(\.\./[^)]+\)\s*(\]\(\.\./[^)]+\))+", "", text)
    return text


def _replace_vision_refs_md(text: str, ctx: ProseContext) -> str:
    text = repair_corrupted_links(text, ctx)
    text = re.sub(
        r"\[full-automation-vision-and-hierarchy\.md\]\([^)]+\)\s*(\[Vision §[^\]]+\]\([^)]+\))",
        r"\1",
        text,
        flags=re.I,
    )
    if re.search(r"\[Vision §\d+ —", text):
        return _replace_bare_vision_md(text, ctx)
    text = _replace_bare_vision_md(text, ctx)
    if "Conflicts resolve in favor of" in text and "§" in text and "[Vision §" not in text:
        sec = re.search(r"§(\d+)", text)
        if sec:
            key = f"§{sec.group(1)}"
            text = re.sub(
                rf"§{sec.group(1)}\.?",
                ctx.vision_md_link(key),
                text,
                count=1,
            )
    return text


def _replace_rule_links_md(text: str, ctx: ProseContext) -> str:
    def repl(m: re.Match[str]) -> str:
        rule = Path(m.group(1)).stem
        if rule in RULE_TO_SPEC:
            item_id, label = RULE_TO_SPEC[rule]
            return f"({ctx.spec_md_link(item_id, label)})"
        return m.group(0)

    text = re.sub(
        r"\(\[[^\]]+\]\([^)]*\.cursor/rules/([^)]+)\)\)",
        repl,
        text,
        flags=re.I,
    )
    return text


def _replace_s0_md(text: str, ctx: ProseContext) -> str:
    if re.search(r"\[S0\]", text, re.I):
        return text
    link = ctx.spec_md_link("B1.1", "S0")
    return re.sub(r"\bS0\b", link, text)


def normalize_step_md(step: str, ctx: ProseContext, *, item_id: str = "", title: str = "") -> str:
    """Normalize one behavior step for markdown storage."""
    s = step.strip()
    if is_meta_step(s):
        return ""
    s = re.sub(r"\*\*([^*]+)\*\*", r"\1", s)
    s = _replace_rule_links_md(s, ctx)
    s = _replace_vision_refs_md(s, ctx)
    s = _replace_s0_md(s, ctx)
    s = re.sub(
        r"^Define and implement (.+?) per \[\[Vision[^\]]+\][^\n]+\]\([^)]+\)(?:[^\[]+\[[^\]]+\]\([^)]+\))*\.?$",
        lambda m: f"Define and implement {m.group(1).strip()} per {ctx.vision_md_link(section_for_branch(item_id) or '§3')}.",
        s,
        flags=re.I,
    )
    s = re.sub(
        r"^Implement (.+?) as specified in vision\s+(\[[^\]]+\]\([^)]+\))\.?$",
        lambda m: f"Define and implement {m.group(1).strip()} per {m.group(2)}.",
        s,
        flags=re.I,
    )
    s = re.sub(
        r"^Implement (.+?) as specified in vision\s*§\d+\.?$",
        lambda m: f"Define and implement {m.group(1).strip()} per {ctx.vision_md_link(section_for_branch(item_id) or '§3')}.",
        s,
        flags=re.I,
    )
    return s.strip()


def normalize_prose_md(text: str, ctx: ProseContext, *, item_id: str = "", title: str = "") -> str:
    text = _replace_rule_links_md(text, ctx)
    text = _replace_vision_refs_md(text, ctx)
    text = _replace_s0_md(text, ctx)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    return text


def fix_encoding(text: str) -> str:
    """Repair common UTF-8 mojibake from legacy markdown sources."""
    if not text:
        return text
    replacements = (
        ("\u00e2\u20ac\u201d", "\u2014"),
        ("\u00e2\u20ac\u201c", "\u2014"),
        ("\u00e2\u20ac\u2122", "\u2014"),
        ("\u00e2\u201a\u00ac", "\u20ac"),
        ("\u00e2\u2020\u2019", "\u2192"),
        ("\u00e2\u2020\u2018", "\u2192"),
        ("\u00c2\u00a7", "\u00a7"),
    )
    for old, new in replacements:
        text = text.replace(old, new)
    return text


def _chapter_href_from_index(stem: str, depth: int) -> str | None:
    """Map *-index stems to published chapter HTML paths."""
    if not stem.endswith("-index"):
        return None
    from hierarchy_book_structure import capability_group_id  # noqa: WPS433

    gid = stem[: -len("-index")]
    branch = gid[0] if gid and gid[0] in "ABCDEFGHIJ" else "meta"
    if branch in "ABCDEFGHIJ" and re.match(r"^[A-J]\d", gid):
        chapter_gid = capability_group_id(f"{gid}.1" if re.match(r"^[A-J]\d+\.\d+$", gid) else gid)
    else:
        chapter_gid = gid
    prefix = "../" * depth
    return f"{prefix}chapters/{branch}-{chapter_gid}.html"


def _lookup_slug(ctx: ProseContext, name: str) -> str | None:
    if name in ctx.slug_by_file:
        return ctx.slug_by_file[name]
    lower = name.lower()
    for key, slug in ctx.slug_by_file.items():
        if key.lower() == lower:
            return slug
    stem = Path(name).stem
    if stem in ctx.slug_by_file:
        return ctx.slug_by_file[stem]
    if f"{stem}.md" in ctx.slug_by_file:
        return ctx.slug_by_file[f"{stem}.md"]
    return None


def _resolve_spec_link_html(ctx: ProseContext, label: str, href_raw: str, depth: int) -> str:
    href_raw = href_raw.strip()
    if ".cursor/skills/" in href_raw.replace("\\", "/"):
        parts = Path(href_raw.replace("\\", "/")).parts
        skill = parts[-2] if parts and parts[-1].upper() == "SKILL.MD" else Path(href_raw).stem
        if skill in SKILL_TO_SPEC:
            item_id, default = SKILL_TO_SPEC[skill]
            return ctx.spec_html_link(item_id, label or default, depth)
        return html.escape(label, quote=True)

    name = Path(href_raw).name
    if name in EXTERNAL_DOC_TO_SPEC:
        item_id, default = EXTERNAL_DOC_TO_SPEC[name]
        return ctx.spec_html_link(item_id, label or default, depth)

    stem = Path(name).stem
    if stem.endswith("-index") or name.endswith("-index.md"):
        chap = _chapter_href_from_index(stem if stem.endswith("-index") else f"{stem}-index", depth)
        if chap:
            return (
                f'<a href="{html.escape(chap, quote=True)}" class="spec-link">'
                f"{html.escape(label, quote=True)}</a>"
            )
        return html.escape(label, quote=True)

    slug = _lookup_slug(ctx, name)
    if slug:
        prefix = "../" * depth
        return (
            f'<a href="{prefix}capabilities/{html.escape(slug, quote=True)}.html" class="spec-link">'
            f"{html.escape(label, quote=True)}</a>"
        )

    if href_raw.startswith("http://") or href_raw.startswith("https://"):
        return (
            f'<a href="{html.escape(href_raw, quote=True)}" class="spec-link">'
            f"{html.escape(label, quote=True)}</a>"
        )

    return html.escape(label, quote=True)


def _markdown_inline_to_html(text: str, ctx: ProseContext, depth: int) -> str:
    """Convert inline markdown links/bold/code to HTML (text segments escaped)."""
    out: list[str] = []
    i = 0
    n = len(text)
    prefix = "../" * depth
    while i < n:
        link = re.match(r"\[([^\]]+)\]\(([^)]+)\)", text[i:])
        if link:
            label = link.group(1)
            href_raw = link.group(2).strip()
            if ".cursor/rules/" in href_raw:
                rule = Path(href_raw).stem
                if rule in RULE_TO_SPEC:
                    item_id, default_label = RULE_TO_SPEC[rule]
                    out.append(ctx.spec_html_link(item_id, label or default_label, depth))
                else:
                    out.append(html.escape(label, quote=True))
            elif "vision-and-hierarchy" in href_raw.lower():
                sec = re.search(r"§(\d+)", label)
                if sec:
                    out.append(ctx.vision_html_link(f"§{sec.group(1)}", depth))
                else:
                    out.append(html.escape(label, quote=True))
            elif href_raw.endswith(".html") and "/branches/" in href_raw:
                out.append(
                    f'<a href="{html.escape(href_raw, quote=True)}" class="spec-link">'
                    f"{html.escape(label, quote=True)}</a>"
                )
            elif href_raw.endswith(".md") or ("/" in href_raw and not href_raw.startswith("http")):
                out.append(_resolve_spec_link_html(ctx, label, href_raw, depth))
            else:
                out.append(_resolve_spec_link_html(ctx, label, href_raw, depth))
            i += link.end()
            continue
        bold = re.match(r"\*\*([^*]+)\*\*", text[i:])
        if bold:
            out.append(f"<strong>{html.escape(bold.group(1), quote=True)}</strong>")
            i += bold.end()
            continue
        code = re.match(r"`([^`]+)`", text[i:])
        if code:
            out.append(f"<code>{html.escape(code.group(1), quote=True)}</code>")
            i += code.end()
            continue
        out.append(html.escape(text[i], quote=True))
        i += 1
    return "".join(out)


def glossary_link_html(fragment: str, depth: int, link_fn) -> str:
    """Apply glossary linking to plain-text segments outside HTML tags."""
    result: list[str] = []
    pos = 0
    skip = re.compile(r"(<a [^>]*>.*?</a>|<code>.*?</code>)", re.S)
    for m in skip.finditer(fragment):
        if m.start() > pos:
            result.append(link_fn(fragment[pos : m.start()], depth, already_html=True))
        result.append(m.group(0))
        pos = m.end()
    if pos < len(fragment):
        result.append(link_fn(fragment[pos:], depth, already_html=True))
    return "".join(result)


def render_prose_html(text: str, ctx: ProseContext, depth: int, link_fn) -> str:
    """Full reader prose → HTML with vision, spec, and glossary links."""
    if not text:
        return ""
    s = fix_encoding(text.strip())
    s = re.sub(r"\*\*([^*]+)\*\*", r"\1", s)
    if ".cursor/rules/" in s:
        s = _replace_rule_links_md(s, ctx)
    if "vision-and-hierarchy" not in s.lower() or not re.search(r"\[Vision §", s, re.I):
        s = _replace_bare_vision_md(s, ctx)
    s = re.sub(r"\[([^\]]+)\]\((\.\./branches/[A-J]\.html)\)", r"[\1](\2)", s)
    s = re.sub(r"\bs0\b", "S0", s, flags=re.I)
    html_body = _markdown_inline_to_html(s, ctx, depth)
    return glossary_link_html(html_body, depth, link_fn)


def compose_reader_narrative(
    reader_md: str,
    ctx: ProseContext,
    depth: int,
    link_fn,
) -> str:
    """Render ## Reader narrative markdown as HTML teaching prose (multi-paragraph)."""
    reader_md = re.sub(r"<!--.*?-->", "", reader_md, flags=re.DOTALL).strip()
    if not reader_md.strip():
        return ""
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", reader_md.strip()) if p.strip()]
    parts = [render_prose_html(p, ctx, depth, link_fn) for p in paragraphs]
    return "\n".join(f"<p>{html}</p>" for html in parts)
