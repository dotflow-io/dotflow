"""Action module"""

from typing import Callable, Dict
from types import FunctionType

from dotflow.core.context import Context


class Action(object):

    def __init__(self, func: Callable = None, retry: int = 1):
        self.func = func
        self.retry = retry
        self.params = []

    def __call__(self, *args, **kwargs):
        # With parameters
        if self.func:
            self._set_params()

            contexts = self._get_context(kwargs=kwargs)
            if contexts:
                return Context(storage=self._retry(*args, **contexts))

            return Context(storage=self._retry(*args))

        # No parameters
        def action(*_args, **_kwargs):
            self.func = args[0]
            self._set_params()

            contexts = self._get_context(kwargs=_kwargs)
            if contexts:
                return Context(storage=self._retry(*_args, **contexts))

            return Context(storage=self._retry(*_args))

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
            context["initial_context"] = kwargs.get("initial_context") or Context()

        if "previous_context" in self.params:
            context["previous_context"] = kwargs.get("previous_context") or Context()

        return context
