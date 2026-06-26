#!/usr/bin/env python3
"""Cursor hook dispatcher v2: context injection, read guards, subagent contracts, compaction."""

from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path

_HOOK_DIR = Path(__file__).resolve().parent
if str(_HOOK_DIR) not in sys.path:
    sys.path.insert(0, str(_HOOK_DIR))

from context_builder import (
    build_context,
    build_subagent_context,
    check_read_permission,
    resolve_workspace_root,
)

CONTINUE_PATTERN = re.compile(
    r"\b(continue|start|resume|/continue|/status|/gate|/task|/verify|/research)\b",
    re.IGNORECASE,
)
JOURNAL_PATH_FRAGMENTS = ("journal/progress.md", "journal/state.json")


def read_input() -> dict:
    raw = sys.stdin.read()
    if not raw.strip():
        return {}
    return json.loads(raw)


def workspace_from_input(data: dict) -> Path:
    roots = data.get("workspace_roots")
    if isinstance(roots, list) and roots:
        return resolve_workspace_root(roots)
    return resolve_workspace_root(None)


def extract_prompt(data: dict) -> str:
    for key in ("prompt", "user_prompt", "message", "text", "content"):
        value = data.get(key)
        if isinstance(value, str):
            return value
    for container in ("input", "payload", "data"):
        nested = data.get(container)
        if isinstance(nested, dict):
            for key in ("prompt", "user_prompt", "message", "text", "content"):
                value = nested.get(key)
                if isinstance(value, str):
                    return value
    return ""


def extract_read_path(data: dict) -> str:
    for key in ("path", "file_path", "filePath", "target"):
        value = data.get(key)
        if isinstance(value, str):
            return value
    for container in ("tool_input", "input", "arguments", "payload"):
        nested = data.get(container)
        if isinstance(nested, dict):
            for key in ("path", "file_path", "filePath", "target"):
                value = nested.get(key)
                if isinstance(value, str):
                    return value
    return ""


def should_inject_context(event: str, data: dict) -> bool:
    if event in ("sessionStart", "subagentStart"):
        return True
    if event == "beforeSubmitPrompt":
        prompt = extract_prompt(data)
        return bool(prompt and CONTINUE_PATTERN.search(prompt))
    if event == "postToolUse":
        path = extract_read_path(data).replace("\\", "/")
        return any(fragment in path for fragment in JOURNAL_PATH_FRAGMENTS)
    return False


def write_compaction_snapshot(root: Path) -> None:
    journal = root / "journal" / "progress.md"
    status = root / "STATUS.md"
    snap_dir = root / "journal"
    snap = snap_dir / f"snapshot-{date.today().isoformat()}.md"
    parts = [f"# Journal snapshot {date.today().isoformat()}", ""]
    if journal.is_file():
        parts.append(journal.read_text(encoding="utf-8"))
    if status.is_file():
        parts.append("")
        parts.append("## STATUS")
        parts.append(status.read_text(encoding="utf-8"))
    snap.write_text("\n".join(parts), encoding="utf-8")


def main() -> None:
    try:
        data = read_input()
        event = str(data.get("hook_event_name", ""))
        root = workspace_from_input(data)

        if event == "preCompact":
            write_compaction_snapshot(root)
            print("{}")
            return

        if event == "preToolUse":
            tool = str(data.get("tool_name", data.get("tool", "")))
            if "Read" in tool:
                path = extract_read_path(data)
                if path and "docs/design" in path.replace("\\", "/"):
                    result = check_read_permission(root, path)
                    if result:
                        print(json.dumps(result))
                        return
            print('{"permission": "allow"}')
            return

        if event == "subagentStart":
            ctx = build_subagent_context(root)
            print(json.dumps({"user_message": ctx, "permission": "allow"}))
            return

        if should_inject_context(event, data):
            context = build_context(root)
            if context:
                print(json.dumps({"additional_context": context}))
            else:
                print("{}")
            return

        print("{}")
    except Exception:
        print("{}")
        sys.exit(0)


if __name__ == "__main__":
    main()
