# Clawganizer

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

Organize your **whole computer** with one command.

Install once, then run `clawganizer` (or `clawganizer run --apply`) to sort loose files from Downloads, Desktop, and other clutter folders into clear homes: Pictures, Documents, Videos, Archives, and more.

## Quick start

```bash
# Install globally (pip)
pip install git+https://github.com/kakarot0105/Clawganizer.git

# Or from a local clone
pip install .

# Preview what would move (safe default)
clawganizer
# same as:
clawganizer run

# Actually organize your computer
clawganizer run --apply

# Tornado UI — press Run
clawganizer ui

# Undo the last applied run
clawganizer undo
```

## UI

```bash
clawganizer ui
```

Opens a local page with a big **Run** button. Pressing it plays a full-screen tornado takeover, then organizes Downloads/Desktop (same engine as the CLI).

## What `run` does

By default Clawganizer scans **top-level files** in:

| Folder | Default |
|--------|---------|
| `~/Downloads` | on |
| `~/Desktop` | on |
| `~/Documents` | off |
| `~/Pictures` | off |

It sorts by type (and screenshot name patterns), for example:

- Images → `~/Pictures/Organized`
- Screenshots → `~/Pictures/Screenshots`
- PDFs / Office → `~/Documents/Organized`
- Videos → `~/Videos/Organized`
- Audio → `~/Music/Organized`
- Archives → `~/Archives`
- Installers → `~/Installers`
- Code snippets → `~/Documents/Code`
- Everything else → `~/Organized/Other`

Nested folders (projects, app bundles, etc.) are left alone. Moves are logged so you can `clawganizer undo`.

## Commands

```bash
clawganizer                 # dry-run organize (whole computer)
clawganizer run             # dry-run
clawganizer run --apply     # move files
clawganizer run --targets Downloads Desktop
clawganizer run --path ~/Downloads --apply
clawganizer status          # pending clutter summary
clawganizer init            # write ~/.config/clawganizer/config.json
clawganizer config          # print effective config
clawganizer undo            # restore last applied run
clawganizer undo --dry-run
```

### Optional OpenClaw workspace helpers

```bash
clawganizer workspace organize
clawganizer workspace create my-app
clawganizer workspace list
clawganizer workspace archive my-app
clawganizer workspace status
```

OpenClaw skill install (Telegram `/clawganizer`) is still documented in [docs/INSTALLATION.md](docs/INSTALLATION.md).

## Configuration

```bash
clawganizer init
$EDITOR ~/.config/clawganizer/config.json
```

Toggle targets, extension → folder maps, and screenshot patterns. See [docs/CONFIG.md](docs/CONFIG.md).

## Documentation

- [Installation](docs/INSTALLATION.md)
- [Usage](docs/USAGE.md)
- [Configuration](docs/CONFIG.md)
- [Contributing](CONTRIBUTING.md)

## Development

```bash
pip install -e ".[dev]"
pytest
```

## License

MIT — see [LICENSE](LICENSE).

## Author

**Kakarot0105**
