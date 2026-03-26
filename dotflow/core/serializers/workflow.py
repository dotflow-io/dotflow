"""Workflow serializer module"""

from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field  # type: ignore

from dotflow.core.serializers.task import SerializerTask


class SerializerWorkflow(BaseModel):
    model_config = ConfigDict(title="workflow")

    workflow_id: UUID = Field(default=None)
    tasks: list[SerializerTask] = Field(default=[])
