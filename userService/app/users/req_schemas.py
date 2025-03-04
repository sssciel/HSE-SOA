from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator
from datetime import datetime
import re

class userRegistration(BaseModel):
    username: str = Field(default=..., min_length=1, max_length=30, description="User's login")
    password: str = Field(default=..., min_length=1, max_length=30, description="User's password")
    email: EmailStr = Field(default=..., description="User's email")

class userLogin(BaseModel):
    username: str = Field(default=..., min_length=1, max_length=30, description="User's login")
    password: str = Field(default=..., min_length=1, max_length=30, description="User's password")

class UserAddRequest(BaseModel):
    username: str
    email: EmailStr
    hashed_password: str
    profile_id: int

class ProfileAddRequest(BaseModel):
    first_name: str = ""
    last_name: str = ""
    status: str = ""
    phone_number: str = ""
    birth_date: datetime = datetime.now()

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value: str) -> str:
        if not re.match(r'^\+\d{11}$', value):
            raise ValueError('Номер телефона должен начинаться с "+" и содержать от 11 цифр')
        return value


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int

    username: str
    email: str
    hashed_password: str
    profile_id: int
    profile: dict

class ProfileUpdateRequest(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    status: str | None = None
    birth_date: datetime | None = None
    phone_number: str | None = None

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value: str) -> str:
        if value is not None and not re.match(r'^\+\d{11}$', value):
            raise ValueError('Номер телефона должен начинаться с "+" и содержать от 11 цифр')
        return value