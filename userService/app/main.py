from fastapi import FastAPI
from app.database import engine, Base
from app.auth import router as router_auth
from app.roles import router as router_roles

app = FastAPI()

@app.get("/")
def home_page():
    return "This is userService in ciel's SocialNetwork"

# Создаем таблицы в базе данных
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(router_auth)
app.include_router(router_roles)