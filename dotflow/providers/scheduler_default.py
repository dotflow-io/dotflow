"""Scheduler Default"""

from collections.abc import Callable

from dotflow.abc.scheduler import Scheduler


class SchedulerDefault(Scheduler):
    def start(self, workflow: Callable, **kwargs) -> None:
        pass

    def stop(self) -> None:
        pass
