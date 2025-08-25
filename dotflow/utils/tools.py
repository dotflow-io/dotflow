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
    """Write file system
    """
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
    """Write file
    """
    try:
        with open(file=path, mode=mode, encoding=encoding) as file:
            file.write(dumps(content))
    except TypeError:
        with open(file=path, mode=mode, encoding=encoding) as file:
            file.write(str(content))


def read_file(
    path: Path,
    encoding: str = "utf-8"
) -> Any:
    """Read file
    """
    if path.exists():
        with open(file=path, mode="r", encoding=encoding) as file:
            try:
                return loads(file.read())
            except JSONDecodeError:
                return file.read()
    return None


def start_and_validate_instance(current_class, instance):
    """
    This function starts a class if it is not instantiated and also
    performs validation that the class instance matches what is expected.
    """
    if callable(current_class):
        current_class = current_class()

    if not isinstance(current_class, instance):
        raise ValueError(
            f"Not a valid {current_class.__name__} instance class."
        )

    return current_class


def _type(value: str) -> Any:
    try:
        return eval(str(value).capitalize())
    except Exception:
        pass

    return value
