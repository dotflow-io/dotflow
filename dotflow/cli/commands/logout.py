"""Command logout module."""

from rich import print  # type: ignore

from dotflow.cli.command import Command
from dotflow.core.config_file import clear_cloud_config
from dotflow.settings import Settings as settings


class LogoutCommand(Command):
    def setup(self):
        if clear_cloud_config():
            print(settings.INFO_ALERT, "Signed out.")
        else:
            print(settings.WARNING_ALERT, "No saved credentials.")
