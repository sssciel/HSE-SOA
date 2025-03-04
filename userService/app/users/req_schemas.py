from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime

class userRegistration(BaseModel):
    username: str = Field(default=..., min_length=1, max_length=30, description="User's login")
    password: str = Field(default=..., min_length=1, max_length=30, description="User's password")
    email: EmailStr = Field(default=..., description="User's email")

class userLogin(BaseModel):
    username: str = Field(default=..., min_length=1, max_length=30, description="User's login")
    password: str = Field(default=..., min_length=1, max_length=30, description="User's password")

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

class ProfileUpdateRequest(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    status: str | None = None
    birth_date: datetime | None = None