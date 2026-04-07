"""Config module"""

from __future__ import annotations

from dotflow.abc.api import Api
from dotflow.abc.log import Log
from dotflow.abc.metrics import Metrics
from dotflow.abc.notify import Notify
from dotflow.abc.scheduler import Scheduler
from dotflow.abc.storage import Storage
from dotflow.abc.tracer import Tracer
from dotflow.core.exception import NotCallableObject
from dotflow.providers.api_default import ApiDefault
from dotflow.providers.log_default import LogDefault
from dotflow.providers.metrics_default import MetricsDefault
from dotflow.providers.notify_default import NotifyDefault
from dotflow.providers.scheduler_default import SchedulerDefault
from dotflow.providers.storage_default import StorageDefault
from dotflow.providers.tracer_default import TracerDefault


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
        tracer (Optional[Tracer]): Type of the tracer.
        metrics (Optional[Metrics]): Type of the metrics.

    Attributes:
        storage (Optional[Storage]):
        notify (Optional[Notify]):
        log (Optional[Log]):
        scheduler (Optional[Scheduler]):
        tracer (Optional[Tracer]):
        metrics (Optional[Metrics]):
    """

    _PROVIDERS = {
        "storage": Storage,
        "notify": Notify,
        "log": Log,
        "api": Api,
        "scheduler": Scheduler,
        "tracer": Tracer,
        "metrics": Metrics,
    }

    def __init__(
        self,
        storage: Storage | None = None,
        notify: Notify | None = None,
        log: Log | None = None,
        api: Api | None = None,
        scheduler: Scheduler | None = None,
        tracer: Tracer | None = None,
        metrics: Metrics | None = None,
    ) -> None:
        self.storage = storage if storage is not None else StorageDefault()
        self.notify = notify if notify is not None else NotifyDefault()
        self.log = log if log is not None else LogDefault()
        self.api = api if api is not None else ApiDefault()
        self.scheduler = (
            scheduler if scheduler is not None else SchedulerDefault()
        )
        self.tracer = tracer if tracer is not None else TracerDefault()
        self.metrics = metrics if metrics is not None else MetricsDefault()

        self._validate()

    def _validate(self) -> None:
        for name, abc in self._PROVIDERS.items():
            value = getattr(self, name)
            if value is not None and not isinstance(value, abc):
                raise NotCallableObject(name=name)
