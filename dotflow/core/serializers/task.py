"""Task serializer module"""

import json

from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict, field_validator  # type: ignore


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

    @field_validator("error", mode="before")
    @classmethod
    def error_validator(cls, value: str) -> str:
        if value:
            return SerializerTaskError(**value.__dict__)
        return value

    @field_validator(
        "initial_context", "current_context", "previous_context", mode="before"
    )
    @classmethod
    def context_validator(cls, value: str) -> str:
        if value and value.storage:
            try:
                return json.dumps(value.storage)
            except Exception:
                return str(value)
        return None
