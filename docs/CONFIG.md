# Configuration

## Environment Variables

Override default settings with environment variables:

```bash
# Custom workspace location
export WORKSPACE=/custom/path
/clawganizer "status"

# Example: Use project-specific workspace
export WORKSPACE=$HOME/myproject/.openclaw
/clawganizer "organize"
```

## Default Locations

| Location | Purpose |
|----------|---------|
| `~/.openclaw/projects/active/` | Active projects |
| `~/.openclaw/projects/archived/` | Archived projects |
| `~/.openclaw/venvs/` | Virtual environments |
| `~/.openclaw/workspace/` | Workspace files |

## Customization

To customize Clawganizer, modify `src/run.sh`:

```bash
# Edit the skill
nano ~/.openclaw/skills/clawganizer/src/run.sh

# Modify folder names, behaviors, etc.
```

