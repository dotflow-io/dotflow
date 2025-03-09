"""Command log module"""

from rich import print  # type: ignore

from dotflow.utils import read_file
from dotflow.settings import Settings as settings
from dotflow.cli.command import Command


class LogCommand(Command):

    def setup(self):
        if settings.LOG_PATH.exists():
            print(read_file(path=settings.LOG_PATH))

            print(
                settings.INFO_ALERT,
                f"To access all logs, open the file ({settings.LOG_PATH.resolve()})."
            )
        else:
            print(settings.WARNING_ALERT, "Log file not found.")
