from datetime import datetime
from typing import Any


class Context:

    def __init__(self, storage: Any = None) -> None:
        self.datetime = datetime.now()
        self.storage = storage
