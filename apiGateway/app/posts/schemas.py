from typing import List

from pydantic import BaseModel, Field


class postCreate(BaseModel):
    title: str = Field(default=..., min_length=1, max_length=30)
    description: str
    creator_id: int
    is_private: bool
    tags: List[str]


class postUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    is_private: bool | None = None
    tags: List[str] | None = None
