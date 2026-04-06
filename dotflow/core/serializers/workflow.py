"""Workflow serializer module"""

import json
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field  # type: ignore

from dotflow.core.serializers.task import SerializerTask


class SerializerWorkflow(BaseModel):
    model_config = ConfigDict(title="workflow")

    workflow_id: UUID = Field(default=None)
    tasks: list[SerializerTask] = Field(default=[])

    def model_dump_json(self, **kwargs) -> str:
        data = json.loads(
            super().model_dump_json(serialize_as_any=True, **kwargs)
        )
        for task in data.get("tasks", []):
            task["error"] = task["errors"][-1] if task.get("errors") else None
        return json.dumps(data)
