from sqlalchemy import ForeignKey, text, Text, select
from sqlalchemy.orm import relationship, Mapped, mapped_column, joinedload
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from sqlalchemy import update as sqlalchemy_update, delete as sqlalchemy_delete 
from datetime import date
from app.database import async_session_maker, User, Profile, AccessLevel, Role
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

class BaseRequest:
    """
    Базовый DAO класс для всех моделей UserService.
    """
    model = None

    # Ищет все подходящие объекты в БД по заданным фильтрам.
    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()

    # Ищет один подходящий объект в БД по заданным фильтрам.
    @classmethod
    async def find_one(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    # Добавляет объект в БД.
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

    # Удаляет объект из БД.
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

    # Обновляет объект в БД.
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