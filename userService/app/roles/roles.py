from app.roles.req_schemas import RoleAddRequest, RoleSetRequest
from app.roles.schemas import RoleRequest, UserRoleRequest
from app.roles.utility import AccessLevel
from app.users.schemas import UserRequest
from fastapi import APIRouter, HTTPException, status

router = APIRouter(prefix="/role", tags=["Roles"])


@router.get("/user_role_status/{user_name}")
async def user_status(user_name: str):
    userRoles = await get_user_roles(user_name)

    roles = [await RoleRequest.find_one(name=role.role_name) for role in userRoles]
    userAccessLevels = {role.access for role in roles}

    if AccessLevel.banned in userAccessLevels:
        return AccessLevel.banned
    elif AccessLevel.admin in userAccessLevels:
        return AccessLevel.admin

    return 1


@router.post("/add", summary="Add new role")
async def add_new_role(role_request: RoleAddRequest):
    role = await RoleRequest.add(**role_request.dict())
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
async def get_role_info(roleName: str) -> RoleAddRequest:
    role = await RoleRequest.find_one(name=roleName)
    if role is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Такой роли не существует"
        )

    return role


@router.post("/set_role/")
async def set_role(setRequest: RoleSetRequest):
    role = await RoleRequest.find_one(name=setRequest.roleName)
    if role is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Такой роли не существует"
        )

    user = await UserRequest.find_one(username=setRequest.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Такого пользователя не существует",
        )

    userID = user.id

    roleExists = await UserRoleRequest.find_one(
        user_id=userID, role_name=setRequest.roleName
    )
    if roleExists is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="У пользователя уже есть эта роль",
        )

    result = await UserRoleRequest.add(user_id=userID, role_name=setRequest.roleName)
    if result is None:
        return "Что-то пошло не так"
    else:
        return "Роль успешно установлена"


@router.delete("/remove_role/")
async def delete_role(setRequest: RoleSetRequest):
    user = await UserRequest.find_one(username=setRequest.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Такого пользователя не существует",
        )

    userID = user.id

    roleExists = await UserRoleRequest.find_one(
        user_id=userID, role_name=setRequest.roleName
    )
    if roleExists is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="У пользователя нет этой роли"
        )

    result = await UserRoleRequest.delete(
        delete_all=True, user_id=userID, role_name=setRequest.roleName
    )
    if result is None:
        return "Что-то пошло не так"

    return "Роль успешно снята"


async def get_user_roles(user_name: str):
    user = await UserRequest.find_one(username=user_name)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Такого пользователя не существует",
        )

    userID = user.id

    rolesResponse = await UserRoleRequest.find_all(user_id=userID)

    return rolesResponse


@router.get("/get_roles/{user_name}")
async def get_user_roles_router(user_name: str):
    rolesResponse = await get_user_roles(user_name)

    roles = [i.role_name for i in rolesResponse]
    return roles
