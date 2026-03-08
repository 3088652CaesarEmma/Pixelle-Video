---
name: pixelle-video
description: Generate AI short videos from text topics. Use when user wants to create videos, make short-form content, or produce visual media from text descriptions.
---

# Pixelle Video

Generate AI short videos from any topic. One command in, video out.

## Before You Start

**Always check if the API is running first:**

    python skill/pixelle.py health

If it prints "API is running." — proceed with commands below.
If it fails, start the server first: `uv run python api/app.py`

## Commands

Run from project root:

    python skill/pixelle.py health
    python skill/pixelle.py generate "<topic>"
    python skill/pixelle.py status <task_id>
    python skill/pixelle.py templates
    python skill/pixelle.py workflows
    python skill/pixelle.py bgm

## Quick Example

    python skill/pixelle.py generate "The history of the Roman Empire"

Returns a task ID. Poll with `status` until the video URL appears.

## Notes

- **Always run `health` before first `generate`** to confirm API is reachable.
- Video generation is async (~1-3 min). Always poll `status` after `generate`.
- Default output is portrait 1080x1920 (short video format).
- Default API address: http://localhost:8000. Set `PIXELLE_API_URL` env var to override.

## Advanced Usage

For more options, read the corresponding reference file:

- `skill/references/params.md` — All generate parameters (scenes, style, title, fps, etc.)
- `skill/references/templates.md` — Template selection and customization
- `skill/references/modes.md` — Different video creation modes
- `skill/references/workflows.md` — Media and TTS workflow configuration
- `skill/references/bgm.md` — Background music options
