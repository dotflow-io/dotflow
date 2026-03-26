"""Start validator module"""

from pydantic import BaseModel, Field  # type: ignore

from dotflow.settings import Settings as settings


class StartValidator(BaseModel):
    step: str
    callable: str | None = Field(default=None)
    initial_context: str | None = Field(default=None)
    output: bool | None = Field(default=True)
    path: str | None = Field(default=settings.START_PATH)
