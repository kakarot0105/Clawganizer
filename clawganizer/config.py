"""Configuration loading and defaults."""

from __future__ import annotations

import json
import os
from copy import deepcopy
from pathlib import Path
from typing import Any

PACKAGE_DIR = Path(__file__).resolve().parent
DEFAULT_CONFIG_PATH = PACKAGE_DIR / "default_config.json"
USER_CONFIG_DIR = Path(os.environ.get("CLAWGANIZER_CONFIG_DIR", Path.home() / ".config" / "clawganizer"))
USER_CONFIG_PATH = USER_CONFIG_DIR / "config.json"
LOG_DIR = Path(os.environ.get("CLAWGANIZER_LOG_DIR", Path.home() / ".local" / "share" / "clawganizer" / "logs"))


def load_default_config() -> dict[str, Any]:
    with DEFAULT_CONFIG_PATH.open(encoding="utf-8") as fh:
        return json.load(fh)


def deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    result = deepcopy(base)
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = deepcopy(value)
    return result


def load_config(path: Path | None = None) -> dict[str, Any]:
    config = load_default_config()
    explicit = path is not None
    config_path = path or USER_CONFIG_PATH
    # Explicit --config must load (including process-substitution /dev/fd paths
    # that may not report as a regular file via Path.is_file()).
    if explicit or config_path.is_file():
        try:
            with config_path.open(encoding="utf-8") as fh:
                user = json.load(fh)
        except OSError:
            if explicit:
                raise
        else:
            config = deep_merge(config, user)
    return config


def ensure_user_config() -> Path:
    USER_CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    if not USER_CONFIG_PATH.exists():
        USER_CONFIG_PATH.write_text(
            json.dumps(load_default_config(), indent=2) + "\n",
            encoding="utf-8",
        )
    return USER_CONFIG_PATH


def expand_path(value: str) -> Path:
    return Path(os.path.expanduser(os.path.expandvars(value))).resolve()
