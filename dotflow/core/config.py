"""Config module"""

from __future__ import annotations

from dotflow.abc.api import Api
from dotflow.abc.log import Log
from dotflow.abc.notify import Notify
from dotflow.abc.scheduler import Scheduler
from dotflow.abc.storage import Storage
from dotflow.core.exception import NotCallableObject
from dotflow.providers.api_default import ApiDefault
from dotflow.providers.log_default import LogDefault
from dotflow.providers.notify_default import NotifyDefault
from dotflow.providers.scheduler_default import SchedulerDefault
from dotflow.providers.storage_default import StorageDefault


class Config:
    """
    Import:
        You can import the **Config** class with:

            from dotflow import Config

            from dotflow.providers import (
                StorageDefault,
                NotifyDefault,
                LogDefault,
                SchedulerDefault,
            )

    Example:
        `class` dotflow.core.config.Config

            config = Config(
                storage=StorageFile(path=".output"),
                notify=NotifyDefault(),
                log=LogDefault()
            )

    Args:
        storage (Optional[Storage]): Type of the storage.
        notify (Optional[Notify]): Type of the notify.
        log (Optional[Log]): Type of the log.
        scheduler (Optional[Scheduler]): Type of the scheduler.

    Attributes:
        storage (Optional[Storage]):
        notify (Optional[Notify]):
        log (Optional[Log]):
        scheduler (Optional[Scheduler]):
    """

    _PROVIDERS = {
        "storage": Storage,
        "notify": Notify,
        "log": Log,
        "api": Api,
        "scheduler": Scheduler,
    }

    def __init__(
        self,
        storage: Storage | None = StorageDefault(),
        notify: Notify | None = NotifyDefault(),
        log: Log | None = LogDefault(),
        api: Api | None = ApiDefault(),
        scheduler: Scheduler | None = SchedulerDefault(),
    ) -> None:
        self.storage = storage
        self.notify = notify
        self.log = log
        self.api = api
        self.scheduler = scheduler

        self._validate()

    def _validate(self) -> None:
        for name, abc in self._PROVIDERS.items():
            value = getattr(self, name)
            if value is not None and not isinstance(value, abc):
                raise NotCallableObject(name=name)
