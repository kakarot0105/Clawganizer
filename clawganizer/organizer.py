"""Whole-computer file organization engine."""

from __future__ import annotations

import json
import re
import shutil
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from fnmatch import fnmatch
from pathlib import Path
from typing import Any, Iterable

from .config import LOG_DIR, expand_path, load_config


@dataclass
class MoveAction:
    source: str
    destination: str
    category: str
    dry_run: bool


@dataclass
class OrganizeResult:
    moved: list[MoveAction] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    log_path: str | None = None

    @property
    def move_count(self) -> int:
        return len(self.moved)


def _home_subdir(name: str) -> Path:
    return Path.home() / name


def enabled_source_dirs(config: dict[str, Any]) -> list[Path]:
    targets = config.get("targets", {})
    dirs: list[Path] = []
    for name, enabled in targets.items():
        if not enabled:
            continue
        path = _home_subdir(name)
        if path.is_dir():
            dirs.append(path)
    return dirs


def extension_map(config: dict[str, Any]) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for category, extensions in config.get("folders", {}).items():
        for ext in extensions:
            mapping[ext.lower().lstrip(".")] = category
    return mapping


def is_skipped(path: Path, config: dict[str, Any]) -> bool:
    if config.get("skip_hidden", True) and path.name.startswith("."):
        return True
    skip_names = set(config.get("skip_names", []))
    if path.name in skip_names:
        return True
    return False


def categorize(path: Path, config: dict[str, Any], ext_map: dict[str, str]) -> str | None:
    for pattern in config.get("screenshot_patterns", []):
        if fnmatch(path.name, pattern):
            return "Screenshots"

    if path.is_dir():
        # Leave directories alone in whole-computer mode — safer default.
        return None

    ext = path.suffix.lower().lstrip(".")
    if not ext:
        return "Other"
    return ext_map.get(ext, "Other")


def unique_destination(dest_dir: Path, filename: str, max_collisions: int) -> Path:
    candidate = dest_dir / filename
    if not candidate.exists():
        return candidate

    stem = Path(filename).stem
    suffix = Path(filename).suffix
    for index in range(1, max_collisions + 1):
        candidate = dest_dir / f"{stem}_{index}{suffix}"
        if not candidate.exists():
            return candidate
    raise FileExistsError(f"Too many name collisions for {filename} in {dest_dir}")


def destination_for(
    category: str,
    source: Path,
    config: dict[str, Any],
) -> Path:
    root = expand_path(config.get("destination_root", "~"))
    # Keep Screenshots under Pictures for a natural layout.
    if category == "Screenshots":
        dest_dir = root / "Pictures" / "Screenshots"
    elif category == "Images":
        dest_dir = root / "Pictures" / "Organized"
    elif category == "Videos":
        dest_dir = root / "Videos" / "Organized"
    elif category == "Audio":
        dest_dir = root / "Music" / "Organized"
    elif category == "Documents":
        dest_dir = root / "Documents" / "Organized"
    elif category == "Code":
        dest_dir = root / "Documents" / "Code"
    elif category == "Archives":
        dest_dir = root / "Archives"
    elif category == "Installers":
        dest_dir = root / "Installers"
    elif category == "Fonts":
        dest_dir = root / "Fonts"
    elif category == "Ebooks":
        dest_dir = root / "Documents" / "Ebooks"
    else:
        dest_dir = root / "Organized" / "Other"

    max_collisions = int(config.get("max_name_collisions", 1000))
    return unique_destination(dest_dir, source.name, max_collisions)


def iter_loose_files(source_dir: Path, config: dict[str, Any]) -> Iterable[Path]:
    """Only organize top-level files in each target folder (non-recursive).

    Recursive whole-home sweeps are dangerous; clutter lives on the surface
    of Downloads/Desktop. Nested project trees stay untouched.
    """
    try:
        entries = sorted(source_dir.iterdir(), key=lambda p: p.name.lower())
    except PermissionError:
        return

    for entry in entries:
        if is_skipped(entry, config):
            continue
        if entry.is_symlink():
            continue
        if entry.is_file():
            yield entry


def plan_moves(
    config: dict[str, Any] | None = None,
    sources: list[Path] | None = None,
) -> list[MoveAction]:
    cfg = config or load_config()
    ext_map = extension_map(cfg)
    source_dirs = sources if sources is not None else enabled_source_dirs(cfg)
    planned: list[MoveAction] = []

    for source_dir in source_dirs:
        for path in iter_loose_files(source_dir, cfg):
            category = categorize(path, cfg, ext_map)
            if category is None:
                continue
            dest = destination_for(category, path, cfg)
            # Skip no-op moves into the same directory tree destination if already organized.
            if path.resolve() == dest.resolve():
                continue
            if path.parent.resolve() == dest.parent.resolve():
                continue
            planned.append(
                MoveAction(
                    source=str(path),
                    destination=str(dest),
                    category=category,
                    dry_run=True,
                )
            )
    return planned


def _write_log(result: OrganizeResult, dry_run: bool) -> Path:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    prefix = "dryrun" if dry_run else "run"
    log_path = LOG_DIR / f"{prefix}-{stamp}.json"
    payload = {
        "timestamp": stamp,
        "dry_run": dry_run,
        "moved": [asdict(m) for m in result.moved],
        "skipped": result.skipped,
        "errors": result.errors,
    }
    log_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return log_path


def organize(
    *,
    dry_run: bool = False,
    config: dict[str, Any] | None = None,
    sources: list[Path] | None = None,
) -> OrganizeResult:
    cfg = config or load_config()
    planned = plan_moves(cfg, sources)
    result = OrganizeResult()

    for action in planned:
        src = Path(action.source)
        dest = Path(action.destination)
        try:
            if dry_run:
                result.moved.append(
                    MoveAction(action.source, action.destination, action.category, True)
                )
                continue

            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src), str(dest))
            result.moved.append(
                MoveAction(action.source, action.destination, action.category, False)
            )
        except OSError as exc:
            result.errors.append(f"{src}: {exc}")

    result.log_path = str(_write_log(result, dry_run=dry_run))
    return result


def latest_run_log() -> Path | None:
    if not LOG_DIR.is_dir():
        return None
    runs = sorted(LOG_DIR.glob("run-*.json"), reverse=True)
    return runs[0] if runs else None


def undo_last_run(*, dry_run: bool = False) -> OrganizeResult:
    log_file = latest_run_log()
    result = OrganizeResult()
    if log_file is None:
        result.errors.append("No previous run log found to undo.")
        return result

    payload = json.loads(log_file.read_text(encoding="utf-8"))
    if payload.get("dry_run"):
        result.errors.append(f"Latest log is a dry-run ({log_file.name}); nothing to undo.")
        return result

    for item in reversed(payload.get("moved", [])):
        src = Path(item["destination"])
        dest = Path(item["source"])
        try:
            if not src.exists():
                result.skipped.append(str(src))
                continue
            if dry_run:
                result.moved.append(
                    MoveAction(str(src), str(dest), item.get("category", "undo"), True)
                )
                continue
            dest.parent.mkdir(parents=True, exist_ok=True)
            if dest.exists():
                result.errors.append(f"Cannot restore {src} → {dest}: destination exists")
                continue
            shutil.move(str(src), str(dest))
            result.moved.append(
                MoveAction(str(src), str(dest), item.get("category", "undo"), False)
            )
        except OSError as exc:
            result.errors.append(f"{src}: {exc}")

    # Mark the undone log so we don't undo twice accidentally.
    if not dry_run and result.moved and not result.errors:
        undone = log_file.with_name(log_file.name.replace("run-", "undone-", 1))
        log_file.rename(undone)
        result.log_path = str(undone)
    else:
        result.log_path = str(log_file)
    return result


def summarize_by_category(moves: list[MoveAction]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for move in moves:
        counts[move.category] = counts.get(move.category, 0) + 1
    return dict(sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])))


_SAFE_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")


def validate_project_name(name: str) -> bool:
    return bool(_SAFE_NAME.match(name))
