from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database.session import create_db_and_tables, dispose_connection
from app.routers import hello, management


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    dispose_connection()


app = FastAPI(title="Hello API", version="0.1.0", lifespan=lifespan)

app.include_router(hello.router, prefix="/hello")
app.include_router(management.router, prefix="/management")
