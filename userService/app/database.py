from datetime import datetime
from typing import Annotated
import enum
import re

from sqlalchemy import func, Integer, text, ForeignKey
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column, relationship
from app.roles.utility import AccessLevel

from app.config import get_db_url

engine = create_async_engine(get_db_url())
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

int_pk = Annotated[int, mapped_column(primary_key=True)]
str_pk = Annotated[str, mapped_column(primary_key=True)]
created_at = Annotated[datetime, mapped_column(server_default=func.now())]
updated_at = Annotated[datetime, mapped_column(server_default=func.now(), onupdate=datetime.now)]
str_uniq = Annotated[str, mapped_column(unique=True, nullable=False)]
str_null_true = Annotated[str, mapped_column(nullable=True)]

# Инициализация базового класса
class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

class User(Base):
    id: Mapped[int_pk]

    username: Mapped[str_uniq]
    email: Mapped[str_uniq]
    hashed_password: Mapped[str]
    profile_id: Mapped[int] = mapped_column(ForeignKey('profiles.id'))

    profile: Mapped["Profile"] = relationship("Profile", back_populates="user")

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "hashed_password": self.hashed_password,
            "profile_id": self.profile_id
        }

class Profile(Base):
    id: Mapped[int_pk]

    first_name: Mapped[str]
    last_name: Mapped[str]
    status: Mapped[str]
    birth_date: Mapped[datetime]

    user: Mapped["User"] = relationship("User", back_populates="profile")
    
    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "status": self.status,
            "birth_date": self.birth_date
        }

class Role(Base):
    name: Mapped[str_pk]
    color: Mapped[str]
    access: Mapped[AccessLevel] = mapped_column(
        default=AccessLevel.user,
        server_default=text("'user'")
    )
    description: Mapped[str_null_true]

class UserRole(Base):
    id: Mapped[int_pk]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    role_name: Mapped[str] = mapped_column(ForeignKey('roles.name'))