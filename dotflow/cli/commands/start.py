"""Command start module"""

from os import system

from dotflow import Config, DotFlow
from dotflow.cli.command import Command
from dotflow.core.exception import InvalidWorkflowFactory, WorkflowFlagConflict
from dotflow.core.module import Module
from dotflow.core.types.execution import TypeExecution
from dotflow.providers import (
    StorageDefault,
    StorageFile,
    StorageGCS,
    StorageS3,
)
from dotflow.utils.basic_functions import basic_callback


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
        step_only_flags = {
            "--callback": self.params.callback is not basic_callback,
            "--initial-context": self.params.initial_context is not None,
        }
        for flag, provided in step_only_flags.items():
            if provided:
                raise WorkflowFlagConflict(flag=flag)

        factory = Module(self.params.workflow)

        if not callable(factory):
            raise InvalidWorkflowFactory(factory=self.params.workflow)

        result = factory()

        if not isinstance(result, DotFlow):
            raise InvalidWorkflowFactory(factory=self.params.workflow)

        result.start(mode=self.params.mode)

    def _new_workflow(self):
        storage = self._build_storage()
        if storage is None:
            return DotFlow()
        return DotFlow(config=Config(storage=storage))

    def _build_storage(self):
        if not self.params.storage:
            return None

        storage_classes = {
            "default": StorageDefault,
            "file": StorageFile,
            "s3": StorageS3,
            "gcs": StorageGCS,
        }

        storage_cls = storage_classes.get(self.params.storage)
        storage_with_path = {StorageDefault, StorageFile}

        if storage_cls in storage_with_path:
            return storage_cls(path=self.params.path)
        return storage_cls()
