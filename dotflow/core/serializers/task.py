"""Task serializer module"""

from __future__ import annotations

import json
from datetime import datetime
from typing import Any, Optional
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    computed_field,
    field_validator,
)

from dotflow.core.context import Context


class SerializerTaskError(BaseModel):
    attempt: Optional[int] = Field(default=None)
    exception: str = Field(default="")
    traceback: str = Field(default="")
    message: str = Field(default="")


class SerializerTask(BaseModel):
    model_config = ConfigDict(title="task")

    task_id: str = Field(default=None)
    workflow_id: Optional[UUID] = Field(default=None)
    status: str = Field(default=None, alias="_status")
    duration: Optional[float] = Field(default=None, alias="_duration")
    initial_context: Any = Field(default=None, alias="_initial_context")
    current_context: Any = Field(default=None, alias="_current_context")
    previous_context: Any = Field(default=None, alias="_previous_context")
    group_name: str = Field(default=None)
    retry_count: int = Field(default=0)
    created_at: Optional[datetime] = Field(default=None)
    started_at: Optional[datetime] = Field(default=None)
    finished_at: Optional[datetime] = Field(default=None)
    errors: list[SerializerTaskError] = Field(
        default_factory=list, alias="_errors"
    )
    max: Optional[int] = Field(default=None, exclude=True)
    size_message: dict = Field(
        default={"message": "Context size exceeded"},
        exclude=True,
    )

    @computed_field
    @property
    def error(self) -> Optional[SerializerTaskError]:
        """Last error (convenience field)."""
        return self.errors[-1] if self.errors else None

    def model_dump_json(self, **kwargs) -> str:
        data = self.model_dump(mode="json", serialize_as_any=True, **kwargs)
        dump_json = json.dumps(data)

        if self.max is None or len(dump_json) <= self.max:
            return dump_json

        context_fields = [
            "current_context",
            "previous_context",
            "initial_context",
        ]

        for field in sorted(
            context_fields,
            key=lambda f: len(str(data.get(f, ""))),
            reverse=True,
        ):
            data[field] = self.size_message
            dump_json = json.dumps(data)
            if len(dump_json) <= self.max:
                return dump_json

        data["errors"] = []
        data["error"] = None
        dump_json = json.dumps(data)

        if self.max and len(dump_json) > self.max:
            for field in context_fields:
                data[field] = None
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
        "initial_context",
        "current_context",
        "previous_context",
        mode="before",
    )
    @classmethod
    def context_validator(cls, value: Any) -> Any:
        if value is None:
            return None
        if not isinstance(value, Context):
            return None
        if value.storage is None:
            return None
        return cls._serialize_context(value)

    @classmethod
    def _serialize_context(cls, ctx: Context) -> Any:
        """Serialize a Context to its storage value."""
        if isinstance(ctx.storage, (list, tuple)):
            contexts = {}
            for index, item in enumerate(ctx.storage):
                if isinstance(item, Context):
                    if item.task_id is not None:
                        key = item.task_id
                    else:
                        key = f"ctx:{index}"
                    contexts[key] = cls._serialize_context(item)
                else:
                    contexts[f"raw:{index}"] = cls._format_raw(item)
            return contexts
        return cls._format_storage(ctx)

    @staticmethod
    def _format_storage(ctx: Context) -> Any:
        """Format storage value as JSON string."""
        try:
            return json.dumps(ctx.storage)
        except TypeError:
            return str(ctx.storage)

    @staticmethod
    def _format_raw(value: Any) -> Any:
        """Format a raw (non-Context) value as JSON string."""
        try:
            return json.dumps(value)
        except TypeError:
            return str(value)
