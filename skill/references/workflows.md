# Workflows

Workflows control which AI models are used for image/video generation and TTS.

## List All Workflows

    python skill/pixelle.py workflows

This shows both media workflows and TTS workflows.

## Media Workflows

Media workflows control how scene images or videos are generated (via ComfyUI).

    python skill/pixelle.py generate "topic" --workflow "runninghub/image_flux.json"

Common types:
- `image_*` — Generate static images (e.g. Flux, SDXL)
- `video_*` — Generate video clips (e.g. Wan2.1)

If omitted, the server uses its default workflow from config.

## TTS Workflows

TTS workflows control voice synthesis.

    python skill/pixelle.py generate "topic" --tts "runninghub/tts_edge.json"

Common types:
- `tts_edge*` — Microsoft Edge TTS (fast, multiple voices)
- `tts_index*` — Index-TTS (supports voice cloning)

## Voice Cloning

Some TTS workflows support voice cloning with a reference audio file:

    python skill/pixelle.py generate "topic" --tts "runninghub/tts_index2.json" --ref-audio "/path/to/voice_sample.wav"

## Workflow Sources

Workflows come from two sources:
- `runninghub` — Cloud-hosted via RunningHub
- `selfhost` — Local ComfyUI instance

The source is shown in brackets when you run `workflows`.
