"""Workflow serializer module"""

from uuid import UUID
from typing import List

from pydantic import BaseModel, Field, ConfigDict  # type: ignore

from dotflow.core.serializers.task import SerializerTask


class SerializerWorkflow(BaseModel):
    model_config = ConfigDict(title="workflow")

    workflow_id: UUID = Field(default=None)
    tasks: List[SerializerTask] = Field(default=[])
