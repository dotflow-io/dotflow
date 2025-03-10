"""Exception module"""

MESSAGE_UNKNOWN_ERROR = "Unknown error, please check logs for more information."
MESSAGE_MISSING_STEP_DECORATOR = "A step function necessarily needs an '@action' decorator to circulate in the workflow. For more implementation details, access the documentation: https://dotflow-io.github.io/dotflow/nav/getting-started/#3-task-function."
MESSAGE_NOT_CALLABLE_OBJECT = "Problem validating the '{name}' object type; this is not a callable object"
MESSAGE_EXECUTION_NOT_EXIST = "The execution mode does not exist. Allowed parameter is 'sequential' and 'background'."
MESSAGE_MODULE_NOT_FOUND = "Problem importing the python module '{module}'."
MESSAGE_PROBLEM_ORDERING = "Problem with correctly ordering functions of the '{name}' class."

class MissingActionDecorator(Exception):

    def __init__(self):
        super(MissingActionDecorator, self).__init__(
            MESSAGE_MISSING_STEP_DECORATOR
        )


class ExecutionModeNotExist(Exception):

    def __init__(self):
        super(ExecutionModeNotExist, self).__init__(
            MESSAGE_EXECUTION_NOT_EXIST
        )


class ModuleNotFound(Exception):

    def __init__(self, module: str):
        super(ModuleNotFound, self).__init__(
            MESSAGE_MODULE_NOT_FOUND.format(
                module=module
            )
        )


class NotCallableObject(Exception):

    def __init__(self, name: str):
        super(NotCallableObject, self).__init__(
            MESSAGE_NOT_CALLABLE_OBJECT.format(
                name=name
            )
        )


class ProblemOrdering(Exception):

    def __init__(self, name: str):
        super(ProblemOrdering, self).__init__(
            MESSAGE_PROBLEM_ORDERING.format(
                name=name
            )
        )