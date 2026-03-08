# Creation Modes

Pixelle-Video supports different modes for video creation.

## Standard Mode (default)

Input a topic, AI automatically generates narration script, images, and assembles the video.

    python skill/pixelle.py generate "The rise of electric vehicles"

The AI will:
1. Generate narration scripts from the topic
2. Create image prompts for each scene
3. Generate images via ComfyUI
4. Synthesize voice via TTS
5. Assemble the final video with BGM

## Fixed Text Mode

Provide your exact narration text — the AI will NOT rewrite it. Each sentence becomes one scene.

    python skill/pixelle.py generate "Scene one text. Scene two text. Scene three text." --mode fixed

Use this when:
- You have a pre-written script
- You need precise control over the narration
- You want to skip the AI text generation step

## Controlling Scene Count

In standard mode, use `--scenes` to control how many scenes are generated:

    python skill/pixelle.py generate "History of Rome" --scenes 8

In fixed mode, `--scenes` is ignored — scene count is determined by your text.
