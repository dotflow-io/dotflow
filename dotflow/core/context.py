"""Context module"""

from typing import Any
from datetime import datetime

from dotflow.core.abc.context import ABCContext


class Context(ABCContext):

    def __init__(self, storage: Any = None) -> None:
        self.datetime = datetime.now()
        self.storage = storage
