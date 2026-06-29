#!/usr/bin/env python3
"""
Hierarchy Expander — single entry point for any registered brainstorming topic.

Usage:
  python scripts/automation/hierarchy-expander-run.py --topic full-automation register --source documents/....md
  python scripts/automation/hierarchy-expander-run.py --topic full-automation init
  python scripts/automation/hierarchy-expander-run.py --topic full-automation pipeline
  python scripts/automation/hierarchy-expander-run.py --topic full-automation certify
  python scripts/automation/hierarchy-expander-run.py --topic full-automation status
  python scripts/automation/hierarchy-expander-run.py list
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from hierarchy_topic_config import (  # noqa: E402
    DEFAULT_MAX_PASSES,
    DEFAULT_MIN_PASSES,
    ROOT as _ROOT,
    default_paths_for_topic,
    list_topics,
    register_topic,
    resolve_topic,
    slugify,
)

TEMPLATE_DIR = ROOT / "docs/automation/templates/hierarchy-expansion"
PY = sys.executable


def run(cmd: list[str]) -> int:
    r = subprocess.run(cmd, cwd=ROOT)
    return r.returncode


def cmd_register(args: argparse.Namespace) -> int:
    cfg = register_topic(
        args.topic,
        source=args.source,
        output_dir=args.output_dir,
        title=args.title or args.topic.replace("-", " ").title(),
    )
    slug = slugify(args.topic)
    prompt_dst = cfg.prompt
    if not prompt_dst.is_file():
        prompt_dst.parent.mkdir(parents=True, exist_ok=True)
        tmpl = TEMPLATE_DIR / "expansion-prompt.template.md"
        text = tmpl.read_text(encoding="utf-8") if tmpl.is_file() else "# Hierarchy expansion\n"
        text = text.replace("<QUEUE_PATH>", cfg.rel(cfg.queue))
        text = text.replace("<OUTPUT_DIR>", cfg.rel(cfg.output_dir))
        prompt_dst.write_text(text, encoding="utf-8")
    cfg.output_dir.mkdir(parents=True, exist_ok=True)
    print(json.dumps({
        "registered": args.topic,
        "source": cfg.rel(cfg.source),
        "queue": cfg.rel(cfg.queue),
        "output_dir": cfg.rel(cfg.output_dir),
        "prompt": cfg.rel(cfg.prompt),
    }, indent=2))
    print(f"\nNext: python scripts/automation/hierarchy-expander-run.py --topic {args.topic} init")
    return 0


def cmd_init(args: argparse.Namespace) -> int:
    cfg = resolve_topic(args.topic, source=args.source, output_dir=args.output_dir)
    if not cfg.source.is_file():
        print(f"ERROR: hierarchy source missing: {cfg.source}", file=sys.stderr)
        return 1
    cmd = [
        PY, "scripts/automation/init-hierarchy-queue.py",
        "--queue", cfg.rel(cfg.queue),
        "--source", cfg.rel(cfg.source),
        "--prompt", cfg.rel(cfg.prompt),
        "--output-dir", cfg.rel(cfg.output_dir),
        "--mode", args.mode,
    ]
    if cfg.queue_data_module is None and args.mode == "full":
        print("WARN: no queue_data_module — use --mode bootstrap or add LEAVES to a queue data module", file=sys.stderr)
    return run(cmd)


def cmd_pipeline(args: argparse.Namespace) -> int:
    cfg = resolve_topic(args.topic, source=args.source, output_dir=args.output_dir)
    min_passes = args.min_passes if args.min_passes is not None else cfg.min_passes
    max_passes = args.max_passes if args.max_passes is not None else cfg.max_passes
    cmd = [
        PY, "scripts/automation/run-hierarchy-full-pipeline.py",
        "--queue", cfg.rel(cfg.queue),
        "--output-dir", cfg.rel(cfg.output_dir),
        "--ledger", cfg.rel(cfg.ledger),
        "--source", cfg.rel(cfg.source),
        "--quality-json", cfg.rel(cfg.quality_report_json),
        "--quality-md", cfg.rel(cfg.quality_report_md),
        "--signoff", cfg.rel(cfg.signoff_bundle),
        "--min-passes", str(min_passes),
        "--max-passes", str(max_passes),
        "--threshold", str(args.threshold),
    ]
    if cfg.queue_data_module:
        cmd.extend(["--queue-data-module", cfg.queue_data_module])
    if args.verify_only:
        cmd.append("--verify-only")
    if args.skip_iterate:
        cmd.append("--skip-iterate")
    code = run(cmd)
    if code == 0:
        return cmd_certify(args)
    return code


def cmd_timeline_agent(args: argparse.Namespace) -> int:
    cfg = resolve_topic(args.topic, source=args.source, output_dir=args.output_dir)
    cmd = [PY, "scripts/automation/hierarchy_agent_timeline.py", args.timeline_cmd]
    if args.timeline_cmd == "queue":
        cmd.extend(["--output-dir", cfg.rel(cfg.output_dir), "--out", "docs/automation/hierarchy-timeline-agent-queue.json"])
        if args.group:
            cmd.extend(["--group", args.group])
        if args.ids:
            cmd.extend(["--ids", args.ids])
    elif args.timeline_cmd in ("run-cli", "run-sdk", "apply-all"):
        cmd.extend(["--output-dir", cfg.rel(cfg.output_dir)])
        if args.group:
            cmd.extend(["--group", args.group])
        if args.ids:
            cmd.extend(["--ids", args.ids])
        if args.limit:
            cmd.extend(["--limit", str(args.limit)])
        if args.model:
            cmd.extend(["--model", args.model])
        if args.force and args.timeline_cmd == "apply-all":
            cmd.append("--force")
    return run(cmd)


def cmd_prose_agent(args: argparse.Namespace) -> int:
    cfg = resolve_topic(args.topic, source=args.source, output_dir=args.output_dir)
    cmd = [PY, "scripts/automation/hierarchy_agent_prose.py", args.prose_cmd]
    if args.prose_cmd == "queue":
        cmd.extend(["--output-dir", cfg.rel(cfg.output_dir), "--out", "docs/automation/hierarchy-prose-agent-queue.json"])
        if args.group:
            cmd.extend(["--group", args.group])
        if args.ids:
            cmd.extend(["--ids", args.ids])
    elif args.prose_cmd == "run-sdk":
        cmd.extend(["--output-dir", cfg.rel(cfg.output_dir)])
        if args.group:
            cmd.extend(["--group", args.group])
        if args.ids:
            cmd.extend(["--ids", args.ids])
        if args.limit:
            cmd.extend(["--limit", str(args.limit)])
        if args.model:
            cmd.extend(["--model", args.model])
    elif args.prose_cmd == "apply-pilot":
        return run([PY, "scripts/automation/hierarchy_agent_prose_pilot.py"])
    elif args.prose_cmd == "apply-meta":
        return run([PY, "scripts/automation/hierarchy_agent_prose_meta.py"])
    elif args.prose_cmd == "apply-plane-a":
        return run([PY, "scripts/automation/hierarchy_agent_prose_plane_a_rest.py"])
    elif args.prose_cmd == "apply-plane-b":
        return run([PY, "scripts/automation/hierarchy_agent_prose_plane_b.py"])
    elif args.prose_cmd == "apply-plane-c":
        return run([PY, "scripts/automation/hierarchy_agent_prose_plane_c.py"])
    elif args.prose_cmd == "apply-plane-d":
        return run([PY, "scripts/automation/hierarchy_agent_prose_plane_d.py"])
    elif args.prose_cmd == "apply-plane-e":
        return run([PY, "scripts/automation/hierarchy_agent_prose_plane_e.py"])
    elif args.prose_cmd == "apply-plane-f":
        return run([PY, "scripts/automation/hierarchy_agent_prose_plane_f.py"])
    elif args.prose_cmd == "apply-plane-g":
        return run([PY, "scripts/automation/hierarchy_agent_prose_plane_g.py"])
    elif args.prose_cmd == "apply-plane-h":
        return run([PY, "scripts/automation/hierarchy_agent_prose_plane_h.py"])
    elif args.prose_cmd == "apply-plane-i":
        return run([PY, "scripts/automation/hierarchy_agent_prose_plane_i.py"])
    elif args.prose_cmd == "apply-plane-j":
        return run([PY, "scripts/automation/hierarchy_agent_prose_plane_j.py"])
    elif args.prose_cmd == "apply-all":
        return run([PY, "scripts/automation/hierarchy_agent_prose_apply_all.py"])
    elif args.prose_cmd == "brief":
        if not args.id:
            print("--id required for brief", file=sys.stderr)
            return 1
        cmd.extend(["--id", args.id, "--output-dir", cfg.rel(cfg.output_dir)])
    return run(cmd)


def cmd_publish(args: argparse.Namespace) -> int:
    cfg = resolve_topic(args.topic, source=args.source, output_dir=args.output_dir)
    html_dir = args.html_dir or str((cfg.output_dir / "html-site").relative_to(ROOT)).replace("\\", "/")
    cmd = [
        PY, "scripts/automation/hierarchy-html-publish.py",
        "--topic", args.topic,
        "--output-dir", cfg.rel(cfg.output_dir),
        "--html-dir", html_dir,
    ]
    if cfg.html_site_config:
        cmd.extend(["--html-site-config", cfg.html_site_config])
    if cfg.html_glossary:
        cmd.extend(["--html-glossary", cfg.html_glossary])
    code = run(cmd)
    if code == 0:
        run([PY, "scripts/automation/verify-book-complete.py"])
    return code


def cmd_certify(args: argparse.Namespace) -> int:
    cfg = resolve_topic(args.topic, source=args.source, output_dir=args.output_dir)
    code = run([
        PY, "scripts/automation/generate-hierarchy-quality-report.py",
        "--output-dir", cfg.rel(cfg.output_dir),
        "--ledger", cfg.rel(cfg.ledger),
        "--source", cfg.rel(cfg.source),
        "--quality-json", cfg.rel(cfg.quality_report_json),
        "--quality-md", cfg.rel(cfg.quality_report_md),
    ])
    if cfg.quality_report_md.is_file():
        print(f"\nReport: {cfg.quality_report_md}")
    return code


def cmd_status(args: argparse.Namespace) -> int:
    cfg = resolve_topic(args.topic, source=args.source, output_dir=args.output_dir)
    out = {}
    if cfg.quality_report_json.is_file():
        out["quality"] = json.loads(cfg.quality_report_json.read_text(encoding="utf-8"))
    else:
        out["quality"] = {"certified_for_human_review": False, "note": "run certify"}
    _, verify_out = _run_capture([
        PY, "scripts/automation/verify-hierarchy-expansion.py",
        "--queue", cfg.rel(cfg.queue),
        "--output-dir", cfg.rel(cfg.output_dir),
    ])
    if "{" in verify_out:
        out["structure"] = json.loads(verify_out[verify_out.index("{"):])
    out["paths"] = {
        "source": cfg.rel(cfg.source),
        "queue": cfg.rel(cfg.queue),
        "output_dir": cfg.rel(cfg.output_dir),
        "ledger": cfg.rel(cfg.ledger),
        "quality_report_md": cfg.rel(cfg.quality_report_md),
    }
    print(json.dumps(out, indent=2))
    certified = out.get("quality", {}).get("certified_for_human_review", False)
    return 0 if certified else 1


def _run_capture(cmd: list[str]) -> tuple[int, str]:
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def cmd_list(_: argparse.Namespace) -> int:
    data = json.loads((ROOT / "docs/automation/hierarchy-topics.json").read_text(encoding="utf-8"))
    for name, t in sorted(data.get("topics", {}).items()):
        print(f"  {name}: {t.get('title', name)}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Hierarchy Expander — unified CLI")
    parser.add_argument("--topic", default="full-automation", help="Registered topic id")
    parser.add_argument("--source", help="Override hierarchy markdown path")
    parser.add_argument("--output-dir", help="Override leaf output directory")
    sub = parser.add_subparsers(dest="command", required=True)

    p_reg = sub.add_parser("register", help="Register new topic in hierarchy-topics.json")
    p_reg.add_argument("--title", help="Human title")
    p_reg.set_defaults(func=cmd_register)

    p_init = sub.add_parser("init", help="Initialize unified queue")
    p_init.add_argument("--mode", choices=("bootstrap", "full"), default="bootstrap")
    p_init.set_defaults(func=cmd_init)

    p_pipe = sub.add_parser("pipeline", help="Iterate all nodes (default 3 passes, then certify)")
    p_pipe.add_argument(
        "--min-passes",
        type=int,
        default=None,
        help=f"Minimum full iterations before cert exit (default {DEFAULT_MIN_PASSES})",
    )
    p_pipe.add_argument(
        "--max-passes",
        type=int,
        default=None,
        help=f"Max iterations (default {DEFAULT_MAX_PASSES}; use 0 for unlimited until certified)",
    )
    p_pipe.add_argument("--threshold", type=int, default=90)
    p_pipe.add_argument("--verify-only", action="store_true")
    p_pipe.add_argument("--skip-iterate", action="store_true")
    p_pipe.set_defaults(func=cmd_pipeline)

    p_pub = sub.add_parser("publish", help="Generate static HTML site from certified hierarchy")
    p_pub.add_argument("--html-dir", help="Override HTML output directory")
    p_pub.set_defaults(func=cmd_publish)

    p_prose = sub.add_parser("prose-agent", help="Agent-authored Reader narrative (book-quality prose)")
    p_prose.add_argument(
        "prose_cmd",
        choices=[
            "queue", "run-sdk", "apply-pilot", "apply-meta", "apply-all",
            "apply-plane-a", "apply-plane-b", "apply-plane-c", "apply-plane-d",
            "apply-plane-e", "apply-plane-f", "apply-plane-g", "apply-plane-h",
            "apply-plane-i", "apply-plane-j", "brief",
        ],
        help="queue=work JSON; run-sdk=Cursor agent batch; apply-*=batch apply; brief=research JSON",
    )
    p_prose.add_argument("--group", help="Limit to group e.g. A1, B3")
    p_prose.add_argument("--ids", help="Comma-separated capability ids")
    p_prose.add_argument("--id", help="Single id for brief")
    p_prose.add_argument("--limit", type=int, default=0, help="Max leaves for run-sdk")
    p_prose.add_argument("--model", default="composer-2.5")
    p_prose.set_defaults(func=cmd_prose_agent)

    p_timeline = sub.add_parser("timeline-agent", help="Agent-authored timeline steps (S0, Cursor CLI, or SDK)")
    p_timeline.add_argument(
        "timeline_cmd",
        choices=["queue", "run-cli", "run-sdk", "apply-all"],
        help="queue=work JSON; run-cli=agent -p; run-sdk=cursor-sdk; apply-all=narrative extract (S0)",
    )
    p_timeline.add_argument("--group", help="Limit to group e.g. A1, INTRO")
    p_timeline.add_argument("--ids", help="Comma-separated capability ids")
    p_timeline.add_argument("--limit", type=int, default=0, help="Max leaves for run-cli/run-sdk")
    p_timeline.add_argument("--model", default="composer-2.5")
    p_timeline.add_argument("--force", action="store_true", help="Re-apply S0 timelines on apply-all")
    p_timeline.set_defaults(func=cmd_timeline_agent)

    sub.add_parser("certify", help="Generate quality certification report").set_defaults(func=cmd_certify)

    sub.add_parser("status", help="Topic status + certification").set_defaults(func=cmd_status)

    sub.add_parser("list", help="List registered topics").set_defaults(func=cmd_list)

    args = parser.parse_args()
    if args.command == "list":
        return cmd_list(args)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
