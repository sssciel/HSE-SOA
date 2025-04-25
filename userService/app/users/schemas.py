from sqlalchemy import ForeignKey, text, Text, select
from sqlalchemy.orm import relationship, Mapped, mapped_column, joinedload
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from sqlalchemy import update as sqlalchemy_update, delete as sqlalchemy_delete 
from datetime import date
from app.database import async_session_maker, User, Profile, AccessLevel, Role
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from app.schemas import BaseRequest


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