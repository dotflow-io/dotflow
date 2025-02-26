"""Retry module"""

from warnings import warn


def retry(max_retry: int):
    warn(
        message="The 'retry' decorator is deprecated",
        category=DeprecationWarning,
        stacklevel=2
    )

    def inside(func):

        def wrapper(*args, **kwargs):
            attempt = 0
            exception = Exception()

            while max_retry > attempt:
                try:
                    return func(*args, **kwargs)
                except Exception as error:
                    exception = error
                    attempt += 1

            raise exception

        return wrapper
    return inside
