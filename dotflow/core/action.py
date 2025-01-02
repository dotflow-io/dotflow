"""Action"""

from dotflow.core.workflow import Context


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
