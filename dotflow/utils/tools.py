"""Tools"""

import json
import logging

from os import makedirs, system
from shutil import copy


def make_dir(path: str, show_log: bool = False):
    try:
        makedirs(name=path, exist_ok=True)
    except Exception as err:
        if show_log:
            logging.error(err)


def copy_file(
        source: str,
        destination: str,
        show_log: bool = False
) -> None:
    try:
        copy(src=source, dst=destination)
    except Exception as err:
        if show_log:
            logging.error(err)


def write_file(
        path: str,
        content: str,
        mode: str = "w"
) -> None:
    if isinstance(content, dict) or isinstance(content, list):
        content = json.dumps(content)

    try:
        with open(file=path, mode=mode, encoding="utf-8") as file:
            file.write(content)
    except Exception:
        system(f"echo '{content}' > {path}")


def read_file(path: str) -> str:
    with open(file=path) as file:
        return file.read()
