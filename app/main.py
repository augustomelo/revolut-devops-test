from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database.session import create_db_and_tables, dispose_connection
from app.routers import hello


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    dispose_connection()


app = FastAPI(title="Hello API", lifespan=lifespan)

app.include_router(hello.router, prefix="/hello")
