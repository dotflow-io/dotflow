"""Transport serializer module"""

from pydantic import BaseModel, Field, model_validator

from dotflow.core.serializers.task import SerializerTask
from dotflow.core.serializers.workflow import SerializerWorkflow


class SerializerTransport(BaseModel):
    resource: str = Field(default=None)
    content: SerializerTask | SerializerWorkflow

    @model_validator(mode="after")
    def set_resource(self):
        self.resource = self.content.model_config.get("title")
        return self
