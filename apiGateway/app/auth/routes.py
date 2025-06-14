import httpx
from fastapi import APIRouter, Request, Response
from fastapi.responses import StreamingResponse

from apiGateway.app.config import get_user_service_url

AUTH_SERVICE_URL = get_user_service_url()

router = APIRouter(prefix="/auth")


async def _proxy(request: Request, dest: str) -> Response:
    async with httpx.AsyncClient(follow_redirects=True) as client:
        proxied = await client.request(
            request.method,
            dest,
            params=request.query_params,
            content=await request.body(),
            headers={k: v for k, v in request.headers.items() if k.lower() != "host"},
            timeout=20,
        )
    return Response(
        content=proxied.content,  # <-- читаем весь ответ целиком
        status_code=proxied.status_code,
        headers=proxied.headers,
        media_type=proxied.headers.get("content-type"),
    )


@router.post("/register")
@router.post("/login")
@router.post("/logout")
@router.get("/me")
@router.post("/update_profile")
@router.get("/listall")
@router.api_route(
    "/{rest_of_path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]
)
async def auth_proxy(rest_of_path: str = "", request: Request = None):
    dest = (
        f"{AUTH_SERVICE_URL}/auth/{rest_of_path}"
        if rest_of_path
        else f"{AUTH_SERVICE_URL}{request.url.path}"
    )
    return await _proxy(request, dest)
