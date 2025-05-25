import yaml
from app.database import Base, engine
from app.roles.roles import router as router_roles
from app.users.auth import router as router_auth
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.responses import Response

app = FastAPI()


@app.get("/")
def home_page():
    return "This is userService in ciel's SocialNetwork"


@app.on_event("startup")
async def on_startup():
    """
    Создаем таблицы в базе данных, если таковых нет.
    """

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/openapi.yaml", include_in_schema=False)
def get_openapi_yaml():
    openapi_schema = get_openapi(
        title="UserService", version="1.0.0", routes=app.routes
    )
    yaml_schema = yaml.dump(openapi_schema, sort_keys=False, allow_unicode=True)
    return Response(content=yaml_schema, media_type="application/x-yaml")


# Подключаем роуты модуля авторизации и управления ролями.
app.include_router(router_auth)
app.include_router(router_roles)
