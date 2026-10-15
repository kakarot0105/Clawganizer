# Usage Guide

## Organize your computer

### Preview (default)

```bash
clawganizer
clawganizer run
```

Shows every planned move. Nothing is changed.

### Apply

```bash
clawganizer run --apply
```

Moves top-level files from enabled targets into category folders under your home directory.

### Limit scope

```bash
# Only Downloads
clawganizer run --targets Downloads --apply

# Only Desktop + Downloads
clawganizer run --targets Desktop Downloads --apply

# A custom folder
clawganizer run --path ~/Inbox --apply
```

### Check pending clutter

```bash
clawganizer status
```

### Undo

```bash
clawganizer undo --dry-run
clawganizer undo
```

Restores files from the most recent **applied** run log.

## Safety model

- Default is **dry-run**; you must pass `--apply` to move files
- Only **top-level files** in target folders are considered (not recursive)
- Directories, symlinks, and hidden files are skipped
- Name collisions get a `_1`, `_2`, … suffix
- Every apply writes a JSON log under `~/.local/share/clawganizer/logs/`

## OpenClaw workspace commands

```bash
clawganizer workspace organize
clawganizer workspace create MyApp
clawganizer workspace list
clawganizer workspace archive MyApp
clawganizer workspace status
```

These manage `~/.openclaw/projects/{active,archived}` and related folders.

## Typical workflows

### New machine cleanup

```bash
clawganizer init
clawganizer status
clawganizer run                 # review
clawganizer run --apply         # clean Downloads + Desktop
```

### Weekly tidy

```bash
clawganizer run --targets Downloads --apply
```

### After a bad apply

```bash
clawganizer undo
```
