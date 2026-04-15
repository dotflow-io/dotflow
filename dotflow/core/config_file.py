"""Persistent CLI config stored at ``~/.dotflow/config.toml``.

Kept minimal on purpose — the only shape we read/write is::

    [cloud]
    base_url = "https://host.dotflow.io/api/v1"
    token = "dtf_sk_..."
"""

from __future__ import annotations

import os
import re
from pathlib import Path

CONFIG_DIR_NAME = ".dotflow"
CONFIG_FILE_NAME = "config.toml"
CLOUD_SECTION = "cloud"


def config_path() -> Path:
    """Return the absolute path of the CLI config file."""
    return Path.home() / CONFIG_DIR_NAME / CONFIG_FILE_NAME


def load_cloud_config() -> dict[str, str]:
    """Read ``[cloud]`` from the config file. Returns {} when absent."""
    path = config_path()

    if not path.exists():
        return {}

    try:
        return _parse_cloud_section(path.read_text(encoding="utf-8"))
    except OSError:
        return {}


def save_cloud_config(token: str, base_url: str) -> Path:
    """Persist ``[cloud]`` with the given token/base_url. Returns the file path."""
    path = config_path()
    path.parent.mkdir(parents=True, exist_ok=True)

    content = (
        f"[{CLOUD_SECTION}]\n"
        f'base_url = "{_escape(base_url)}"\n'
        f'token = "{_escape(token)}"\n'
    )

    fd = os.open(
        str(path),
        os.O_WRONLY | os.O_CREAT | os.O_TRUNC,
        0o600,
    )
    try:
        os.fchmod(fd, 0o600)
    except OSError:
        pass
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


_SECTION_RE = re.compile(r"^\s*\[(?P<name>[^\]]+)\]\s*$")
_KEY_VALUE_RE = re.compile(
    r'^\s*(?P<key>[A-Za-z_][A-Za-z0-9_-]*)\s*=\s*"(?P<value>(?:[^"\\]|\\.)*)"\s*$'
)


def _parse_cloud_section(content: str) -> dict[str, str]:
    """Parse just ``[cloud]`` key/string-value pairs from a TOML-ish file."""
    current_section: str | None = None
    result: dict[str, str] = {}

    for line in content.splitlines():
        stripped = line.strip()

        if not stripped or stripped.startswith("#"):
            continue

        section = _SECTION_RE.match(line)
        if section:
            current_section = section.group("name").strip()
            continue

        if current_section != CLOUD_SECTION:
            continue

        key_value = _KEY_VALUE_RE.match(line)
        if not key_value:
            continue

        result[key_value.group("key")] = _unescape(key_value.group("value"))

    return result


def _escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def _unescape(value: str) -> str:
    return value.replace('\\"', '"').replace("\\\\", "\\")
