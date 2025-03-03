"""Command task module"""

from dotflow.cli.command import Command
from dotflow.cli.validators import TaskValidator


class TaskCommand(Command):

    def add(self):
        attr = TaskValidator(params=self.params).attr
        print(attr)
