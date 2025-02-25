"""DotFlow"""

from functools import partial

from dotflow.core.controller import Controller
from dotflow.core.task import TaskBuilder


class DotFlow:

    def __init__(self) -> None:
        self.task = TaskBuilder()
        self.start = partial(Controller, self.task.queu)
