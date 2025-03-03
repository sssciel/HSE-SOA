from sqlalchemy import ForeignKey, text, Text, select
from sqlalchemy.orm import relationship, Mapped, mapped_column, joinedload
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from sqlalchemy import update as sqlalchemy_update, delete as sqlalchemy_delete 
from datetime import date
from app.database import async_session_maker, User, Profile, AccessLevel, Role
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

class userRegistration(BaseModel):
    username: str = Field(default=..., min_length=1, max_length=30, description="User's login")
    password: str = Field(default=..., min_length=1, max_length=30, description="User's password")
    email: EmailStr = Field(default=..., description="User's email")

class userLogin(BaseModel):
    username: str = Field(default=..., min_length=1, max_length=30, description="User's login")
    password: str = Field(default=..., min_length=1, max_length=30, description="User's password")

class BaseRequest:
    model = None
    
    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def find_one(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def add(cls, **values):
        async with async_session_maker() as session:
            async with session.begin():
                new_instance = cls.model(**values)
                session.add(new_instance)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return new_instance

    @classmethod
    async def delete(cls, delete_all: bool = False, **filter_by):
        if not delete_all and not filter_by:
            raise ValueError("Необходимо указать хотя бы один параметр для удаления.")

        async with async_session_maker() as session:
            async with session.begin():
                query = sqlalchemy_delete(cls.model).filter_by(**filter_by)
                result = await session.execute(query)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return result.rowcount

    @classmethod
    async def update(cls, filter_by, **values):
        async with async_session_maker() as session:
            async with session.begin():
                query = (
                    sqlalchemy_update(cls.model)
                    .where(*[getattr(cls.model, k) == v for k, v in filter_by.items()])
                    .values(**values)
                    .execution_options(synchronize_session="fetch")
                )
                result = await session.execute(query)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return result.rowcount

class UserRequest(BaseRequest):
    model = User

    @classmethod
    async def find_one_id(cls, data_id):
        async with async_session_maker() as session:
            query = select(cls.model).options(joinedload(cls.model.profile)).filter_by(id=data_id)
            result = await session.execute(query)
            result = result.scalar_one_or_none()

            if result is None:
                return result

            userData = result.to_dict()
            userData["profile"] = result.profile
            return userData

class ProfileRequest(BaseRequest):
    model = Profile

class RoleRequest(BaseRequest):
    model = Role

class UserAddRequest(BaseModel):
    username: str
    email: str
    hashed_password: str
    profile_id: int

class ProfileAddRequest(BaseModel):
    first_name: str
    last_name: str
    status: str
    birth_date: datetime

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int

    username: str
    email: str
    hashed_password: str
    profile_id: int
    profile: dict

class RoleAddRequest(BaseModel):
    name: str = Field(..., description="Название роли")
    color: str = Field(..., description="Цвет роли в формате '(r, g, b)'")
    access: AccessLevel = Field(..., description="Уровень доступа")
    description: str | None = Field(..., description="Описание роли")

class ProfileUpdateRequest(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    status: str | None = None
    birth_date: datetime | None = None

