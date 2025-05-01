from fastapi import FastAPI

from app.routers import hello

app = FastAPI(title="Hello API")

app.include_router(hello.router, prefix="/hello")
