"""Task serializer module"""

import json

from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict, field_validator

from dotflow.core.context import Context


class SerializerTaskError(BaseModel):

    traceback: str
    message: str


class SerializerTask(BaseModel):
    model_config = ConfigDict(title="task")

    task_id: int = Field(default=None)
    workflow_id: Optional[UUID] = Field(default=None)
    status: str = Field(default=None, alias="_status")
    error: Optional[SerializerTaskError] = Field(default=None, alias="_error")
    duration: Optional[float] = Field(default=None, alias="_duration")
    initial_context: Any = Field(default=None, alias="_initial_context")
    current_context: Any = Field(default=None, alias="_current_context")
    previous_context: Any = Field(default=None, alias="_previous_context")
    group_name: str = Field(default=None)
    max: Optional[int] = Field(default=None, exclude=True)
    size_message: Optional[str] = Field(default="Context size exceeded", exclude=True)

    def model_dump_json(self, **kwargs) -> str:
        dump_json = super().model_dump_json(serialize_as_any=True, **kwargs)

        if self.max and len(dump_json) > self.max:
            self.initial_context = self.size_message
            self.current_context = self.size_message
            self.previous_context = self.size_message

            dump_json = super().model_dump_json(serialize_as_any=True, **kwargs)

            return dump_json[0:self.max]

        return dump_json

    @field_validator("error", mode="before")
    @classmethod
    def error_validator(cls, value: str) -> str:
        if value:
            return SerializerTaskError(**value.__dict__)
        return None

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
