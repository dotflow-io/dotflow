"""Context module"""

from uuid import UUID

from typing import Any
from datetime import datetime


class ContextInstance:
    """
    Import:
        You can import the **ContextInstance** class with:

            from dotflow.core.context import ContextInstance
    """

    def __init__(self, *args, **kwargs):
        self._time = None
        self._task_id = None
        self._workflow_id = None
        self._storage = None


class Context(ContextInstance):
    """
    Import:
        You can import the Context class directly from dotflow:

            from dotflow import Context

    Example:
        `class` dotflow.core.context.Context

            Context(
                storage={"data": [0, 1, 2, 3]}
            )

    Args:
        storage (Any): Attribute where any type of Python object can be stored.

        task_id (int): Task ID.

        workflow_id (UUID): Workflow ID.
    """

    def __init__(
            self,
            storage: Any = None,
            task_id: int = None,
            workflow_id: UUID = None,
    ) -> None:
        super().__init__(
            task_id,
            storage,
            task_id,
            workflow_id
        )
        self.time = datetime.now()
        self.task_id = task_id
        self.workflow_id = workflow_id
        self.storage = storage

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value: datetime):
        self._time = value

    @property
    def task_id(self):
        return self._task_id

    @task_id.setter
    def task_id(self, value: int):
        if isinstance(value, int):
            self._task_id = value

        if not self.task_id:
            self._task_id = value

    @property
    def workflow_id(self):
        return self._workflow_id

    @workflow_id.setter
    def workflow_id(self, value: UUID):
        if isinstance(value, UUID):
            self._workflow_id = value

    @property
    def storage(self):
        return self._storage

    @storage.setter
    def storage(self, value: Any):
        if isinstance(value, Context):
            self._storage = value.storage

            self.time = value.time
            self.task_id = value.task_id
            self.workflow_id = value.workflow_id
        else:
            self._storage = value
