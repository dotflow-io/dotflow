"""Workflow serializer module"""

# mypy: disable-error-code="misc"

from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, computed_field

from dotflow.core.serializers.task import SerializerTask


class SerializerWorkflow(BaseModel):
    model_config = ConfigDict(title="workflow")

    workflow_id: UUID = Field(default=None)
    workflow_name: str | None = Field(default=None)
    tasks: list[SerializerTask] = Field(default=[])

    @computed_field
    @property
    def id(self) -> UUID | None:
        return self.workflow_id

    @computed_field
    @property
    def name(self) -> str | None:
        return self.workflow_name
