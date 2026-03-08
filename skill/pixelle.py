#!/usr/bin/env python3
"""
Pixelle-Video CLI Wrapper for OpenClaw Skill

This script provides a simplified CLI interface for the Pixelle-Video API,
hiding all HTTP complexity from the calling agent. The agent only needs to
know the command names and a few simple parameters.

Usage:
    python skill/pixelle.py health
    python skill/pixelle.py generate <topic> [options]
    python skill/pixelle.py status <task_id>
    python skill/pixelle.py templates
    python skill/pixelle.py workflows
    python skill/pixelle.py bgm
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request


API_URL = os.environ.get("PIXELLE_API_URL", "http://localhost:8000")


# ---------------------------------------------------------------------------
# HTTP helpers (stdlib only, no external dependencies)
# ---------------------------------------------------------------------------

def _request(method: str, path: str, body: dict | None = None) -> dict:
    url = f"{API_URL}{path}"
    data = json.dumps(body).encode() if body else None
    headers = {"Content-Type": "application/json"} if body else {}
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        err_body = e.read().decode() if e.fp else ""
        try:
            detail = json.loads(err_body).get("detail", err_body)
        except Exception:
            detail = err_body
        detail = detail.strip() if detail else f"HTTP {e.code} {e.reason}"
        print(f"Error: {detail}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(
            f"Error: Cannot connect to Pixelle-Video API at {API_URL}\n"
            f"Make sure the API server is running (uv run python api/app.py).\n"
            f"Detail: {e.reason}",
            file=sys.stderr,
        )
        sys.exit(1)


def _get(path: str) -> dict:
    return _request("GET", path)


def _post(path: str, body: dict) -> dict:
    return _request("POST", path, body)


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_health(args: argparse.Namespace) -> None:
    """Check if the Pixelle-Video API is running and reachable."""
    url = f"{API_URL}/health"
    req = urllib.request.Request(url, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            status = data.get("status", "unknown")
            version = data.get("version", "unknown")
            service = data.get("service", "Pixelle-Video API")
            print(f"API is running.")
            print(f"Service: {service}")
            print(f"Version: {version}")
            print(f"Status:  {status}")
            print(f"URL:     {API_URL}")
    except urllib.error.HTTPError as e:
        print(f"API is NOT healthy (HTTP {e.code}).", file=sys.stderr)
        print(f"The server at {API_URL} is reachable but not working properly.", file=sys.stderr)
        print(f"", file=sys.stderr)
        print(f"To start the API server, run:", file=sys.stderr)
        print(f"  uv run python api/app.py", file=sys.stderr)
        sys.exit(1)
    except (urllib.error.URLError, OSError) as e:
        reason = getattr(e, "reason", e)
        print(f"API is NOT reachable at {API_URL}", file=sys.stderr)
        print(f"Reason: {reason}", file=sys.stderr)
        print(f"", file=sys.stderr)
        print(f"To start the API server, run:", file=sys.stderr)
        print(f"  uv run python api/app.py", file=sys.stderr)
        sys.exit(1)


def cmd_generate(args: argparse.Namespace) -> None:
    """Generate a video from a topic / script text."""
    body: dict = {
        "text": args.topic,
        "frame_template": args.template or "1080x1920/image_default.html",
    }

    if args.mode:
        body["mode"] = args.mode
    if args.title:
        body["title"] = args.title
    if args.scenes is not None:
        body["n_scenes"] = args.scenes
    if args.style:
        body["prompt_prefix"] = args.style
    if args.workflow:
        body["media_workflow"] = args.workflow
    if args.tts:
        body["tts_workflow"] = args.tts
    if args.ref_audio:
        body["ref_audio"] = args.ref_audio
    if args.bgm:
        body["bgm_path"] = args.bgm
    if args.bgm_volume is not None:
        body["bgm_volume"] = args.bgm_volume
    if args.fps is not None:
        body["video_fps"] = args.fps
    if args.template_params:
        try:
            body["template_params"] = json.loads(args.template_params)
        except json.JSONDecodeError:
            print("Error: --template-params must be valid JSON", file=sys.stderr)
            sys.exit(1)

    result = _post("/api/video/generate/async", body)
    task_id = result.get("task_id", "unknown")

    print(f"Video generation started.\nTask ID: {task_id}")
    print(f"Run 'python skill/pixelle.py status {task_id}' to check progress.")


def cmd_status(args: argparse.Namespace) -> None:
    """Check status of a video generation task."""
    task_id = args.task_id
    result = _get(f"/api/tasks/{task_id}")

    status = result.get("status", "unknown")
    progress = result.get("progress")

    if status == "completed":
        res = result.get("result", {})
        video_url = res.get("video_url", "N/A")
        duration = res.get("duration", 0)
        file_size = res.get("file_size", 0)
        size_mb = file_size / (1024 * 1024) if file_size else 0
        print(f"Task {task_id}: completed")
        print(f"Video URL: {video_url}")
        print(f"Duration: {duration:.1f}s | Size: {size_mb:.1f}MB")
    elif status == "failed":
        error = result.get("error", "Unknown error")
        print(f"Task {task_id}: failed")
        print(f"Error: {error}")
    elif status == "cancelled":
        print(f"Task {task_id}: cancelled")
    else:
        progress_str = f" ({progress}%)" if progress is not None else ""
        print(f"Task {task_id}: {status}{progress_str}")


def cmd_templates(args: argparse.Namespace) -> None:
    """List available video templates."""
    result = _get("/api/resources/templates")
    templates = result.get("templates", [])

    if not templates:
        print("No templates available.")
        return

    print("Available templates:")
    for t in templates:
        key = t.get("key", t.get("path", ""))
        orientation = t.get("orientation", "")
        size = t.get("size", "")
        label = f" ({orientation}, {size})" if orientation else ""
        print(f"  - {key}{label}")


def cmd_workflows(args: argparse.Namespace) -> None:
    """List available media and TTS workflows."""
    media = _get("/api/resources/workflows/media")
    tts = _get("/api/resources/workflows/tts")

    media_wfs = media.get("workflows", [])
    tts_wfs = tts.get("workflows", [])

    if media_wfs:
        print("Media workflows (--workflow):")
        for w in media_wfs:
            key = w.get("key", w.get("name", ""))
            source = w.get("source", "")
            label = f" [{source}]" if source else ""
            print(f"  - {key}{label}")

    if tts_wfs:
        if media_wfs:
            print()
        print("TTS workflows (--tts):")
        for w in tts_wfs:
            key = w.get("key", w.get("name", ""))
            source = w.get("source", "")
            label = f" [{source}]" if source else ""
            print(f"  - {key}{label}")

    if not media_wfs and not tts_wfs:
        print("No workflows available.")


def cmd_bgm(args: argparse.Namespace) -> None:
    """List available background music files."""
    result = _get("/api/resources/bgm")
    bgm_files = result.get("bgm_files", [])

    if not bgm_files:
        print("No background music files available.")
        return

    print("Available BGM (--bgm):")
    for b in bgm_files:
        path = b.get("path", b.get("name", ""))
        source = b.get("source", "")
        label = f" [{source}]" if source else ""
        print(f"  - {path}{label}")


# ---------------------------------------------------------------------------
# CLI setup
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pixelle",
        description="Pixelle-Video: AI video generation CLI",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # --- health ---
    hl = sub.add_parser("health", help="Check if the API server is running")
    hl.set_defaults(func=cmd_health)

    # --- generate ---
    gen = sub.add_parser("generate", help="Generate a video from a topic")
    gen.add_argument("topic", help="Video topic or script text")
    gen.add_argument("--scenes", type=int, help="Number of scenes (1-20)")
    gen.add_argument("--template", help="Template key")
    gen.add_argument("--style", help="Image style prefix")
    gen.add_argument("--title", help="Video title")
    gen.add_argument("--mode", choices=["generate", "fixed"], help="Creation mode")
    gen.add_argument("--workflow", help="Media workflow key")
    gen.add_argument("--tts", help="TTS workflow key")
    gen.add_argument("--ref-audio", help="Reference audio for voice cloning")
    gen.add_argument("--bgm", help="Background music file path")
    gen.add_argument("--bgm-volume", type=float, help="BGM volume (0.0-1.0)")
    gen.add_argument("--fps", type=int, help="Video FPS (15-60)")
    gen.add_argument("--template-params", help="Template custom params (JSON string)")
    gen.set_defaults(func=cmd_generate)

    # --- status ---
    st = sub.add_parser("status", help="Check task status")
    st.add_argument("task_id", help="Task ID")
    st.set_defaults(func=cmd_status)

    # --- templates ---
    tpl = sub.add_parser("templates", help="List available templates")
    tpl.set_defaults(func=cmd_templates)

    # --- workflows ---
    wf = sub.add_parser("workflows", help="List available workflows")
    wf.set_defaults(func=cmd_workflows)

    # --- bgm ---
    bg = sub.add_parser("bgm", help="List available background music")
    bg.set_defaults(func=cmd_bgm)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
