from fastapi import APIRouter, HTTPException, HTTPException, status, Response, Depends, Request
from app.core import get_password_hash, verify_password, create_access_token, get_current_user
from app.schemas import userRegistration, UserRequest, UserResponse, ProfileRequest, ProfileAddRequest, userLogin, ProfileUpdateRequest


router = APIRouter(prefix='/auth', tags=['Auth'])

@router.get("/listall", summary="Вывести всех пользователей")
async def list_all() -> list[UserResponse]:
    return await UserRequest.find_all()

@router.get("/{id}", summary="Получить одного пользователя")
async def get_user(userID: int) -> UserResponse | str:
    response = await UserRequest.find_one(userID)
    return response if response is not None else f"Пользователя {userID} не существует"

@router.post("/register/")
async def reg_user(user_data: userRegistration) -> bool:
    user = await UserRequest.find_one(username=user_data.username)
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пользователь с таким именем уже существует'
        )

    user = await UserRequest.find_one(email=user_data.email)
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пользователь с такой почтой уже существует'
        )

    profile_request = ProfileAddRequest().dict()

    profile_result = await ProfileRequest.add(**profile_request)
    if profile_result is None: 
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Проблема с созданием профиля'
        )
    profile_id = profile_result.id

    user_request = user_data.dict()
    user_request['hashed_password'] = get_password_hash(user_data.password)
    user_request['profile_id'] = profile_id
    del user_request['password']

    await UserRequest.add(**user_request)
    return True

async def authenticate_user(username: str, password: str):
    user = await UserRequest.find_one(username=username)
    if not user or verify_password(plain_password=password, hashed_password=user.hashed_password) is False:
        return None

    return user

@router.post("/login/")
async def auth_user(response: Response, user_data: userLogin):
    code = await authenticate_user(username=user_data.username, password=user_data.password)
    if code is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Неверное имя пользователя или пароль')

    access_token = create_access_token({"sub": str(code.id)})

    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return {'access_token': access_token, 'refresh_token': None}

@router.get("/me/")
async def get_me(user_data: UserResponse = Depends(get_current_user)):
    return user_data

@router.post("/logout/")
async def logout_user(response: Response):
    response.delete_cookie(key="users_access_token")
    return {'message': 'Пользователь успешно вышел из системы'}

@router.post("/update_profile/")
async def update_profile(update_info: ProfileUpdateRequest, user_data: UserResponse = Depends(get_current_user)):
    update_request = {key: value for key, value in update_info.model_dump().items() if value is not None}

    if (len(update_request) == 0):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Пустые изменения')

    result = await ProfileRequest.update(filter_by={'id': user_data["profile_id"]}, **update_request)

    if result:
        return "Профиль успешно изменен"
    else:
        return "При изменении профиля произошла ошибка"