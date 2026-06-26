"""Build additional_context for Cursor hooks from state.json, journal, STATUS, and facts."""

from __future__ import annotations

import re
from pathlib import Path

from state_io import load_state, path_allowed, state_summary_markdown

MAX_FACT_BYTES = 4096
JOURNAL_REL = Path("journal/progress.md")
STATUS_REL = Path("STATUS.md")
INDEX_REL = Path("docs/facts/INDEX.md")
FACTS_DIR_REL = Path("docs/facts")


def resolve_workspace_root(workspace_roots: list[str] | None) -> Path:
    if workspace_roots:
        return Path(workspace_roots[0])
    return Path.cwd()


def read_text(path: Path) -> str | None:
    if not path.is_file():
        return None
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return None


def parse_index_rows(index_text: str) -> list[tuple[str, list[str]]]:
    rows: list[tuple[str, list[str]]] = []
    for line in index_text.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.split("|")]
        if len(cells) < 5:
            continue
        file_cell = cells[2]
        keywords_cell = cells[4]
        if file_cell.lower() in ("file", "") or "---" in file_cell:
            continue
        file_match = re.search(r"([\w.-]+\.md)", file_cell)
        if not file_match:
            continue
        rel = f"docs/facts/{file_match.group(1)}"
        keywords = [k.strip().lower() for k in keywords_cell.split(",") if k.strip()]
        rows.append((rel, keywords))
    return rows


def match_index_files(
    index_rows: list[tuple[str, list[str]]],
    search_text: str,
) -> list[str]:
    search_lower = search_text.lower()
    matched: list[str] = []
    for rel_path, keywords in index_rows:
        for kw in keywords:
            if kw and kw in search_lower:
                if rel_path not in matched:
                    matched.append(rel_path)
                break
    return matched


def excerpt_file(path: Path, remaining_bytes: int) -> str | None:
    if remaining_bytes <= 0 or not path.is_file():
        return None
    try:
        content = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if len(content.encode("utf-8")) <= remaining_bytes:
        return content
    truncated = content[:remaining_bytes]
    return truncated + "\n\n...(truncated)..."


def collect_fact_paths(workspace_root: Path, state: dict) -> list[str]:
    fact_paths: list[str] = []
    for p in state.get("context_files") or []:
        if p not in fact_paths and "docs/facts" in p.replace("\\", "/"):
            fact_paths.append(p)
    for p in state.get("allowed_reads") or []:
        if "docs/facts" in str(p).replace("\\", "/") and p not in fact_paths:
            fact_paths.append(p)
    search_blob = " ".join(
        str(state.get(k, "")) for k in ("next_action", "phase", "feature_id", "blockers")
    )
    index_text = read_text(workspace_root / INDEX_REL)
    if index_text:
        for rel in match_index_files(parse_index_rows(index_text), search_blob):
            if rel not in fact_paths:
                fact_paths.append(rel)
    return fact_paths


def build_context(workspace_root: Path) -> str | None:
    state = load_state(workspace_root)
    journal_text = read_text(workspace_root / JOURNAL_REL)
    if not journal_text and not state.get("next_action"):
        return None

    parts: list[str] = ["## Injected pipeline context (hook v2)", ""]
    parts.append(state_summary_markdown(state))

    status_text = read_text(workspace_root / STATUS_REL)
    if status_text and status_text.strip():
        parts.append("")
        parts.append("### STATUS.md")
        parts.append(status_text.strip()[:1500])

    fact_paths = collect_fact_paths(workspace_root, state)
    if fact_paths:
        parts.append("")
        parts.append("### Related facts")
        remaining = MAX_FACT_BYTES
        for rel in fact_paths:
            fact_path = workspace_root / rel
            if not fact_path.is_file():
                fact_path = workspace_root / FACTS_DIR_REL / Path(rel).name
            excerpt = excerpt_file(fact_path, remaining)
            if excerpt:
                parts.append(f"#### {rel}")
                parts.append(excerpt)
                remaining -= len(excerpt.encode("utf-8"))
                if remaining <= 0:
                    break

    parts.append("")
    parts.append(
        "Read `journal/state.json` and paths in **allowed_reads** only. "
        "Do not read design docs outside allowed_reads."
    )
    return "\n".join(parts)


def build_subagent_context(workspace_root: Path) -> str:
    state = load_state(workspace_root)
    parts = [
        "## Subagent contract (v2)",
        "",
        "You are a worker subagent. **Do not** write `journal/progress.md` or `journal/state.json`.",
        "Return a structured summary to the parent conductor.",
        "",
        state_summary_markdown(state),
    ]
    return "\n".join(parts)


def check_read_permission(workspace_root: Path, read_path: str) -> dict | None:
    state = load_state(workspace_root)
    if path_allowed(read_path, state):
        return None
    return {
        "permission": "ask",
        "user_message": (
            f"Read of `{read_path}` is outside allowed_reads for the current pipeline step. "
            "Approve if intentional, or run the Librarian subagent to update allowed_reads."
        ),
        "agent_message": (
            f"Read blocked (ask): `{read_path}` not in allowed_reads. "
            f"Allowed: {state.get('allowed_reads')}"
        ),
    }
