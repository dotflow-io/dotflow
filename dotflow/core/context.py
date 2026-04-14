"""Context module"""

from datetime import datetime
from typing import Any
from uuid import UUID


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

        task_id (str): Task ID (ULID).

        workflow_id (UUID): Workflow ID.
    """

    def __init__(
        self,
        storage: Any = None,
        task_id: str = "",
        workflow_id: UUID = None,
    ) -> None:
        super().__init__(task_id, storage, task_id, workflow_id)
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
    def task_id(self, value: str):
        if value is None:
            self._task_id = None
            return
        if not isinstance(value, str):
            raise TypeError(
                f"task_id must be a str, got {type(value).__name__}: {value!r}"
            )
        self._task_id = value

    @property
    def workflow_id(self):
        return self._workflow_id

    @workflow_id.setter
    def workflow_id(self, value: UUID):
        if value is None:
            self._workflow_id = None
            return
        if isinstance(value, str):
            try:
                value = UUID(value)
            except ValueError as err:
                raise ValueError(
                    f"Invalid workflow_id: '{value}' is not a valid UUID format."
                ) from err
        if not isinstance(value, UUID):
            raise TypeError(
                f"workflow_id must be a UUID or UUID string, "
                f"got {type(value).__name__}: {value!r}"
            )
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
