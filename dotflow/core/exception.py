"""Exception module"""

MESSAGE_MISSING_STEP_DECORATOR = "A step function necessarily needs an 'action' decorator to circulate in the workflow. For more implementation details, access the documentation: https://dotflow-io.github.io/dotflow/nav/getting-started/#3-task-function."
MESSAGE_EXECUTION_NOT_EXIST = "The execution mode does not exist. Allowed parameter is 'sequential' and 'background'."
MESSAGE_STEP_MISSING_INIT = "The '{name}' class assigned to the step is incomplete. It is extremely important that there is an '__init__' function."


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


class StepMissingInit(Exception):

    def __init__(self, name: str):
        name = name
        super(StepMissingInit, self).__init__(
            MESSAGE_STEP_MISSING_INIT.format(name=name)
        )
