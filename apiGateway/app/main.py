import httpx
from fastapi import FastAPI, Request, Response
from app.post_service import router as route_posts

USER_SERVICE_URL = "http://userservice:8001"

app = FastAPI(title="API Gateway")

@app.get("/")
def home_page():
    return "Hi! This is API GateWay."

app.include_router(route_posts)