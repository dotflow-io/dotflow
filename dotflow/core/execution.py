"""Execution module — compatibility wrapper around TaskEngine"""

from collections.abc import Callable
from uuid import UUID

from dotflow.core.context import Context
from dotflow.core.engine import TaskEngine
from dotflow.core.task import Task
from dotflow.utils import basic_callback


class Execution:
    """Backward-compatible wrapper that delegates to TaskEngine.

    Preserves the original interface where instantiation triggers execution.
    New code should use TaskEngine directly.
    """

    VALID_OBJECTS = TaskEngine.VALID_OBJECTS

    def __init__(
        self,
        task: Task,
        workflow_id: UUID,
        previous_context: Context = None,
        _flow_callback: Callable = basic_callback,
    ) -> None:
        self.task = task
        engine = TaskEngine(
            task=task,
            workflow_id=workflow_id,
            previous_context=previous_context,
        )

        with engine.start():
            engine.execute_with_retry()

        self.task.callback(task=self.task)
        _flow_callback(task=self.task)

    def _is_action(self, class_instance: Callable, func: Callable):
        engine = TaskEngine.__new__(TaskEngine)
        return engine._is_action(class_instance, func)

    def _execution_orderer(
        self, callable_list: list[str], class_instance: Callable
    ):
        engine = TaskEngine.__new__(TaskEngine)
        return engine._execution_orderer(callable_list, class_instance)
