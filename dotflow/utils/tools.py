"""Tools"""

import socket
from json import JSONDecodeError, dumps, loads
from pathlib import Path
from typing import Any


def hostname() -> str:
    """Return the local hostname, with a ``local`` fallback."""
    try:
        return socket.gethostname() or "local"
    except OSError:
        return "local"


def write_file(
    path: str, content: Any, mode: str = "w", encoding: str = "utf-8"
) -> None:
    """Write file"""
    try:
        with open(file=path, mode=mode, encoding=encoding) as file:
            file.write(dumps(content))
    except TypeError:
        with open(file=path, mode=mode, encoding=encoding) as file:
            file.write(str(content))


def read_file(path: Path, encoding: str = "utf-8") -> Any:
    """Read file"""
    if path.exists():
        with open(file=path, encoding=encoding) as file:
            content = file.read()
        try:
            return loads(content)
        except JSONDecodeError:
            return content
    return None
