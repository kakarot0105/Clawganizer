# Changelog

All notable changes to this project will be documented in this file.

## [2.0.0] - 2026-10-15

### Added
- Global pip-installable package (`clawganizer` console script)
- `clawganizer run` organizes whole-computer clutter (Downloads, Desktop, …)
- Dry-run by default; `--apply` to move files
- Move logging + `clawganizer undo`
- User config at `~/.config/clawganizer/config.json`
- `status`, `init`, `config` commands
- Pytest suite for organizer + CLI

### Changed
- Primary product is now a system-wide organizer, not only an OpenClaw skill
- OpenClaw `src/run.sh` bridges to the Python CLI when installed

### Kept
- `clawganizer workspace …` for OpenClaw project folders

## [1.0.0] - 2026-03-20

### Added
- Initial OpenClaw skill release
- List / create / archive / organize / status / docs commands

---

Uses [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
