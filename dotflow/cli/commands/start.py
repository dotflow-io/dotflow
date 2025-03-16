"""Command start module"""

from os import system

from dotflow import DotFlow, Config
from dotflow.providers import StorageDefault, StorageFile
from dotflow.core.types.execution import TypeExecution
from dotflow.cli.command import Command


class StartCommand(Command):

    def setup(self):
        workflow = DotFlow()

        if self.params.storage:
            storage = {"default": StorageDefault, "file": StorageFile}

            config = Config(
                storage=storage.get(self.params.storage)(
                    path=self.params.path,
                )
            )
            workflow = DotFlow(config=config)

        workflow.task.add(
            step=self.params.step,
            callback=self.params.callback,
            initial_context=self.params.initial_context,
        )

        workflow.start(mode=self.params.mode)

        if self.params.mode == TypeExecution.BACKGROUND:
            system("/bin/bash")
