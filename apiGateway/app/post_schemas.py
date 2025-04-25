from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator
from datetime import datetime
from typing import List
import re

class postCreate(BaseModel):
    title: str = Field(default=..., min_length=1, max_length=30, description="Post's Title")
    description: str
    creator_id: int
    is_private: bool
    tags: List[str]

class postDelete(BaseModel):
    post_id: int

class postUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    is_private: bool | None = None
    tags: List[str] | None = None

class postOut(BaseModel):
    title: str
    description: str
    creator_id: int
    is_private: bool
    tags: List[str]
    created_at: datetime
    updated_at: datetime

class postList(BaseModel):
    posts: List[postOut]
    total: int

class CommentCreate(BaseModel):
    text: str

class CommentOut(BaseModel):
    post_id: int
    user_id: int
    text: str
    created_at: datetime

class CommentList(BaseModel):
    comments: List[CommentOut]
    total: int