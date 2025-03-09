"""Command init module"""

from os import system

from rich import print  # type: ignore

from dotflow.settings import Settings as settings
from dotflow.cli.command import Command


class InitCommand(Command):

    def setup(self):
        if settings.GITIGNORE.exists():
            system("echo '\n\n# Dotflow\n.output' >> .gitignore")
            print(
                settings.INFO_ALERT,
                f"Installation complete! The ({settings.GITIGNORE.resolve()}) file has been modified."
            )
