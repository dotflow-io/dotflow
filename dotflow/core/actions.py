"""Actions module"""

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
