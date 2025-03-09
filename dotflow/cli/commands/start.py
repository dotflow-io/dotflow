"""Command start module"""

from os import system

from dotflow import DotFlow, Config
from dotflow.core.types.execution import TypeExecution
from dotflow.cli.command import Command


class StartCommand(Command):

    def setup(self):
        workflow = DotFlow(
            config=Config(
                path=self.params.path,
                output=self.params.output_context
            )
        )

        workflow.task.add(
            step=self.params.step,
            callback=self.params.callback,
            initial_context=self.params.initial_context
        )

        workflow.start(
            mode=self.params.mode
        )

        if self.params.mode == TypeExecution.BACKGROUND:
            system("/bin/bash")
