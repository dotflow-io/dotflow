"""Command start module"""

from os import system

from dotflow import Config, DotFlow
from dotflow.cli.command import Command
from dotflow.core.exception import InvalidWorkflowFactory
from dotflow.core.module import Module
from dotflow.core.types.execution import TypeExecution
from dotflow.providers import (
    StorageDefault,
    StorageFile,
    StorageGCS,
    StorageS3,
)


class StartCommand(Command):
    def setup(self):
        if getattr(self.params, "workflow", None):
            self._start_from_factory()
        else:
            self._start_from_step()

        if self.params.mode == TypeExecution.BACKGROUND:
            system("/bin/bash")

    def _start_from_step(self):
        workflow = self._new_workflow()

        workflow.task.add(
            step=self.params.step,
            callback=self.params.callback,
            initial_context=self.params.initial_context,
        )

        workflow.start(mode=self.params.mode)

    def _start_from_factory(self):
        factory = Module(self.params.workflow)

        if not callable(factory):
            raise InvalidWorkflowFactory(factory=self.params.workflow)

        result = factory()

        if not isinstance(result, DotFlow):
            raise InvalidWorkflowFactory(factory=self.params.workflow)

        result.start(mode=self.params.mode)

    def _new_workflow(self):
        if not self.params.storage:
            return DotFlow()

        storage_classes = {
            "default": StorageDefault,
            "file": StorageFile,
            "s3": StorageS3,
            "gcs": StorageGCS,
        }

        storage_cls = storage_classes.get(self.params.storage)
        storage_with_path = {StorageDefault, StorageFile}

        if storage_cls in storage_with_path:
            storage = storage_cls(path=self.params.path)
        else:
            storage = storage_cls()

        config = Config(storage=storage)

        return DotFlow(config=config)
