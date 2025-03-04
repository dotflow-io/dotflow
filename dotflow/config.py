"""Config module"""

import logging

from os import makedirs
from shutil import copy


class Config:

    PATH = ".storage"
    LOG_FILE_NAME = "dotflow.log"

    PATHS = {
        "workflows": "{}/workflows",
    }

    def __init__(
            self,
            path: str = PATH,
            output: bool = False
    ) -> None:
        self.logger_name = "dotflow"
        self.logger_path = f"{path}/{self.LOG_FILE_NAME}"
        self.output = output

        for folder_path in self.PATHS:
            try:
                makedirs(
                    name=self.PATHS[folder_path].format(path),
                    exist_ok=True
                )
            except Exception as err:
                logging.error(err)

    def _log_transfer(self):
        src = f"{self.PATH}/{self.LOG_FILE_NAME}"

        if src != self.logger_path:
            try:
                copy(src=src, dst=self.logger_path)
            except Exception as err:
                logging.error(err)
