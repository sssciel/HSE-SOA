from app.database import Role, UserRole
from app.schemas import BaseRequest


class RoleRequest(BaseRequest):
    model = Role


class UserRoleRequest(BaseRequest):
    model = UserRole
