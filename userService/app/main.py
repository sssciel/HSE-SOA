from fastapi import FastAPI
from app.database import engine, Base
from app.users.auth import router as router_auth
from app.roles.roles import router as router_roles
from app.schemas import test_db_connection

app = FastAPI()

@app.get("/")
def home_page():
    return "This is userService in ciel's SocialNetwork"

@app.on_event("startup")
async def on_startup():
    """
    Создаем таблицы в базе данных, если таковых нет.
    """

    # await test_db_connection()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Подключаем роуты модуля авторизации и управления ролями.
app.include_router(router_auth)
app.include_router(router_roles)