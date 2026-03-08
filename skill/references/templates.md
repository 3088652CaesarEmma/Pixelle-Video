# Templates

Templates control the visual layout and size of the generated video.

## List Templates

    python skill/pixelle.py templates

## Orientations

Templates are organized by output size:

| Size | Orientation | Use Case |
|------|-------------|----------|
| 1080x1920 | Portrait | TikTok, Reels, Shorts |
| 1920x1080 | Landscape | YouTube, presentations |
| 1080x1080 | Square | Instagram, social posts |

## Using a Template

    python skill/pixelle.py generate "topic" --template "1080x1920/image_default.html"

If `--template` is omitted, defaults to portrait (1080x1920/image_default.html).

## Template Types

- `image_*` — Static image background with subtitle overlay
- `video_*` — Video clip background with subtitle overlay
- `static_*` — Solid/gradient background with text

## Custom Template Parameters

Some templates support custom styling via `--template-params` (JSON):

    python skill/pixelle.py generate "topic" --template-params '{"accent_color": "#ff6600", "font_size": "48px"}'

Available parameters depend on the specific template. Common ones:
- `accent_color` — Highlight/accent color (hex)
- `background` — Custom background image URL
- `font_size` — Text font size
- `text_color` — Text color (hex)
