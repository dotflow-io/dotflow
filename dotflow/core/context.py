"""Context module"""

from datetime import datetime
from typing import Any
from dotflow.abc.context import ABCContext


class Context(ABCContext):

    def __init__(self, storage: Any = None) -> None:
        self.datetime = datetime.now()
        self.storage = storage
