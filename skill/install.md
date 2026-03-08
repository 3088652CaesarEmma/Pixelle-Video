## Install Pixelle-Video Skill

Please follow these steps to install the Pixelle-Video AI video generation skill into your workspace.

### Step 1: Clone the repository

```bash
git clone -b dev_skills https://github.com/AIDC-AI/Pixelle-Video.git
cd Pixelle-Video
```

### Step 2: Install dependencies

```bash
uv sync
```

If `uv` is not installed, install it first: `curl -LsSf https://astral.sh/uv/install.sh | sh`

### Step 3: Start the API server

```bash
uv run python api/app.py
```

Keep this running in the background.

### Step 4: Verify installation

```bash
python skill/pixelle.py health
```

If it prints "API is running." — installation is complete.

### Step 5: Copy skill files into your workspace

Copy the `skill/` folder into your agent workspace's skills directory:

```bash
cp -r skill/ ~/.openclaw/workspace/skills/pixelle-video/
```

Then read `skill/SKILL.md` to learn all available commands.

### Quick Test

```bash
python skill/pixelle.py generate "The history of the Roman Empire"
```

This returns a task ID. Check progress with:

```bash
python skill/pixelle.py status <task_id>
```

When status is "completed", the video URL will be shown.
