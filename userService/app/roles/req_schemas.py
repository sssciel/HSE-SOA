from pydantic import BaseModel, EmailStr, Field, ConfigDict
from app.roles.utility import AccessLevel

class RoleAddRequest(BaseModel):
    name: str = Field(..., description="Название роли")
    color: str = Field(..., description="Цвет роли в формате '(r, g, b)'")
    access: AccessLevel = Field(default=1, description="Уровень доступа")
    description: str | None = Field(..., description="Описание роли")

class RoleSetRequest(BaseModel):
    username: str
    roleName: str