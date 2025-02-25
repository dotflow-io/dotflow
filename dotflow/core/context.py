"""Context module"""

from typing import Any
from datetime import datetime


class Context:

    def __init__(self, storage: Any = None) -> None:
        self.time = datetime.now()
        self.storage = storage

        if isinstance(storage, Context):
            self.time = storage.time
            self.storage = storage.storage
