import httpx
from fastapi import Request, HTTPException, status

USERSERVICE_URL = "http://userservice:8001"

async def get_current_user(request: Request):
    token = request.cookies.get("users_access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication token"
        )

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{USERSERVICE_URL}/auth/me/", cookies={"users_access_token": token})

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail="Invalid or expired authentication token"
        )

    return response.json()