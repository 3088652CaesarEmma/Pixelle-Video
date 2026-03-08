# Generate Parameters

Full parameter reference for the `generate` command.

## Usage

    python skill/pixelle.py generate <topic> [options]

## Parameters

| Flag | Description | Default |
|------|-------------|---------|
| `--scenes N` | Number of scenes to generate (1-20) | 5 |
| `--title TEXT` | Video title | AI-generated |
| `--style TEXT` | Image style prefix (e.g. "watercolor painting", "cyberpunk", "anime") | None |
| `--template KEY` | Frame template key (run `templates` to list) | 1080x1920/image_default.html |
| `--mode MODE` | Creation mode: `generate` or `fixed` (see modes.md) | generate |
| `--workflow KEY` | Media workflow key (run `workflows` to list) | Server default |
| `--tts KEY` | TTS workflow key (run `workflows` to list) | Server default |
| `--ref-audio PATH` | Reference audio file for voice cloning | None |
| `--bgm PATH` | Background music file path (run `bgm` to list) | None |
| `--bgm-volume N` | BGM volume level (0.0 to 1.0) | 0.3 |
| `--fps N` | Video frames per second (15-60) | 30 |
| `--template-params JSON` | Custom template parameters as JSON string | None |

## Examples

Basic — just a topic:

    python skill/pixelle.py generate "Space exploration in 2030"

With style and scene count:

    python skill/pixelle.py generate "History of coffee" --scenes 8 --style "vintage illustration"

With custom title and landscape template:

    python skill/pixelle.py generate "AI revolution" --title "The AI Era" --template "1920x1080/image_default.html"

With fixed narration text (no AI rewriting):

    python skill/pixelle.py generate "Line one. Line two. Line three." --mode fixed

With template customization:

    python skill/pixelle.py generate "Ocean life" --template-params '{"accent_color": "#0077be"}'
