"""Command init module"""

from pathlib import Path
from os import system

from dotflow.cli.command import Command
from dotflow.utils.print import print_info


class InitCommand(Command):

    GITIGNORE = Path(".gitignore")

    def setup(self):
        if self.GITIGNORE.exists():
            system("echo '\n\n# Dotflow\n.output' >> .gitignore")
            print_info(
                f"Installation complete! The ({self.GITIGNORE.resolve()}) file has been modified."
            )
