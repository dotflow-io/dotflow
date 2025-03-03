"""Start validator module"""

from typing import Optional

from pydantic import BaseModel, Field  # type: ignore


class StartValidator(BaseModel):

    step: str
    callable: Optional[str] = Field(default=None)
