"""Action module"""

from typing import Callable

from dotflow.core.context import Context


class Action(object):

    def __init__(self, func: Callable = None, retry: int = 1):
        self.func = func
        self.retry = retry

    def __call__(self, *args, **kwargs):
        if self.func:
            if self._has_context():
                context = kwargs.get("previous_context") or Context()
                return Context(storage=self._retry(*args, previous_context=context))
            else:
                return Context(storage=self._retry(*args))

        def wrapper(*_args, **_kwargs):
            self.func = args[0]
            if self._has_context():
                context = _kwargs.get("previous_context") or Context()
                return Context(storage=self._retry(*_args, previous_context=context))
            else:
                return Context(storage=self._retry(*_args))
        return wrapper

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

    def _has_context(self):
        return 'previous_context' in self.func.__code__.co_varnames
