"""Command start module"""

import os
from os import system

from dotflow import Config, DotFlow
from dotflow.cli.command import Command
from dotflow.core.types.execution import TypeExecution
from dotflow.providers import (
    ServerAPI,
    ServerDefault,
    StorageDefault,
    StorageFile,
    StorageGCS,
    StorageS3,
)


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
        config = self._build_config()
        workflow_id = os.getenv("WORKFLOW_ID")

        if config is None:
            return DotFlow(workflow_id=workflow_id)
        return DotFlow(config=config, workflow_id=workflow_id)

    def _build_config(self):
        storage = self._build_storage()
        server = self._build_server()

        if storage is None and server is None:
            return None

        return Config(
            storage=storage or StorageDefault(),
            server=server or ServerDefault(),
        )

    def _build_server(self):
        base_url = os.getenv("SERVER_BASE_URL")
        user_token = os.getenv("SERVER_USER_TOKEN")

        if not base_url or not user_token:
            return None
        return ServerAPI(base_url=base_url, user_token=user_token)

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
