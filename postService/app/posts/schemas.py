from sqlalchemy import String, Text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from postService.app.db.core import Base, int_pk, str_null_true


class Post(Base):
    post_id: Mapped[int_pk]
    creator_id: Mapped[int]

    title: Mapped[str] = mapped_column(Text)
    description: Mapped[str_null_true] = mapped_column(Text)
    is_private: Mapped[bool] = mapped_column(default=False)
    tags: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)

    def to_dict(self):
        return {
            "post_id": self.post_id,
            "creator_id": self.creator_id,
            "title": self.title,
            "description": self.description,
            "is_private": self.is_private,
            "tags": self.tags,
        }
