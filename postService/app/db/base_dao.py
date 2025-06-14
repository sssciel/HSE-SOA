from sqlalchemy import delete as sqlalchemy_delete
from sqlalchemy import select
from sqlalchemy import update as sqlalchemy_update
from sqlalchemy.exc import SQLAlchemyError

from postService.app.db.core import async_session_maker


class BaseDAO:
    """
    Базовый DAO класс для всех моделей UserService.
    """

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

    @classmethod
    async def find_paginated(cls, limit: int, offset: int = 0, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by).offset(offset).limit(limit)
            result = await session.execute(query)
            return result.scalars().all()
