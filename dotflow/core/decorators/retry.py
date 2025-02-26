"""Retry module"""

from warnings import warn


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
