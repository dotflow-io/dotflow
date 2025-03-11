"""Action module"""

from typing import Callable, Dict
from types import FunctionType

from dotflow.core.context import Context


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

    Args:
        func (Callable):

        task (Callable):

        retry (int):
            Integer-type argument referring to the number of retry attempts
            the function will execute in case of failure.
    """

    def __init__(
            self,
            func: Callable = None,
            task: Callable = None,
            retry: int = 1
    ) -> None:
        self.func = func
        self.task = task
        self.retry = retry
        self.params = []

    def __call__(self, *args, **kwargs):
        # With parameters
        if self.func:
            self._set_params()

            task = self._get_task(kwargs=kwargs)
            contexts = self._get_context(kwargs=kwargs)

            if contexts:
                return Context(
                    storage=self._retry(*args, **contexts),
                    task_id=task.task_id,
                    workflow_id=task.workflow_id
                )

            return Context(
                storage=self._retry(*args),
                task_id=task.task_id,
                workflow_id=task.workflow_id
            )

        # No parameters
        def action(*_args, **_kwargs):
            self.func = args[0]
            self._set_params()

            task = self._get_task(kwargs=_kwargs)
            contexts = self._get_context(kwargs=_kwargs)

            if contexts:
                return Context(
                    storage=self._retry(*_args, **contexts),
                    task_id=task.task_id,
                    workflow_id=task.workflow_id
                )

            return Context(
                storage=self._retry(*_args),
                task_id=task.task_id,
                workflow_id=task.workflow_id
            )

        return action

    def _retry(self, *args, **kwargs):
        attempt = 0
        exception = Exception()

        while self.retry > attempt:
            try:
                return self.func(*args, **kwargs)
            except Exception as error:
                exception = error
                attempt += 1

        raise exception

    def _set_params(self):
        if isinstance(self.func, FunctionType):
            self.params = [param for param in self.func.__code__.co_varnames]

        if type(self.func) is type:
            if hasattr(self.func, "__init__"):
                if hasattr(self.func.__init__, "__code__"):
                    self.params = [param for param in self.func.__init__.__code__.co_varnames]

    def _get_context(self, kwargs: Dict):
        context = {}
        if "initial_context" in self.params:
            context["initial_context"] = Context(kwargs.get("initial_context"))

        if "previous_context" in self.params:
            context["previous_context"] = Context(kwargs.get("previous_context"))

        return context

    def _get_task(self, kwargs: Dict):
        return kwargs.get("task")
