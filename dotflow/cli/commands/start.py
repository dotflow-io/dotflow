"""Command start module"""

from os import system

from dotflow import DotFlow, Config
from dotflow.providers import StorageDefault, StorageFile
from dotflow.core.types.execution import TypeExecution
from dotflow.cli.command import Command


class StartCommand(Command):

    def setup(self):
        workflow = self._new_workflow()

        workflow.task.add(
            step=self.params.step,
            callback=self.params.callback,
            initial_context=self.params.initial_context,
        )

        workflow.start(mode=self.params.mode)

        if self.params.mode == TypeExecution.BACKGROUND:
            system("/bin/bash")

    def _new_workflow(self):
        if not self.params.storage:
            return DotFlow()

        storage_classes = {
            "default": StorageDefault,
            "file": StorageFile
        }

        config = Config(
            storage=storage_classes.get(self.params.storage)(
                path=self.params.path,
            )
        )

        return DotFlow(config=config)
