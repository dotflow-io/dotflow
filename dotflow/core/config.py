"""Config module"""

from typing import Optional

from dotflow.abc.storage import Storage
from dotflow.abc.notify import Notify

from dotflow.providers.storage_default import StorageDefault
from dotflow.providers.notify_default import NotifyDefault


class Config:
    """
    Import:
        You can import the **Config** class with:

            from dotflow import Config
            from dotflow.storage import StorageDefault
            from dotflow.notify import NotifyDefault

    Example:
        `class` dotflow.core.config.Config

            config = Config(
                storage=StorageFile(path=".output"),
                notify=NotifyDefault()
            )

    Args:
        storage (Optional[Storage]): Type of the storage.
        notify (Optional[Notify]): Type of the notify.

    Attributes:
        storage (Storage):
        notify (Notify):
    """

    def __init__(
            self,
            storage: Optional[Storage] = None,
            notify: Optional[Notify] = None
    ) -> None:
        self.storage = storage if storage else StorageDefault()
        self.notify = notify if notify else NotifyDefault()
