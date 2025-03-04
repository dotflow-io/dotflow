"""Command init module"""

from os import system, path

from dotflow.cli.command import Command


class InitCommand(Command):

    def __init__(self, **kwargs):
        self.params = kwargs.get("arguments")
        self.init()

    def init(self):
        if path.isfile(".gitignore"):
            system("echo '\n\n# Dotflow\n.output' >> .gitignore")
