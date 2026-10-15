"""OpenClaw-style project workspace helpers (optional legacy mode)."""

from __future__ import annotations

import os
from pathlib import Path


def workspace_root() -> Path:
    return Path(os.environ.get("WORKSPACE", Path.home() / ".openclaw")).expanduser()


def projects_dir() -> Path:
    path = workspace_root() / "projects"
    path.mkdir(parents=True, exist_ok=True)
    (path / "active").mkdir(exist_ok=True)
    (path / "archived").mkdir(exist_ok=True)
    return path


def list_projects() -> tuple[list[str], list[str]]:
    root = projects_dir()
    active = sorted(p.name for p in (root / "active").iterdir() if p.is_dir())
    archived = sorted(p.name for p in (root / "archived").iterdir() if p.is_dir())
    return active, archived


def create_project(name: str) -> Path:
    path = projects_dir() / "active" / name
    path.mkdir(parents=True, exist_ok=False)
    return path


def archive_project(name: str) -> Path:
    active = projects_dir() / "active" / name
    archived = projects_dir() / "archived" / name
    if not active.is_dir():
        raise FileNotFoundError(f"Project not found: {name}")
    if archived.exists():
        raise FileExistsError(f"Archived project already exists: {name}")
    active.rename(archived)
    return archived


def organize_workspace() -> Path:
    root = workspace_root()
    projects_dir()
    (root / "venvs").mkdir(parents=True, exist_ok=True)
    for sub in ("memory", "skills", "notes"):
        (root / "workspace" / sub).mkdir(parents=True, exist_ok=True)
    return root


def workspace_status() -> dict[str, object]:
    active, archived = list_projects()
    return {
        "workspace": str(workspace_root()),
        "active": len(active),
        "archived": len(archived),
        "active_names": active,
        "archived_names": archived,
    }
