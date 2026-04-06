"""Scheduler Cron"""

from __future__ import annotations

import signal
import threading
from collections.abc import Callable
from datetime import datetime
from time import sleep

from dotflow.abc.scheduler import Scheduler
from dotflow.core.exception import ModuleNotFound
from dotflow.core.types.overlap import TypeOverlap


class SchedulerCron(Scheduler):
    """
    Import:
        You can import the **SchedulerCron** class with:

            from dotflow.providers import SchedulerCron

    Example:
        `class` dotflow.providers.scheduler_cron.SchedulerCron

            from dotflow import DotFlow, Config
            from dotflow.providers import SchedulerCron

            config = Config(
                scheduler=SchedulerCron(
                    cron="*/5 * * * *",
                    overlap="skip",
                )
            )

            workflow = DotFlow(config=config)
            workflow.task.add(step=extract)
            workflow.task.add(step=load)
            workflow.schedule()

    Args:
        cron (str): A cron expression defining the schedule
            (e.g. ``"*/5 * * * *"`` for every 5 minutes).

        overlap (str): Strategy when a previous run is still active.
            One of ``"skip"``, ``"queue"``, or ``"parallel"``.
            Defaults to ``"skip"``.

    Attributes:
        cron (str): The cron expression.

        overlap (str): The overlap strategy.

        running (bool): Whether the scheduler loop is active.
    """

    def __init__(
        self,
        cron: str,
        overlap: str = TypeOverlap.SKIP,
    ) -> None:
        try:
            from croniter import croniter  # noqa: F401
        except ImportError:
            raise ModuleNotFound(
                module="croniter", library="dotflow[scheduler]"
            )

        self.cron = cron
        self.overlap = overlap
        self.running = False
        self._executing = False
        self._lock = threading.Lock()
        self._queue_count = 0

    def start(self, workflow: Callable, **kwargs) -> None:
        """Start the scheduler loop. Blocks the main thread.

        Args:
            workflow (Callable): The workflow start function to execute
                on each scheduled run.
            **kwargs: Additional keyword arguments passed to the workflow
                execution (e.g. mode, resume).
        """
        from croniter import croniter

        self.running = True
        self._register_signals()

        cron_iter = croniter(self.cron, datetime.now())

        while self.running:
            next_run = cron_iter.get_next(datetime)
            wait = (next_run - datetime.now()).total_seconds()

            while wait > 0 and self.running:
                step = min(wait, 1.0)
                sleep(step)
                wait -= step

            if not self.running:
                break

            self._dispatch(workflow=workflow, **kwargs)

    def stop(self) -> None:
        """Stop the scheduler loop gracefully."""
        self.running = False

    def _dispatch(self, workflow: Callable, **kwargs) -> None:
        if self.overlap == TypeOverlap.SKIP:
            self._dispatch_skip(workflow=workflow, **kwargs)
        elif self.overlap == TypeOverlap.QUEUE:
            self._dispatch_queue(workflow=workflow, **kwargs)
        elif self.overlap == TypeOverlap.PARALLEL:
            self._dispatch_parallel(workflow=workflow, **kwargs)

    def _dispatch_skip(self, workflow: Callable, **kwargs) -> None:
        with self._lock:
            if self._executing:
                return
            self._executing = True

        thread = threading.Thread(
            target=self._execute_and_reset,
            args=(workflow,),
            kwargs=kwargs,
        )
        thread.start()

    def _dispatch_queue(self, workflow: Callable, **kwargs) -> None:
        with self._lock:
            if self._executing:
                self._queue_count += 1
                return
            self._executing = True

        thread = threading.Thread(
            target=self._execute_queued,
            args=(workflow,),
            kwargs=kwargs,
        )
        thread.start()

    def _dispatch_parallel(self, workflow: Callable, **kwargs) -> None:
        thread = threading.Thread(target=workflow, kwargs=kwargs)
        thread.start()

    def _execute_and_reset(self, workflow: Callable, **kwargs) -> None:
        try:
            workflow(**kwargs)
        finally:
            with self._lock:
                self._executing = False

    def _execute_queued(self, workflow: Callable, **kwargs) -> None:
        try:
            workflow(**kwargs)
        finally:
            with self._lock:
                if self._queue_count > 0:
                    self._queue_count -= 1
                    thread = threading.Thread(
                        target=self._execute_queued,
                        args=(workflow,),
                        kwargs=kwargs,
                    )
                    thread.start()
                else:
                    self._executing = False

    def _register_signals(self) -> None:
        signal.signal(signal.SIGINT, self._handle_signal)
        signal.signal(signal.SIGTERM, self._handle_signal)

    def _handle_signal(self, signum, frame) -> None:
        self.stop()
