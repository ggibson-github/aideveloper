#!/usr/bin/env python3
"""Run timeline CLI batch in parallel shards; merge progress when all exit."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
PY = sys.executable
QUEUE = ROOT / "docs/automation/hierarchy-timeline-agent-queue.json"
PROGRESS_MAIN = ROOT / "docs/automation/hierarchy-timeline-cli-progress.json"
SHARD_DIR = ROOT / "docs/automation/timeline-cli-shards"


def merge_progress(shard_paths: list[Path]) -> dict:
    merged: dict = {"done": {}, "failed": {}}
    if PROGRESS_MAIN.is_file():
        base = json.loads(PROGRESS_MAIN.read_text(encoding="utf-8"))
        merged["done"].update(base.get("done", {}))
        merged["failed"].update(base.get("failed", {}))
    for p in shard_paths:
        if not p.is_file():
            continue
        data = json.loads(p.read_text(encoding="utf-8"))
        merged["done"].update(data.get("done", {}))
        merged["failed"].update(data.get("failed", {}))
    PROGRESS_MAIN.write_text(json.dumps(merged, indent=2) + "\n", encoding="utf-8")
    return merged


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--shards", type=int, default=6)
    parser.add_argument("--model", default="composer-2.5")
    parser.add_argument("--merge-only", action="store_true")
    args = parser.parse_args()

    SHARD_DIR.mkdir(parents=True, exist_ok=True)
    shard_progress = sorted(SHARD_DIR.glob("progress-*.json"))

    if args.merge_only:
        m = merge_progress(shard_progress)
        print(f"Merged: {len(m['done'])} done, {len(m['failed'])} failed")
        return 0

    q = json.loads(QUEUE.read_text(encoding="utf-8"))
    done: set[str] = set()
    if PROGRESS_MAIN.is_file():
        done.update(json.loads(PROGRESS_MAIN.read_text(encoding="utf-8")).get("done", {}))

    items = [it for it in q["items"] if it["item_id"] not in done]
    if not items:
        print("All items already done")
        return 0

    n = min(args.shards, len(items))
    chunks: list[list] = [[] for _ in range(n)]
    for i, it in enumerate(items):
        chunks[i % n].append(it)

    procs: list[subprocess.Popen] = []
    for idx, chunk in enumerate(chunks):
        if not chunk:
            continue
        shard_q = SHARD_DIR / f"queue-{idx}.json"
        prog = SHARD_DIR / f"progress-{idx}.json"
        shard_q.write_text(
            json.dumps({"generated": q.get("generated"), "items": chunk}, indent=2) + "\n",
            encoding="utf-8",
        )
        cmd = [
            PY,
            "scripts/automation/hierarchy_agent_timeline.py",
            "run-cli",
            "--queue",
            str(shard_q.relative_to(ROOT)).replace("\\", "/"),
            "--model",
            args.model,
            "--progress-file",
            str(prog.relative_to(ROOT)).replace("\\", "/"),
        ]
        log = SHARD_DIR / f"shard-{idx}.log"
        print(f"Shard {idx}: {len(chunk)} leaves -> {log.name}")
        f = log.open("w", encoding="utf-8")
        procs.append(subprocess.Popen(cmd, cwd=ROOT, stdout=f, stderr=subprocess.STDOUT))

    codes = [p.wait() for p in procs]
    merge_progress([SHARD_DIR / f"progress-{i}.json" for i in range(n)])
    failed_shards = sum(1 for c in codes if c != 0)
    merged = json.loads(PROGRESS_MAIN.read_text(encoding="utf-8"))
    print(f"Shards exit codes: {codes}; done={len(merged['done'])} failed={len(merged['failed'])}")
    return 1 if failed_shards else 0


if __name__ == "__main__":
    raise SystemExit(main())
