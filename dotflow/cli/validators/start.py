"""Start validator module"""

from typing import Optional

from pydantic import BaseModel, Field  # type: ignore

from dotflow.settings import Settings as settings


class StartValidator(BaseModel):

    step: str
    callable: Optional[str] = Field(default=None)
    initial_context: Optional[str] = Field(default=None)
    output: Optional[bool] = Field(default=True)
    path: Optional[str] = Field(default=settings.START_PATH)
