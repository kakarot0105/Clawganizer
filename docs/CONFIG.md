# Configuration

## Config file

```bash
clawganizer init
# writes ~/.config/clawganizer/config.json
```

Override the config directory with `CLAWGANIZER_CONFIG_DIR`.
Override log directory with `CLAWGANIZER_LOG_DIR`.

## Targets

```json
"targets": {
  "Downloads": true,
  "Desktop": true,
  "Documents": false,
  "Pictures": false
}
```

Only enabled targets that exist under `$HOME` are scanned.

## Destination root

```json
"destination_root": "~"
```

Category folders are created under this root (default: your home directory).

## Extension maps

```json
"folders": {
  "Images": ["jpg", "png", "gif", "..."],
  "Videos": ["mp4", "mov", "..."]
}
```

Unknown extensions go to `Organized/Other`.

## Screenshots

```json
"screenshot_patterns": ["Screenshot*", "Screen Shot*", "CleanShot*", "Capture*"]
```

Matching filenames go to `Pictures/Screenshots` regardless of extension category.

## Destination layout

| Category | Destination |
|----------|-------------|
| Images | `~/Pictures/Organized` |
| Screenshots | `~/Pictures/Screenshots` |
| Videos | `~/Videos/Organized` |
| Audio | `~/Music/Organized` |
| Documents | `~/Documents/Organized` |
| Code | `~/Documents/Code` |
| Archives | `~/Archives` |
| Installers | `~/Installers` |
| Fonts | `~/Fonts` |
| Ebooks | `~/Documents/Ebooks` |
| Other | `~/Organized/Other` |

## OpenClaw workspace env

```bash
export WORKSPACE=/custom/path
clawganizer workspace status
```

## Inspect effective config

```bash
clawganizer config
```
