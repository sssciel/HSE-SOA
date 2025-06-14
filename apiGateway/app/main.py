from fastapi import FastAPI

from apiGateway.app.auth.routes import router as route_auth
from apiGateway.app.posts.actions import router as route_posts_actions
from apiGateway.app.posts.crud import router as route_posts_crud

app = FastAPI(title="API Gateway")


@app.get("/")
def home_page():
    return "Hi! This is API GateWay."


app.include_router(route_posts_crud)
app.include_router(route_posts_actions)
app.include_router(route_auth)
