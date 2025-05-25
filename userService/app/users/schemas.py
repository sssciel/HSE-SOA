from app.database import Profile, User, async_session_maker
from app.schemas import BaseRequest
from sqlalchemy import select
from sqlalchemy.orm import joinedload


class UserRequest(BaseRequest):
    model = User

    @classmethod
    async def find_one_id(cls, data_id):
        async with async_session_maker() as session:
            query = (
                select(cls.model)
                .options(joinedload(cls.model.profile))
                .filter_by(id=data_id)
            )
            result = await session.execute(query)
            result = result.scalar_one_or_none()

            if result is None:
                return result

            userData = result.to_dict()
            userData["profile"] = result.profile
            return userData


class ProfileRequest(BaseRequest):
    model = Profile
