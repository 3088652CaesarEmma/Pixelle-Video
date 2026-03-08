# Background Music

Add background music to generated videos.

## List Available BGM

    python skill/pixelle.py bgm

Shows all available music files with their source (default or custom).

## Using BGM

    python skill/pixelle.py generate "topic" --bgm "bgm/default.mp3"

## Adjusting Volume

BGM volume range is 0.0 (silent) to 1.0 (full). Default is 0.3.

    python skill/pixelle.py generate "topic" --bgm "bgm/happy.mp3" --bgm-volume 0.5

## BGM Sources

- `bgm/` — Built-in music files shipped with the project
- `data/bgm/` — Custom music files added by the user

Custom files with the same name override built-in ones.
