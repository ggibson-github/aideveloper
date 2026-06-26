"""Read and write journal/state.json (v2 machine router)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

STATE_REL = Path("journal/state.json")
JOURNAL_REL = Path("journal/progress.md")

DEFAULT_STATE: dict[str, Any] = {
    "version": 2,
    "spec_file": "spec.md",
    "spec_version": None,
    "mode": "greenfield",
    "phase": "not_started",
    "feature_id": None,
    "repo_url": None,
    "current_branch": "main",
    "last_completed": None,
    "next_action": "run spec-parser",
    "context_files": [],
    "allowed_reads": [
        "journal/progress.md",
        "journal/state.json",
        "spec.md",
        "docs/facts/INDEX.md",
    ],
    "forbidden_reads": [
        "docs/design/hld.md",
        "docs/design/dd.md",
        "docs/design/dd/",
    ],
    "gates_pending": [],
    "blocking_questions": [],
    "deferred_questions": [],
    "resolved_qa_archive": "docs/decisions/archive.md",
    "blockers": None,
    "pause_reason": None,
    "last_failure": None,
    "completion_status": "not_started",
    "evidence_required": False,
    "evidence_files": [],
    "last_verify": None,
    "last_session_summary": None,
}


def load_state(workspace_root: Path) -> dict[str, Any]:
    path = workspace_root / STATE_REL
    if not path.is_file():
        return dict(DEFAULT_STATE)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            merged = dict(DEFAULT_STATE)
            merged.update(data)
            return merged
    except (OSError, json.JSONDecodeError):
        pass
    return dict(DEFAULT_STATE)


def save_state(workspace_root: Path, state: dict[str, Any]) -> None:
    path = workspace_root / STATE_REL
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")


def path_allowed(path: str, state: dict[str, Any]) -> bool:
    normalized = path.replace("\\", "/").lower()
    allowed = state.get("allowed_reads") or []
    context = state.get("context_files") or []
    always = [
        "journal/progress.md",
        "journal/state.json",
        "status.md",
        "docs/facts/index.md",
    ]
    check_list = list(allowed) + list(context) + always
    for entry in check_list:
        entry_n = str(entry).replace("\\", "/").lower()
        if not entry_n:
            continue
        if normalized == entry_n or normalized.endswith("/" + entry_n):
            return True
        if entry_n.endswith("/") and normalized.startswith(entry_n):
            return True
        if normalized.startswith(entry_n):
            return True
    forbidden = state.get("forbidden_reads") or []
    for entry in forbidden:
        entry_n = str(entry).replace("\\", "/").lower()
        if entry_n and (normalized == entry_n or entry_n in normalized):
            return False
    if "docs/design/" in normalized and normalized.endswith((".md", ".mmd")):
        if "requirements-summary" in normalized:
            return True
        return False
    return True


def state_summary_markdown(state: dict[str, Any]) -> str:
    lines = ["### State (journal/state.json)", ""]
    for key in (
        "next_action",
        "phase",
        "mode",
        "feature_id",
        "context_files",
        "allowed_reads",
        "gates_pending",
        "blocking_questions",
        "blockers",
        "evidence_required",
        "evidence_files",
        "last_verify",
        "completion_status",
    ):
        val = state.get(key)
        if val is not None and val != [] and val != "":
            lines.append(f"- **{key}:** {val}")
    return "\n".join(lines)
