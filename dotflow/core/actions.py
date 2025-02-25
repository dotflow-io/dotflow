"""Actions module"""

from typing import Any
from warnings import warn

from dotflow.core.context import Context


def action(func):
    def inside(*args, **kwargs):
        previous_context = kwargs.get("previous_context") or Context()

        if 'previous_context' in func.__code__.co_varnames:
            output = func(*args, previous_context=previous_context)
        else:
            output = func(*args)

        if output:
            if isinstance(output, Context):
                return output
            return Context(storage=output)

        return Context()

    return inside


def retry(max_retry):
    warn("The 'retry' decorator is deprecated", DeprecationWarning, stacklevel=2)

    def inside(func):

        def wrapper(*args, **kwargs):
            attempt = 0
            error_output = Exception()

            while max_retry > attempt:
                try:
                    return func(*args, **kwargs)
                except Exception as error:
                    error_output = error
                    attempt += 1

            raise error_output

        return wrapper
    return inside


class Action(object):

    def __init__(self, func=None, retry: int = 1):
        self._func = func
        self._retry = retry

    def __call__(self, *args, **kwargs):
        if self._func:
            if 'previous_context' in self._func.__code__.co_varnames:
                previous_context = kwargs.get("previous_context") or Context()
                return Context(storage=self.retry(*args, previous_context=previous_context))
            else:
                return Context(storage=self.retry(*args))

        def wrapper(*_args, **_kwargs):
            self._func = args[0]
            if 'previous_context' in args[0].__code__.co_varnames:
                previous_context = _kwargs.get("previous_context") or Context()
                return Context(storage=self.retry(*_args, previous_context=previous_context))
            else:
                return Context(storage=self.retry(*_args))
        return wrapper

    def retry(self, *args, **kwargs):
        attempt = 0
        error_output = Exception()

        while self._retry > attempt:
            try:
                return self._func(*args, **kwargs)
            except Exception as error:
                error_output = error
                attempt += 1

        raise error_output
