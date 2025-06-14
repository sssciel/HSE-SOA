from fastapi import HTTPException, Request, status
from jose import JWTError, jwt

from apiGateway.app.config import get_auth_data

SECRET_KEY = get_auth_data()["secret_key"]
ALGORITHM = get_auth_data()["algorithm"]


def decode_jwt(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        return user_id
    except JWTError:
        return None


def get_current_user(request: Request):
    token = request.cookies.get("users_access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication token",
        )

    user_id = decode_jwt(token)

    return user_id
