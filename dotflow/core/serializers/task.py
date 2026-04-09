"""Task serializer module"""

from __future__ import annotations

import json
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from dotflow.core.context import Context


class SerializerTaskError(BaseModel):
    attempt: Optional[int] = Field(default=None)
    exception: str = Field(default="")
    traceback: str = Field(default="")
    message: str = Field(default="")


class SerializerTask(BaseModel):
    model_config = ConfigDict(title="task")

    task_id: int = Field(default=None)
    workflow_id: Optional[UUID] = Field(default=None)
    status: str = Field(default=None, alias="_status")
    duration: Optional[float] = Field(default=None, alias="_duration")
    initial_context: Any = Field(default=None, alias="_initial_context")
    current_context: Any = Field(default=None, alias="_current_context")
    previous_context: Any = Field(default=None, alias="_previous_context")
    group_name: str = Field(default=None)
    retry_count: int = Field(default=0)
    errors: list[SerializerTaskError] = Field(
        default_factory=list, alias="_errors"
    )
    max: Optional[int] = Field(default=None, exclude=True)
    size_message: Optional[str] = Field(
        default="Context size exceeded", exclude=True
    )

    def model_dump_json(self, **kwargs) -> str:
        data = json.loads(
            super().model_dump_json(serialize_as_any=True, **kwargs)
        )
        data["error"] = data["errors"][-1] if data["errors"] else None
        dump_json = json.dumps(data)

        if self.max and len(dump_json) > self.max:
            data["initial_context"] = self.size_message
            data["current_context"] = self.size_message
            data["previous_context"] = self.size_message
            dump_json = json.dumps(data)

            if len(dump_json) > self.max:
                data["errors"] = []
                data["error"] = None
                dump_json = json.dumps(data)

        return dump_json

    @field_validator("errors", mode="before")
    @classmethod
    def errors_validator(cls, value: list) -> list:
        if not value:
            return []
        return [
            SerializerTaskError(**item.__dict__)
            if not isinstance(item, dict)
            else SerializerTaskError(**item)
            for item in value
        ]

    @field_validator(
        "initial_context", "current_context", "previous_context", mode="before"
    )
    @classmethod
    def context_validator(cls, value: str) -> str:
        if value and value.storage:
            context = cls.context_loop(value=value)
            return context
        return None

    @classmethod
    def format_context(cls, value):
        try:
            return json.dumps(value.storage)
        except TypeError:
            return str(value.storage)

    @classmethod
    def context_loop(cls, value):
        if isinstance(value.storage, list):
            contexts = {}
            if any(isinstance(context, Context) for context in value.storage):
                for context in value.storage:
                    if isinstance(context, Context):
                        contexts[context.task_id] = cls.context_loop(context)
                    else:
                        contexts[context.task_id] = cls.format_context(context)
            return contexts
        return cls.format_context(value=value)
