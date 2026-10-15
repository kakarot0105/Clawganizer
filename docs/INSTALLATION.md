# Installation Guide

## Requirements

- Python 3.9+
- macOS or Linux (Windows via WSL is fine)
- Write access to your home directory

## Global install (recommended)

### From GitHub

```bash
pip install --user git+https://github.com/kakarot0105/Clawganizer.git
```

Ensure your user scripts directory is on `PATH` (often `~/.local/bin`):

```bash
export PATH="$HOME/.local/bin:$PATH"
# add that line to ~/.bashrc or ~/.zshrc for persistence
```

Verify:

```bash
clawganizer --version
clawganizer status
```

### From a clone

```bash
git clone https://github.com/kakarot0105/Clawganizer.git
cd Clawganizer
pip install --user .
```

### Editable (development)

```bash
pip install -e ".[dev]"
pytest
```

## First run

```bash
# Always starts as a dry-run preview
clawganizer run

# When the plan looks right:
clawganizer run --apply
```

Optional: write a config file before applying:

```bash
clawganizer init
```

## OpenClaw skill (optional)

If you also use OpenClaw / Telegram skills:

```bash
mkdir -p ~/.openclaw/skills
cp -r . ~/.openclaw/skills/clawganizer/
# or: git clone … into ~/.openclaw/skills/clawganizer
```

The skill’s `src/run.sh` forwards to the `clawganizer` CLI when installed, and falls back to a small bash helper otherwise.

```bash
bash ~/.openclaw/skills/clawganizer/src/run.sh "status"
```

## Troubleshooting

### `clawganizer: command not found`

- Confirm install: `python3 -m pip show clawganizer`
- Put scripts on PATH: `python3 -m site --user-base` → add `bin` under that path
- Or run via module: `python3 -m clawganizer run`

### Permission denied moving files

- Do not run as root
- Check ownership of the source file and destination folder
- Use `clawganizer run` (dry-run) to inspect the plan first

### Want to reverse a run

```bash
clawganizer undo --dry-run
clawganizer undo
```

## Next steps

- [USAGE.md](USAGE.md) — command reference
- [CONFIG.md](CONFIG.md) — customize targets and categories
