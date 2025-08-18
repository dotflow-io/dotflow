"""Config module"""

from typing import Optional

from dotflow.abc.logs import Logs
from dotflow.abc.storage import Storage
from dotflow.abc.notify import Notify

from dotflow.plugins.logs import LogsHandler
from dotflow.providers.storage_default import StorageDefault
from dotflow.providers.notify_default import NotifyDefault


class Config:
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
                log=LogsHandler()
            )

    Args:
        storage (Optional[Storage]): Type of the storage.
        notify (Optional[Notify]): Type of the notify.
        log (Optional[Logs]): Type of the notify.

    Attributes:
        storage (Optional[Storage]):
        notify (Optional[Notify]):
        log (Optional[Logs]):
    """

    def __init__(
        self,
        storage: Optional[Storage] = StorageDefault(),
        notify: Optional[Notify] = NotifyDefault(),
        log: Optional[Logs] = LogsHandler(),
    ) -> None:
        self.storage = storage
        self.notify = notify
        self.log = log
