"""Tools"""

from pathlib import Path
from typing import Any
from json import loads, dumps, JSONDecodeError
from os import system


def write_file_system(
        path: str,
        content: str,
        mode: str = "w"
) -> None:
    """Write file system"""
    if mode == "a":
        system(f"echo '{content}' >> {path}")

    if mode == "w":
        system(f"echo '{content}' > {path}")


def write_file(
        path: str,
        content: Any,
        mode: str = "w",
        encoding: str = "utf-8"
) -> None:
    """Write file"""
    try:
        with open(file=path, mode=mode, encoding=encoding) as file:
            file.write(dumps(content))
    except TypeError:
        with open(file=path, mode=mode, encoding=encoding) as file:
            file.write(str(content))


def read_file(
        path: Path,
        encoding: str = "utf-8"
) -> Any | None:
    """Read file"""
    if path.exists():
        with open(file=path, mode="r", encoding=encoding) as file:
            try:
                return loads(file.read())
            except JSONDecodeError:
                return file.read()
    return None
