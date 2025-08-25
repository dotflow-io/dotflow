"""Command start module"""

from os import system

from dotflow import DotFlow
from dotflow.core.types.execution import ExecutionModeType
from dotflow.cli.command import Command


class StartCommand(Command):

    def setup(self):
        workflow = self._new_workflow()

        workflow.add(
            step=self.params.step,
            callback=self.params.callback,
            initial_context=self.params.initial_context,
        )

        workflow.start(mode=self.params.mode)

        if self.params.mode == ExecutionModeType.BACKGROUND:
            system("/bin/bash")

    def _new_workflow(self):
        return DotFlow()
