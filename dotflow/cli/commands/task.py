"""Command task module"""

from dotflow import DotFlow
from dotflow.cli.command import Command
from dotflow.cli.validators import TaskValidator


class TaskCommand(Command):

    def add(self):
        attr = TaskValidator(**self.params.__dict__).json()
        print(attr)

    def start(self):
        workflow = DotFlow()
        workflow.task.add(
            step=self.params.step,
            callback=self.params.callback
        )
        workflow.start()
