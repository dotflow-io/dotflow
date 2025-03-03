"""Task validator module"""

from typing import Optional

from pydantic import BaseModel, Field  # type: ignore


class TaskValidator(BaseModel):

    step: str
    callback: Optional[str] = Field(default=None)
    initial_context: Optional[str] = Field(default=None)
