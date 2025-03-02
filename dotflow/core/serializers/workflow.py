"""Workflow serializer module"""

from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict  # type: ignore


class SerializerWorkflow(BaseModel):
    model_config = ConfigDict(title="workflow")

    workflow_id: UUID = Field(default=None)
