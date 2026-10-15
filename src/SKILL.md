---
name: clawganizer
description: "Clawganizer — organize your whole computer. Prefer the global CLI: pip install + clawganizer run --apply. Also manages OpenClaw project workspaces."
user-invocable: true
metadata: { "openclaw": { "emoji": "📁", "requires": {} } }
---

# Clawganizer

Global installer (recommended):

```bash
pip install git+https://github.com/kakarot0105/Clawganizer.git
clawganizer run          # dry-run preview
clawganizer run --apply  # organize Downloads + Desktop
clawganizer undo
```

Skill bridge (`run.sh`) forwards to the CLI when available.

## OpenClaw skill usage

```bash
/clawganizer "organize"
/clawganizer "status"
/clawganizer "create project MyProject"
/clawganizer "list projects"
/clawganizer "archive OldProject"
```

## Configuration

`~/.config/clawganizer/config.json` (create with `clawganizer init`)
