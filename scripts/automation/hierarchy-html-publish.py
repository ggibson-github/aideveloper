#!/usr/bin/env python3
"""
Publish hierarchy plan documents as a static corporate HTML site.

Generic rules: scripts/automation/hierarchy_html_rules.py
Human docs: docs/automation/templates/hierarchy-html/publication-rules.md

Usage:
  python scripts/automation/hierarchy-html-publish.py --topic <TOPIC>
  python scripts/automation/hierarchy-expander-run.py --topic <TOPIC> publish
"""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import sys
from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from hierarchy_html_config import (  # noqa: E402
    derive_branch_meta,
    load_glossary_config,
    load_site_config,
    ordered_branches,
    resolve_index_stats,
)
from hierarchy_html_glossary import build_glossary_page, init_glossary, link_glossary  # noqa: E402
from hierarchy_html_parse import ParsedNode, load_all_nodes  # noqa: E402
from hierarchy_html_rules import (  # noqa: E402
    PublishRuleViolation,
    enforce_publish_rules,
    is_conceptual_capability,
    public_behavior_steps,
    sanitize_export_record,
    validate_pages,
    validate_site_config,
)
from hierarchy_reader_narrative import (  # noqa: E402
    build_branch_story_md,
    build_chapter_story_md,
    build_group_story_md,
    build_reader_story_md,
    display_title,
    humanize_timeline_step,
)
from hierarchy_book_structure import (  # noqa: E402
    META_CHAPTER_GROUPS,
    META_READING_HINTS,
    capability_group_id,
    group_nodes,
    group_title,
    is_sequential_group,
    ordered_group_ids,
)
from hierarchy_prose import ProseContext, build_prose_context, compose_reader_narrative, fix_encoding, render_prose_html  # noqa: E402
from hierarchy_topic_config import resolve_topic  # noqa: E402

TEMPLATE_DIR = ROOT / "docs/automation/templates/hierarchy-html"
# html-site/chapters/*.html lives one level below site root (same as branches/, capabilities/).
CHAPTER_DEPTH = 1


@dataclass
class PublishContext:
    topic_title: str
    site: dict[str, Any]
    branch_meta: dict[str, dict[str, str]]
    prose: ProseContext


def esc(s: str) -> str:
    return html.escape(fix_encoding(s), quote=True)


def rel_href(from_dir_depth: int, target: str) -> str:
    return ("../" * from_dir_depth if from_dir_depth else "") + target


def shell(ctx: PublishContext, *, title: str, body: str, depth: int = 0, nav_extra: str = "") -> str:
    css = rel_href(depth, "assets/css/site.css")
    js = rel_href(depth, "assets/js/site.js")
    home = rel_href(depth, "index.html")
    branches = rel_href(depth, "branches/index.html")
    glossary = rel_href(depth, "glossary.html")
    data = rel_href(depth, "data/manifest.json")
    brand = esc(ctx.site.get("brand_title", "Architecture Blueprint"))
    subtitle = esc(ctx.site.get("brand_subtitle", ""))
    footer = esc(ctx.site.get("footer_label", "Architecture blueprint"))
    branch_nav = esc(ctx.site.get("branch_group_label_plural", "Branches"))
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>{esc(title)}</title>
  <link rel="stylesheet" href="{css}"/>
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js" defer></script>
  <script src="https://cdn.jsdelivr.net/npm/mermaid@10.9.0/dist/mermaid.min.js" defer></script>
  <script src="{js}" defer></script>
</head>
<body data-base="">
  <header class="site-header">
    <div class="header-inner">
      <a class="brand" href="{home}">{brand}<span>{subtitle}</span></a>
      <nav class="nav">
        <a href="{home}">Overview</a>
        <a href="{branches}">{branch_nav}</a>
        <a href="{glossary}">Glossary</a>
        {nav_extra}
        <a href="{data}">Data</a>
      </nav>
    </div>
  </header>
  {body}
  <footer class="site-footer">
    <div class="footer-inner">
      <span>{footer} · {date.today().isoformat()}</span>
    </div>
  </footer>
</body>
</html>"""


def overview_mermaid(ctx: PublishContext, branch_ids: list[str]) -> str:
    center = ctx.site.get("overview_mermaid_center", "Core loop")
    lines = ["flowchart TB"]
    for bid in branch_ids:
        if bid == "meta":
            continue
        meta = ctx.branch_meta.get(bid, {})
        title = meta.get("title", bid).replace('"', "'")
        lines.append(f'  {bid}["{bid}: {title}"]')
    if branch_ids:
        first = next((b for b in branch_ids if b != "meta"), branch_ids[0])
        lines.append(f'  center(({center})) --> {first}')
        for bid in branch_ids:
            if bid != "meta" and bid != first:
                lines.append(f"  {first} --> {bid}")
    return "\n".join(lines)


def branch_mermaid(ctx: PublishContext, branch_id: str, nodes: list[ParsedNode]) -> str:
    meta = ctx.branch_meta.get(branch_id, {})
    title = meta.get("title", branch_id)
    label = ctx.site.get("branch_group_label", "Branch")
    lines = ["flowchart LR", f'  subgraph grp ["{label} {branch_id} — {title}"]']
    for n in nodes[:12]:
        nid = re.sub(r"[^a-zA-Z0-9]", "_", n.id)
        lines.append(f'    {nid}["{n.id.replace(chr(34), chr(39))}"]')
    if len(nodes) > 12:
        lines.append(f'    more["+ {len(nodes) - 12} more"]')
    lines.append("  end")
    return "\n".join(lines)


def chart_config(chart_type: str, labels: list, datasets: list, options: dict | None = None) -> str:
    return json.dumps({"type": chart_type, "data": {"labels": labels, "datasets": datasets}, "options": options or {}})


def hitl_callout(ctx: PublishContext, depth: int) -> str:
    p = "../" * depth
    return f"""
<div class="hitl-callout">
  <h2>Human touchpoints explained</h2>
  <dl>
    <dt><a href="{p}glossary.html#h1" class="glossary-link">H1 — Initial planning gate</a></dt>
    <dd>Approve the plan before autonomous pursuit begins.</dd>
    <dt><a href="{p}glossary.html#h2" class="glossary-link">H2 — Blocker assistance</a></dt>
    <dd>Provide help when automation is stuck.</dd>
    <dt><a href="{p}glossary.html#h3" class="glossary-link">H3 — Final sign-off</a></dt>
    <dd>Accept or reject verified outcomes.</dd>
  </dl>
</div>"""


def build_index_page(ctx: PublishContext, nodes: list[ParsedNode]) -> str:
    by_branch: dict[str, list[ParsedNode]] = defaultdict(list)
    for n in nodes:
        by_branch[n.branch].append(n)

    branch_order = ordered_branches(by_branch)
    branch_labels = [
        f"{b} — {ctx.branch_meta.get(b, {}).get('title', b)}" for b in branch_order
    ]
    branch_counts = [len(by_branch[b]) for b in branch_order]
    branch_colors = [ctx.branch_meta.get(b, {}).get("color", "#0d9488") for b in branch_order]

    stat_cards = ""
    for value, label in resolve_index_stats(
        ctx.site, node_count=len(nodes), branch_count=len(branch_order),
    ):
        stat_cards += f"""
      <div class="stat-card"><div class="value">{esc(value)}</div><div class="label">{link_glossary(label, 0)}</div></div>"""

    branch_cards = ""
    blabel = ctx.site.get("branch_group_label", "Branch")
    for bid in branch_order:
        meta = ctx.branch_meta.get(bid, {"title": bid, "story": "", "color": "#0d9488"})
        branch_cards += f"""
<article class="branch-card" style="--branch-color: {meta.get('color', '#0d9488')}">
  <div class="branch-id">{esc(blabel)} {esc(bid)}</div>
  <h3><a href="branches/{esc(bid)}.html">{esc(meta.get('title', bid))}</a></h3>
  <p>{link_glossary(meta.get('story', ''), 0)}</p>
  <div class="meta">{len(by_branch[bid])} {esc(ctx.site.get('capability_label', 'capabilities'))}</div>
</article>"""

    charts_cfg = ctx.site.get("charts", [])
    chart_panels = ""
    if len(charts_cfg) >= 1:
        c0 = charts_cfg[0]
        bar = chart_config(
            c0.get("type", "bar"),
            branch_labels,
            [{"label": "Capabilities", "data": branch_counts, "backgroundColor": branch_colors, "borderRadius": 6}],
            {"indexAxis": "y", "plugins": {"legend": {"display": False}}},
        )
        chart_panels += f"""
    <div class="chart-panel">
      <h3>{link_glossary(c0.get('title', 'Capability density by branch'), 0)}</h3>
      <p class="chart-caption">{link_glossary(c0.get('caption', ''), 0)}</p>
      <div class="chart-wrap"><canvas data-chart='{esc(bar)}'></canvas></div>
    </div>"""
    if len(charts_cfg) >= 2:
        c1 = charts_cfg[1]
        doughnut = chart_config(
            c1.get("type", "doughnut"),
            [b for b in branch_order],
            [{"label": "Capabilities", "data": branch_counts, "backgroundColor": branch_colors, "borderWidth": 0}],
            {"plugins": {"legend": {"position": "right", "labels": {"boxWidth": 12, "font": {"size": 11}}}}},
        )
        chart_panels += f"""
    <div class="chart-panel">
      <h3>{link_glossary(c1.get('title', 'Architectural scope by branch'), 0)}</h3>
      <p class="chart-caption">{link_glossary(c1.get('caption', ''), 0)}</p>
      <div class="chart-wrap"><canvas data-chart='{esc(doughnut)}'></canvas></div>
    </div>"""

    body = f"""
<section class="hero">
  <div class="hero-inner">
    <p class="hero-eyebrow">{esc(ctx.site.get('hero_eyebrow', 'Architecture portfolio'))}</p>
    <h1>{esc(ctx.topic_title)}</h1>
    <p class="hero-lead">{link_glossary(ctx.site.get('hero_lead', ''), 0)}</p>
    <div class="hero-stats">{stat_cards}
    </div>
  </div>
</section>
<main>
  <h2 class="section-title">The story at a glance</h2>
  <p class="section-sub">{link_glossary(ctx.site.get('story_sub', ''), 0)}</p>
  <p class="story-block">{link_glossary(ctx.site.get('story_at_a_glance', ''), 0)}</p>

  <div class="diagram-panel">
    <pre class="mermaid">{esc(overview_mermaid(ctx, branch_order))}</pre>
  </div>

  <div class="grid-2">{chart_panels}
  </div>

  <h2 class="section-title" style="margin-top: 2.5rem">{link_glossary(ctx.site.get('explore_branches_heading', 'Explore the branches'), 0)}</h2>
  <p class="section-sub">{link_glossary(ctx.site.get('explore_branches_sub', ''), 0)}</p>
  <div class="branch-grid">{branch_cards}</div>
</main>"""
    return shell(ctx, title=f"{ctx.topic_title} — Overview", body=body, depth=0)


def build_branches_index(ctx: PublishContext, nodes: list[ParsedNode]) -> str:
    by_branch: dict[str, list[ParsedNode]] = defaultdict(list)
    for n in nodes:
        by_branch[n.branch].append(n)

    blabel = ctx.site.get("branch_group_label", "Branch")
    cards = ""
    for bid in ordered_branches(by_branch):
        meta = ctx.branch_meta.get(bid, {})
        cards += f"""
<article class="branch-card" style="--branch-color: {meta.get('color', '#0d9488')}">
  <div class="branch-id">{esc(blabel)} {esc(bid)}</div>
  <h3><a href="{esc(bid)}.html">{esc(meta.get('title', bid))}</a></h3>
  <p>{link_glossary(meta.get('subtitle', meta.get('title', '')), 1)}</p>
  <div class="meta">{len(by_branch[bid])} {esc(ctx.site.get('capability_label', 'capabilities'))}</div>
</article>"""

    body = f"""
<main>
  <h1 class="page-title">{link_glossary(ctx.site.get('branch_group_label_plural', 'Branches'), 1)}</h1>
  <p class="section-sub">{link_glossary(ctx.site.get('explore_branches_sub', ''), 1)}</p>
  <div class="branch-grid">{cards}</div>
</main>"""
    return shell(ctx, title=ctx.site.get("branch_group_label_plural", "Branches"), body=body, depth=1)


def group_flow_mermaid(group_id: str, nodes: list[ParsedNode]) -> str:
    """Sequential flow within a group (e.g. A2 pursuit loop)."""
    if not is_sequential_group(group_id) or len(nodes) < 2:
        return ""
    lines = ["flowchart LR"]
    ids: list[str] = []
    for n in nodes[:12]:
        nid = re.sub(r"[^a-zA-Z0-9]", "_", n.id)
        ids.append(nid)
        label = display_title(n)[:40].replace('"', "'")
        lines.append(f'  {nid}["{n.id}<br/>{label}"]')
    for i in range(len(ids) - 1):
        lines.append(f"  {ids[i]} --> {ids[i + 1]}")
    return "\n".join(lines)


def _cell_html(c: str) -> str:
    c = fix_encoding(c.strip())
    if len(c) >= 2 and c.startswith("`") and c.endswith("`"):
        return f"<code>{html.escape(c[1:-1], quote=True)}</code>"
    return html.escape(c, quote=True)


def _html_table(headers: list[str], rows: list[list[str]]) -> str:
    if not rows:
        return ""
    th = "".join(f"<th>{esc(h)}</th>" for h in headers)
    body = ""
    for row in rows:
        body += "<tr>" + "".join(f"<td>{_cell_html(c)}</td>" for c in row) + "</tr>"
    return f'<table class="data-table"><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table>'


def _verification_table(node: ParsedNode) -> str:
    if not node.verification:
        return ""
    headers = list(node.verification[0].keys())
    rows: list[list[str]] = []
    for row in node.verification[:8]:
        cells = [fix_encoding(str(row.get(h, ""))) for h in headers]
        if any(c in ("Link", "Why", "------") for c in cells):
            break
        if cells and cells[0].startswith("[") and "vision-and-hierarchy" in " ".join(cells):
            continue
        rows.append(cells)
    if not rows:
        return ""
    return f"""
<h2 class="section-title">Verification</h2>
<div class="card table-wrap">{_html_table(headers, rows)}</div>"""


def _bullet_section(title: str, items: list[str], limit: int = 8) -> str:
    if not items:
        return ""
    clean: list[str] = []
    skip_re = re.compile(
        r"^\[ \]|^\*\*|## |implement##|Cross-links|Adversarial review|"
        r"Silent stop:|False complete:|Scope bleed:|Concrete implementation",
        re.I,
    )
    for x in items:
        x = fix_encoding(x.strip())
        if re.match(r"^pass \d+:", x, re.I):
            continue
        if "cross-link related nodes" in x.lower():
            continue
        if skip_re.search(x):
            continue
        if x.startswith("|") or x in ("------", "Link", "Why"):
            continue
        clean.append(re.sub(r"`([^`]+)`", r"\1", x))
    if not clean:
        return ""
    lis = "".join(f"<li>{esc(x)}</li>" for x in clean[:limit])
    return f"""
<h2 class="section-title">{esc(title)}</h2>
<div class="card"><ul class="prose-list">{lis}</ul></div>"""


def build_group_chapter_page(
    ctx: PublishContext,
    group_id: str,
    nodes: list[ParsedNode],
    branch_id: str,
) -> str:
    meta = ctx.branch_meta.get(branch_id, {})
    blabel = ctx.site.get("branch_group_label", "Branch")
    branch_title = meta.get("title", branch_id)
    story = compose_reader_narrative(
        build_chapter_story_md(group_id, nodes, branch_title, branch_id=branch_id),
        ctx.prose,
        CHAPTER_DEPTH,
        link_glossary,
    )
    flow = group_flow_mermaid(group_id, nodes)
    flow_block = ""
    if flow:
        flow_block = f"""
<div class="diagram-panel">
  <pre class="mermaid">{esc(flow)}</pre>
</div>"""
    cap_items = ""
    for n in nodes:
        cap_items += f"""
<li>
  <span class="cap-id"><a href="{rel_href(CHAPTER_DEPTH, 'capabilities/' + n.slug + '.html')}">{esc(n.id)}</a></span>
  <span class="cap-title">{esc(display_title(n))}</span>
</li>"""
    body = f"""
<main>
  <nav class="breadcrumb">
    <a href="{rel_href(CHAPTER_DEPTH, 'index.html')}">Overview</a> ·
    <a href="{rel_href(CHAPTER_DEPTH, 'branches/' + branch_id + '.html')}">{esc(blabel)} {esc(branch_id)}</a> ·
    {esc(group_id)}
  </nav>
  <p class="page-id">{esc(group_id)} · {esc(branch_title)}</p>
  <h1 class="page-title">{esc(group_title(group_id))}</h1>
  <div class="story-block">{story}</div>
  {flow_block}
  <h2 class="section-title">Capabilities in this chapter</h2>
  <div class="card"><ul class="cap-list">{cap_items}</ul></div>
</main>"""
    return shell(ctx, title=f"{group_id} — {group_title(group_id)}", body=body, depth=CHAPTER_DEPTH)


def build_reading_order_html(
    ctx: PublishContext,
    branch_id: str,
    group_ids: list[str],
    depth: int,
) -> str:
    """Clickable numbered chapter list (meta front matter and similar)."""
    items = ""
    for i, gid in enumerate(group_ids, 1):
        title = group_title(gid)
        hint = META_READING_HINTS.get(gid, "")
        href = rel_href(depth, f"chapters/{branch_id}-{gid}.html")
        hint_html = f'<span class="reading-hint">{esc(hint)}</span>' if hint else ""
        items += f"""
<li class="reading-order-item">
  <a href="{href}">
    <span class="reading-num">{i}.</span>
    <strong>{esc(gid)}</strong> — {esc(title)}
  </a>
  {hint_html}
</li>"""
    return f"""
<h2 class="section-title">Read in this order</h2>
<nav class="reading-order" aria-label="Reading order">
  <ol class="reading-order-list">{items}</ol>
</nav>"""


def build_branch_page(ctx: PublishContext, branch_id: str, nodes: list[ParsedNode]) -> str:
    meta = ctx.branch_meta.get(branch_id, {"title": branch_id, "story": "", "color": "#0d9488"})
    blabel = ctx.site.get("branch_group_label", "Branch")
    nodes = sorted(nodes, key=lambda n: n.id)
    grouped = group_nodes(nodes)
    group_ids = ordered_group_ids(branch_id, list(grouped.keys()))

    branch_story = compose_reader_narrative(
        build_branch_story_md(branch_id, meta.get("title", branch_id), group_ids),
        ctx.prose,
        1,
        link_glossary,
    )

    reading_order = ""
    if branch_id == "meta":
        reading_order = build_reading_order_html(ctx, branch_id, group_ids, 1)

    sections = ""
    for gid in group_ids:
        gnodes = grouped[gid]
        flow = group_flow_mermaid(gid, gnodes)
        flow_html = ""
        if flow:
            flow_html = f'<div class="diagram-panel"><pre class="mermaid">{esc(flow)}</pre></div>'
        cap_items = ""
        for n in gnodes:
            cap_items += f"""
<li>
  <span class="cap-id"><a href="../capabilities/{esc(n.slug)}.html">{esc(n.id)}</a></span>
  <span class="cap-title">{esc(display_title(n))}</span>
</li>"""
        sections += f"""
<section class="cap-group">
  <h2 class="section-title"><a href="../chapters/{esc(branch_id)}-{esc(gid)}.html">{esc(gid)}: {esc(group_title(gid))}</a></h2>
  {flow_html}
  <div class="card"><ul class="cap-list">{cap_items}</ul></div>
</section>"""

    body = f"""
<main>
  <nav class="breadcrumb"><a href="../index.html">Overview</a> · <a href="index.html">{esc(ctx.site.get('branch_group_label_plural', 'Branches'))}</a> · {esc(blabel)} {esc(branch_id)}</nav>
  <p class="page-id">{esc(blabel)} {esc(branch_id)}</p>
  <h1 class="page-title">{esc(meta.get('title', branch_id))}</h1>
  <div class="story-block">{branch_story}</div>
  {reading_order}
  <p><span class="badge">{len(nodes)} {link_glossary(ctx.site.get('capability_label', 'capabilities'), 1)}</span></p>
  {sections}
</main>"""
    return shell(ctx, title=f"{branch_id} — {meta.get('title', branch_id)}", body=body, depth=1)


def build_capability_page(ctx: PublishContext, node: ParsedNode) -> str:
    meta = ctx.branch_meta.get(node.branch, {})
    blabel = ctx.site.get("branch_group_label", "Branch")
    steps = public_behavior_steps(node.behavior_steps, item_id=node.id, branch=node.branch)
    timeline_section = (
        "What this defines"
        if is_conceptual_capability(node.id, node.branch)
        else "How it works"
    )
    branch_title = meta.get("title", node.branch)

    reader_md = node.reader_narrative.strip()
    if not reader_md:
        reader_md = build_reader_story_md(node, ctx.prose, branch_title)
    narrative_html = compose_reader_narrative(reader_md, ctx.prose, 1, link_glossary)

    timeline = "".join(
        f'<li><span class="step-num">Step {i}</span><span class="step-text">'
        f'{render_prose_html(humanize_timeline_step(step, node), ctx.prose, 1, link_glossary)}</span></li>'
        for i, step in enumerate(steps[:8], 1)
    )

    mermaid_block = ""
    if node.mermaid:
        mermaid_block = f"""
<div class="diagram-panel">
  <pre class="mermaid">{esc(node.mermaid)}</pre>
</div>"""

    json_summary = esc(ctx.site.get("json_details_summary", "Implementation contract"))
    book_mode = ctx.site.get("book_mode", True)
    json_block = ""
    if node.json_example:
        if book_mode:
            json_block = f"""
<h2 class="section-title">{json_summary}</h2>
<div class="card"><pre class="code-block">{esc(node.json_example)}</pre></div>"""
        else:
            json_block = f"""
<details class="details-block">
  <summary>{json_summary}</summary>
  <div class="details-body">
    <pre>{esc(node.json_example)}</pre>
  </div>
</details>"""

    release_note = ""
    if node.release:
        release_note = f'<p class="release-note">Target release: {esc(node.release)}</p>'

    callout_ids = set(ctx.site.get("hitl_callout_node_ids") or [])
    callout = hitl_callout(ctx, 1) if node.id in callout_ids else ""

    gid = capability_group_id(node.id)
    chapter_link = ""
    if re.match(r"^[A-J]\d", gid):
        chapter_link = f' · <a href="../chapters/{esc(node.branch)}-{esc(gid)}.html">{esc(gid)}</a>'

    body = f"""
<main>
  <nav class="breadcrumb">
    <a href="../index.html">Overview</a> ·
    <a href="../branches/{esc(node.branch)}.html">{esc(blabel)} {esc(node.branch)}</a>{chapter_link} ·
    {esc(node.id)}
  </nav>
  <p class="page-id">{esc(node.id)} · {esc(meta.get('title', node.branch))}</p>
  <h1 class="page-title">{esc(display_title(node))}</h1>
  <p class="page-subtitle">{esc(node.title)}</p>
  {callout}
  <div class="story-block">{narrative_html}</div>
  {mermaid_block}
  <h2 class="section-title">{timeline_section}</h2>
  <ol class="timeline">{timeline or '<li><span class="step-text">See diagram above.</span></li>'}</ol>
  {_verification_table(node)}
  {_bullet_section("Edge cases", node.edge_cases)}
  {_bullet_section("Acceptance criteria", node.acceptance)}
  {json_block}
  {release_note}
</main>"""
    return shell(ctx, title=f"{node.id} — {display_title(node)}", body=body, depth=1)


def publish(
    *,
    topic: str,
    output_dir: Path,
    html_dir: Path,
    topic_title: str,
    html_site_config: str | None = None,
    html_glossary: str | None = None,
    vision_source: Path | None = None,
) -> dict:
    site = load_site_config(topic, html_site_config=html_site_config)
    glossary_entries = load_glossary_config(topic, html_glossary=html_glossary)
    init_glossary(entries=glossary_entries)

    enforce_publish_rules(validate_site_config(site, glossary_entries))

    # HTML publish is read-only for markdown leaves. Prose normalization (including reader
    # narratives) runs in run-hierarchy-full-pipeline.py — not here — to avoid clobbering
    # author/agent prose when regenerating HTML.
    nodes = load_all_nodes(output_dir, None)
    branch_meta = derive_branch_meta(output_dir, nodes)
    prose = build_prose_context(output_dir)
    ctx = PublishContext(topic_title=topic_title, site=site, branch_meta=branch_meta, prose=prose)

    by_branch: dict[str, list[ParsedNode]] = defaultdict(list)
    for n in nodes:
        by_branch[n.branch].append(n)

    pages: dict[str, str] = {}
    pages[str(html_dir / "index.html")] = build_index_page(ctx, nodes)
    pages[str(html_dir / "glossary.html")] = build_glossary_page(
        shell_fn=lambda **kw: shell(ctx, **kw),
        depth=0,
        intro=site.get("glossary_intro", ""),
    )
    pages[str(html_dir / "branches" / "index.html")] = build_branches_index(ctx, nodes)
    for bid, branch_nodes in by_branch.items():
        pages[str(html_dir / "branches" / f"{bid}.html")] = build_branch_page(ctx, bid, branch_nodes)
        if bid in "ABCDEFGHIJ":
            for gid, gnodes in group_nodes(branch_nodes).items():
                if re.match(r"^[A-J]\d", gid):
                    pages[str(html_dir / "chapters" / f"{bid}-{gid}.html")] = build_group_chapter_page(
                        ctx, gid, gnodes, bid,
                    )
        elif bid == "meta":
            for gid, gnodes in group_nodes(branch_nodes).items():
                if gid in META_CHAPTER_GROUPS:
                    pages[str(html_dir / "chapters" / f"{bid}-{gid}.html")] = build_group_chapter_page(
                        ctx, gid, gnodes, bid,
                    )
    for n in nodes:
        pages[str(html_dir / "capabilities" / f"{n.slug}.html")] = build_capability_page(ctx, n)

    enforce_publish_rules(validate_pages(pages))

    html_dir.mkdir(parents=True, exist_ok=True)
    assets_css = html_dir / "assets/css/site.css"
    assets_js = html_dir / "assets/js/site.js"
    assets_css.parent.mkdir(parents=True, exist_ok=True)
    assets_js.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(TEMPLATE_DIR / "site.css", assets_css)
    shutil.copy2(TEMPLATE_DIR / "site.js", assets_js)

    data_dir = html_dir / "data"
    nodes_data_dir = data_dir / "nodes"
    nodes_data_dir.mkdir(parents=True, exist_ok=True)

    manifest = {
        "generated_at": date.today().isoformat(),
        "topic_title": topic_title,
        "node_count": len(nodes),
        "branches": {},
        "nodes": [],
    }
    for n in nodes:
        dest = nodes_data_dir / f"{n.slug}.json"
        dest.write_text(json.dumps(sanitize_export_record(n.to_dict()), indent=2) + "\n", encoding="utf-8")
        manifest["nodes"].append({"id": n.id, "title": n.title, "branch": n.branch, "html": f"capabilities/{n.slug}.html"})
        manifest["branches"].setdefault(n.branch, []).append(n.id)

    (data_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    for rel_path, html in pages.items():
        out = Path(rel_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html, encoding="utf-8")

    page_count = len(pages)
    return {
        "html_dir": str(html_dir.relative_to(ROOT)).replace("\\", "/"),
        "pages": page_count,
        "nodes": len(nodes),
        "rules": "docs/automation/templates/hierarchy-html/publication-rules.md",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Publish hierarchy as static HTML site")
    parser.add_argument("--topic", default="full-automation")
    parser.add_argument("--output-dir", help="Markdown plan directory")
    parser.add_argument("--html-dir", help="HTML output directory (default: <output-dir>/html-site)")
    parser.add_argument("--html-site-config", help="Override site config JSON")
    parser.add_argument("--html-glossary", help="Override glossary overlay JSON")
    args = parser.parse_args()

    cfg = resolve_topic(args.topic, output_dir=args.output_dir)
    out_dir = cfg.output_dir
    html_dir = Path(args.html_dir) if args.html_dir else out_dir / "html-site"
    if not out_dir.is_dir():
        print(f"ERROR: output dir missing: {out_dir}", file=sys.stderr)
        return 1

    html_site_config = args.html_site_config or getattr(cfg, "html_site_config", None)
    html_glossary = args.html_glossary or getattr(cfg, "html_glossary", None)

    try:
        result = publish(
            topic=args.topic,
            output_dir=out_dir,
            html_dir=html_dir if html_dir.is_absolute() else ROOT / html_dir,
            topic_title=cfg.title,
            html_site_config=html_site_config,
            html_glossary=html_glossary,
            vision_source=cfg.source,
        )
    except PublishRuleViolation as exc:
        for loc, msg in exc.violations:
            print(f"ERROR publication rule [{loc}]: {msg}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    print(f"\nOpen: {(ROOT / result['html_dir'] / 'index.html').as_uri()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
