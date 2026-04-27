"""Exception module"""

from dotflow.utils import message_error, traceback_error

MESSAGE_UNKNOWN_ERROR = (
    "Unknown error, please check logs for more information."
)
MESSAGE_MISSING_STEP_DECORATOR = "A step function necessarily needs an '@action' decorator to circulate in the workflow. For more implementation details, access the documentation: https://dotflow-io.github.io/dotflow/#3-task-function."
MESSAGE_NOT_CALLABLE_OBJECT = "Problem validating the '{name}' object type; this is not a callable object"
MESSAGE_EXECUTION_NOT_EXIST = "The execution mode does not exist. Allowed parameter is 'sequential', 'background' and 'parallel'."
MESSAGE_IMPORT_MODULE_ERROR = "Error importing Python module '{module}'."
MESSAGE_PROBLEM_ORDERING = (
    "Problem with correctly ordering functions of the '{name}' class."
)
MESSAGE_MODULE_NOT_FOUND = (
    "Module '{module}' not found. Please install with 'pip install {library}'"
)
MESSAGE_INVALID_WORKFLOW_FACTORY = (
    "'{factory}' must be a callable that returns a DotFlow instance."
)
MESSAGE_WORKFLOW_FLAG_CONFLICT = (
    "{flag} is only valid with --step and cannot be used with --workflow."
)
MESSAGE_INPUT_CHANGED = (
    "Workflow '{workflow_id}' was previously executed with a different "
    "initial_context. Pass on_input_change='reset' to discard prior "
    "checkpoints, or 'reuse' to ignore the new input."
)
MESSAGE_INVALID_ON_INPUT_CHANGE = (
    "on_input_change must be one of 'reuse', 'reset', 'raise'; got '{value}'."
)


class MissingActionDecorator(Exception):
    def __init__(self):
        super().__init__(MESSAGE_MISSING_STEP_DECORATOR)


class ExecutionModeNotExist(Exception):
    def __init__(self):
        super().__init__(MESSAGE_EXECUTION_NOT_EXIST)


class ImportModuleError(Exception):
    def __init__(self, module: str):
        super().__init__(MESSAGE_IMPORT_MODULE_ERROR.format(module=module))


class NotCallableObject(Exception):
    def __init__(self, name: str):
        super().__init__(MESSAGE_NOT_CALLABLE_OBJECT.format(name=name))


class ProblemOrdering(Exception):
    def __init__(self, name: str):
        super().__init__(MESSAGE_PROBLEM_ORDERING.format(name=name))


class ModuleNotFound(Exception):
    def __init__(self, module: str, library: str):
        super().__init__(
            MESSAGE_MODULE_NOT_FOUND.format(module=module, library=library)
        )


class InvalidWorkflowFactory(Exception):
    def __init__(self, factory: str):
        super().__init__(
            MESSAGE_INVALID_WORKFLOW_FACTORY.format(factory=factory)
        )


class WorkflowFlagConflict(Exception):
    def __init__(self, flag: str):
        super().__init__(MESSAGE_WORKFLOW_FLAG_CONFLICT.format(flag=flag))


class ExecutionWithClassError(Exception):
    def __init__(self):
        super().__init__("Unknown")


class InputChangedError(Exception):
    def __init__(self, workflow_id: str):
        super().__init__(
            MESSAGE_INPUT_CHANGED.format(workflow_id=workflow_id)
        )


class InvalidOnInputChange(Exception):
    def __init__(self, value: str):
        super().__init__(
            MESSAGE_INVALID_ON_INPUT_CHANGE.format(value=value)
        )


class TaskError:
    def __init__(self, error: Exception = None, attempt: int = None) -> None:
        self.attempt = attempt
        self.exception = type(error).__name__ if error else ""
        self.traceback = traceback_error(error=error) if error else ""
        self.message = message_error(error=error) if error else ""
