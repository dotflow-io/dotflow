"""DotFlow"""


from dotflow.abc.workflow import ABCWorkflow
from dotflow.core.context import Context
from dotflow.core.controller import Controller
from dotflow.core.task import TaskBuilder


class DotFlow(ABCWorkflow):

    def __init__(self, initial_context: Context = Context()) -> None:
        if not isinstance(initial_context, Context):
            initial_context = Context(storage=initial_context)

        self.task = TaskBuilder()
        self.start = Controller
        self.initial_context = initial_context
