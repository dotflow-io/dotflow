"""Action module"""

from typing import Callable, Dict

from dotflow.core.context import Context


class Action(object):

    def __init__(self, func: Callable = None, retry: int = 1):
        self.func = func
        self.retry = retry

    def __call__(self, *args, **kwargs):
        if self.func:
            if self._has_context():
                context = self._get_context(kwargs=kwargs)
                return Context(storage=self._retry(*args, previous_context=context))
            else:
                return Context(storage=self._retry(*args))

        def action(*_args, **_kwargs):
            self.func = args[0]
            if self._has_context():
                context = self._get_context(kwargs=_kwargs)
                return Context(storage=self._retry(*_args, previous_context=context))
            else:
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

    def _has_context(self):
        return 'previous_context' in self.func.__code__.co_varnames

    def _get_context(self, kwargs: Dict):
        return kwargs.get("previous_context") or Context()
