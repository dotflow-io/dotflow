"""Task serializer module"""

from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict  # type: ignore


class SerializerTaskError(BaseModel):

    traceback: str
    message: str


class SerializerTask(BaseModel):
    model_config = ConfigDict(title="task")

    task_id: int = Field(default=None)
    workflow_id: Optional[UUID] = Field(default=None)
    status: str = Field(default=None)
    error: Optional[SerializerTaskError] = Field(default=None)
    duration: float = Field(default=None)
    initial_context: Any = Field(default=None)
    current_context: Any = Field(default=None)
    previous_context: Any = Field(default=None)
