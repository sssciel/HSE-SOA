import httpx
from fastapi import FastAPI, Request, Response

USER_SERVICE_URL = "http://userservice:8001"

app = FastAPI(title="API Gateway")


async def proxy_request(request: Request, path: str):
    """Функция проксирования запроса к userService"""
    async with httpx.AsyncClient() as client:
        url = f"{USER_SERVICE_URL}/{path}"
        method = request.method
        headers = dict(request.headers)
        
        try:
            response = await client.request(
                method, url, headers=headers, content=await request.body()
            )
            return Response(
                content=response.content,
                status_code=response.status_code,
                headers=dict(response.headers)
            )
        except httpx.RequestError:
            return Response(
                content="User Service is unavailable",
                status_code=503
            )


@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def gateway(path: str, request: Request):
    """Обработчик всех маршрутов, проксирующий их на userService"""
    return await proxy_request(request, path)