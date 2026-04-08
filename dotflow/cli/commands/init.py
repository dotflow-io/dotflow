"""Command init module"""

from cookiecutter.main import cookiecutter
from rich import print  # type: ignore

from dotflow.cli.command import Command
from dotflow.settings import Settings as settings

TEMPLATE_REPO = "https://github.com/dotflow-io/template"


class InitCommand(Command):
    def setup(self):
        cookiecutter(TEMPLATE_REPO)

        print(
            settings.INFO_ALERT,
            "Project created!",
        )
