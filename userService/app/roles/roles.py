from fastapi import APIRouter, HTTPException, status
from app.roles.schemas import RoleRequest
from app.roles.req_schemas import RoleAddRequest
from app.roles.utility import AccessLevel

router = APIRouter(prefix='/role', tags=['Roles'])

@router.post("/add", summary="Add new role")
async def add_new_role(role: RoleAddRequest):
    role = await RoleRequest.add(**role.dict())

    if role:
        return {"message": "Роль успешно создана", "role": role}
    else:
        return "Ошибка создании роли"

@router.post("/delete/{role_name}", summary="Delete a role")
async def delete_role(role_name: str):
    role = await RoleRequest.delete(name=role_name)

    if role:
        return "Роль успешно удалена"
    else:
        return "Ошибка удаления роли"

@router.post("/{role_name}", summary="List role's information")
async def delete_role(role_name: str) -> RoleAddRequest:
    role = await RoleRequest.find_one(name=role_name)

    if role is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Такой роли не существует'
        )

    return role
