"""Config module"""

from typing import List, Optional

from dotflow.abc.storage import Storage
from dotflow.abc.notify import Notify
from dotflow.abc.logs import Logs

from dotflow.plugins.logs import LogsHandler
from dotflow.providers.storage_default import StorageDefault
from dotflow.providers.notify_default import NotifyDefault
from dotflow.utils.tools import start_and_validate_instance


class ConfigInstance:

    def __init__(self, *_args, **_kwargs):
        self._storage: Storage = None
        self._notify: Notify = None
        self._logs: List[Logs] = None


class Config(ConfigInstance):
    """
    Import:
        You can import the **Config** class with:

            from dotflow import Config

            from dotflow.providers import (
                StorageDefault,
                NotifyDefault,
                LogsHandler
            )

    Example:
        `class` dotflow.core.config.Config

            config = Config(
                storage=StorageFile(path=".output"),
                notify=NotifyDefault(),
                logs=LogsHandler
            )

    Args:
        storage (Optional[Storage]): Type of the Storage.
        notify (Optional[Notify]): Type of the Notify.
        logs (Optional[List[Logs]]): Type of the Logs.

    Attributes:
        storage (Optional[Storage]):
        notify (Optional[Notify]):
        logs (Optional[List[Logs]]):
    """

    def __init__(
        self,
        storage: Optional[Storage] = StorageDefault,
        notify: Optional[Notify] = NotifyDefault,
        logs: Optional[List[Logs]] = LogsHandler
    ):
        super().__init__()
        self.storage = storage
        self.notify = notify
        self.logs = logs

    @property
    def storage(self):
        return self._storage

    @storage.setter
    def storage(self, value):
        if not value:
            value = StorageDefault()

        self._storage = start_and_validate_instance(value, Storage)

    @property
    def notify(self):
        return self._notify

    @notify.setter
    def notify(self, value):
        if not value:
            value = NotifyDefault()

        self._notify = start_and_validate_instance(value, Notify)

    @property
    def logs(self):
        return self._logs

    @logs.setter
    def logs(self, value):
        if not value:
            value = [LogsHandler]

        if isinstance(value, list):
            if isinstance(value, list):
                for index, current_log in enumerate(value):
                    value[index] = start_and_validate_instance(current_log, Logs)
        else:
            value = [start_and_validate_instance(value, Logs)]

        self._logs = value
