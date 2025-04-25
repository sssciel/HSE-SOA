from sqlalchemy import ForeignKey, text, Text, select
from sqlalchemy.orm import relationship, Mapped, mapped_column, joinedload
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from sqlalchemy import update as sqlalchemy_update, delete as sqlalchemy_delete 
from datetime import date
from app.database import async_session_maker, UserRole, Role
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from app.schemas import BaseRequest


class RoleRequest(BaseRequest):
    model = Role

class UserRoleRequest(BaseRequest):
    model = UserRole