"""Tools"""

import logging

from os import makedirs
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
