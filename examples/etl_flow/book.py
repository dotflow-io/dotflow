from pydantic import BaseModel  # type: ignore


class Book(BaseModel):

    title: str
    author: str
