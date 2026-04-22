"""Persistent CLI config stored at ``~/.dotflow/config.json``."""

from __future__ import annotations

import contextlib
import json
import os
from pathlib import Path

CONFIG_DIR_NAME = ".dotflow"
CONFIG_FILE_NAME = "config.json"
CLOUD_SECTION = "cloud"


def config_path() -> Path:
    """Return the absolute path of the CLI config file."""
    return Path.home() / CONFIG_DIR_NAME / CONFIG_FILE_NAME


def load_cloud_config() -> dict[str, str]:
    """Read the ``cloud`` section from the config file. ``{}`` when absent."""
    path = config_path()

    if not path.exists():
        return {}

    try:
        raw = path.read_text(encoding="utf-8")
    except OSError:
        return {}

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return {}

    section = data.get(CLOUD_SECTION) if isinstance(data, dict) else None
    if not isinstance(section, dict):
        return {}

    return {
        key: str(value)
        for key, value in section.items()
        if isinstance(value, str)
    }


def save_cloud_config(token: str, base_url: str) -> Path:
    """Persist ``cloud`` with the given token/base_url. Returns the file path."""
    path = config_path()
    path.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        CLOUD_SECTION: {
            "base_url": base_url,
            "token": token,
        }
    }
    content = json.dumps(payload, indent=2) + "\n"

    fd = os.open(
        str(path),
        os.O_WRONLY | os.O_CREAT | os.O_TRUNC,
        0o600,
    )
    with contextlib.suppress(OSError):
        os.fchmod(fd, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        fh.write(content)

    return path


def clear_cloud_config() -> bool:
    """Remove the config file. Returns True when something was deleted."""
    path = config_path()

    if not path.exists():
        return False

    try:
        path.unlink()
        return True
    except OSError:
        return False


def resolve(key: str, env_var: str) -> str | None:
    """Resolve a setting with env > file precedence. ``None`` when absent."""
    env_value = os.environ.get(env_var)

    if env_value:
        return env_value

    return load_cloud_config().get(key) or None
