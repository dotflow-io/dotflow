"""Command schedule module"""

from dotflow import Config, DotFlow
from dotflow.cli.command import Command
from dotflow.providers import (
    SchedulerCron,
    StorageDefault,
    StorageFile,
    StorageGCS,
    StorageS3,
)


class ScheduleCommand(Command):
    def setup(self):
        workflow = self._new_workflow()

        workflow.task.add(
            step=self.params.step,
            callback=self.params.callback,
            initial_context=self.params.initial_context,
        )

        workflow.schedule(
            mode=self.params.mode,
            resume=self.params.resume,
        )

    def _new_workflow(self):
        scheduler = SchedulerCron(
            cron=self.params.cron,
            overlap=self.params.overlap,
        )

        if not self.params.storage:
            return DotFlow(config=Config(scheduler=scheduler))

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

        config = Config(
            storage=storage,
            scheduler=scheduler,
        )

        return DotFlow(config=config)
