"""Action module"""

from time import sleep

from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Dict
from types import FunctionType

from dotflow.core.exception import ExecutionWithClassError
from dotflow.core.context import Context


def is_execution_with_class_internal_error(error: Exception) -> bool:
    message = str(error)
    patterns = [
        "initial_context",
        "previous_context",
        "missing 1 required positional argument: 'self'",
    ]
    return any(pattern in message for pattern in patterns)


class Action(object):
    """
    Import:
        You can import the **action** decorator directly from dotflow:

            from dotflow import action

    Example:
        `class` dotflow.core.action.Action

        Standard

            @action
            def my_task():
                print("task")

        With Retry

            @action(retry=5)
            def my_task():
                print("task")


        With Timeout

            @action(timeout=60)
            def my_task():
                print("task")

        With Retry delay

            @action(retry=5, retry_delay=5)
            def my_task():
                print("task")

        With Backoff

            @action(retry=5, backoff=True)
            def my_task():
                print("task")

    Args:
        func (Callable):

        task (Callable):

        retry (int): Number of task retries on on_failure.

        timeout (int): Execution timeout for a task. Duration (in seconds)

        retry_delay (int): Retry delay on task on_failure. Duration (in seconds)

        backoff (int): Exponential backoff

    """

    def __init__(
        self,
        func: Callable = None,
        task: Callable = None,
        retry: int = 1,
        timeout: int = 0,
        retry_delay: int = 1,
        backoff: bool = False,
    ) -> None:
        self.func = func
        self.task = task
        self.retry = retry
        self.timeout = timeout
        self.retry_delay = retry_delay
        self.backoff = backoff
        self.params = []

    def __call__(self, *args, **kwargs):
        # With parameters
        if self.func:
            self._set_params()

            task = self._get_task(kwargs=kwargs)
            contexts = self._get_context(kwargs=kwargs)

            if contexts:
                return Context(
                    storage=self._run_action(*args, **contexts),
                    task_id=task.task_id,
                    workflow_id=task.workflow_id,
                )

            return Context(
                storage=self._run_action(*args),
                task_id=task.task_id,
                workflow_id=task.workflow_id,
            )

        # No parameters
        def action(*_args, **_kwargs):
            self.func = args[0]
            self._set_params()

            task = self._get_task(kwargs=_kwargs)
            contexts = self._get_context(kwargs=_kwargs)

            if contexts:
                return Context(
                    storage=self._run_action(*_args, **contexts),
                    task_id=task.task_id,
                    workflow_id=task.workflow_id,
                )

            return Context(
                storage=self._run_action(*_args),
                task_id=task.task_id,
                workflow_id=task.workflow_id,
            )

        return action

    def _run_action(self, *args, **kwargs):
        for attempt in range(1, self.retry + 1):
            try:
                if self.timeout:
                    with ThreadPoolExecutor(max_workers=1) as executor:
                        future = executor.submit(self.func, *args, **kwargs)
                        return future.result(timeout=self.timeout)

                return self.func(*args, **kwargs)

            except Exception as error:
                last_exception = error

                if is_execution_with_class_internal_error(error=last_exception):
                    raise ExecutionWithClassError()

                if attempt == self.retry:
                    raise last_exception

                sleep(self.retry_delay)
                if self.backoff:
                    self.retry_delay *= 2

    def _set_params(self):
        if isinstance(self.func, FunctionType):
            self.params = [param for param in self.func.__code__.co_varnames]

        if type(self.func) is type:
            if hasattr(self.func, "__init__"):
                if hasattr(self.func.__init__, "__code__"):
                    self.params = [
                        param for param in self.func.__init__.__code__.co_varnames
                    ]

    def _get_context(self, kwargs: Dict):
        context = {}
        if "initial_context" in self.params:
            context["initial_context"] = Context(kwargs.get("initial_context"))

        if "previous_context" in self.params:
            context["previous_context"] = Context(kwargs.get("previous_context"))

        return context

    def _get_task(self, kwargs: Dict):
        return kwargs.get("task")
