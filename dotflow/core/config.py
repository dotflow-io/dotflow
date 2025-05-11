"""Config module"""

from typing import Optional

from dotflow.abc.log import Log
from dotflow.abc.storage import Storage
from dotflow.abc.notify import Notify

from dotflow.providers.log_default import LogDefault
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
                LogDefault
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
        log (Optional[Log]): Type of the notify.

    Attributes:
        storage (Optional[Storage]):
        notify (Optional[Notify]):
        log (Optional[Log]):
    """

    def __init__(
        self,
        storage: Optional[Storage] = StorageDefault(),
        notify: Optional[Notify] = NotifyDefault(),
        log: Optional[Log] = LogDefault(),
    ) -> None:
        self.storage = storage
        self.notify = notify
        self.log = log
