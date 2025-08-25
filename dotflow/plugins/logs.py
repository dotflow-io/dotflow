"""Logs Handler"""

import sys
import json

from uuid import UUID
from typing import Any

from pydantic import BaseModel, Field, model_validator, field_validator

from dotflow.abc.logs import Logs
from dotflow.core.decorators.tools import _threading
from dotflow.core.types.task import StatusTaskType
from dotflow.providers.otel.logs import client

WORKFLOW_LOG_FORMAT = "{workflow_id}: {status}"


class TaskFields(BaseModel):

    task_id: int
    workflow_id: UUID
    group_name: str
    status: str = Field(alias="_status")
    duration: float = Field(alias="_duration")
    current_context_bytes: Any = Field(default=0, alias="_current_context")

    @field_validator("current_context_bytes", mode='after')
    @classmethod
    def _current_context(cls, value: int) -> int:
        return sys.getsizeof(value.storage)


class TaskLogResponse(BaseModel):

    msg: str = Field(default=None)
    extra: TaskFields
    formatting_type: str = Field(exclude=True)

    @model_validator(mode="after")
    def load_msg(self):
        self.msg = self.formatting_type.format(
            workflow_id=self.extra.workflow_id,
            task_id=self.extra.task_id,
            status=self.extra.status,
        )
        return self


class LogsHandler(Logs):
    """Logs"""

    def __init__(self):
        self.client = client

    @_threading
    def on_workflow_status_change(self, *_args, **_kwargs) -> None:
        pass

    @_threading
    def on_task_status_change(self, task_object) -> None:
        data = TaskLogResponse(
            extra=task_object.__dict__,
            formatting_type="{workflow_id}: TASK {task_id} - {status}",
        )

        if data.extra.status == StatusTaskType.FAILED:
            return

        data = json.loads(data.model_dump_json())
        self.client.info(**data)

    @_threading
    def on_status_failed(self, task_object) -> None:
        data = TaskLogResponse(
            extra=task_object.__dict__,
            formatting_type="{task_id}: {workflow_id} - {status}",
        )

        data = json.loads(data.model_dump_json())
        self.client.error(**data, exc_info=True)

    @_threading
    def when_context_assigned(self, task_object) -> None:
        data = TaskLogResponse(
            extra=task_object.__dict__,
            formatting_type="{workflow_id}: TASK {task_id} - Assigned Context",
        )

        data = json.loads(data.model_dump_json())
        self.client.info(**data)
