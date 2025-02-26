"""Context module"""

from typing import Any
from datetime import datetime


class Context:

    def __init__(self, storage: Any = None) -> None:
        self.time = datetime.now()

        if isinstance(storage, Context):
            self.storage = storage.storage
        else:
            self.storage = storage
