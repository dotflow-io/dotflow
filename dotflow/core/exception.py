"""Exception module"""

MESSAGE_MISSING_STEP_DECORATOR = "A step function necessarily needs an 'action' decorator to circulate in the workflow. For more implementation details, access the documentation: https://dotflow-io.github.io/dotflow/nav/getting-started/#3-task-function."
MESSAGE_EXECUTION_NOT_EXIST = "The execution mode does not exist. Allowed parameter is 'sequential' and 'background'."


class MissingStepDecorator(Exception):

    def __init__(self):
        super(MissingStepDecorator, self).__init__(MESSAGE_MISSING_STEP_DECORATOR)


class ExecutionModeNotExist(Exception):

    def __init__(self):
        super(ExecutionModeNotExist, self).__init__(MESSAGE_EXECUTION_NOT_EXIST)
