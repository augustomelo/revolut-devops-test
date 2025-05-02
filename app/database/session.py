import logging
import os
from typing import Generator

from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

logger = logging.getLogger(__name__)

_database_url = os.getenv("DATABASE_URL")

if _database_url is None:
    logger.error("Environment variable 'DATABASE_URL' not set")
else:
    if "sqlite://" in _database_url:
        _engine = create_engine(
            "sqlite://",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
    else:
        _engine = create_engine(_database_url, echo=True)


def create_db_and_tables():
    try:
        SQLModel.metadata.create_all(_engine)
    except Exception as ex:
        logger.error("Unable to setup the connection or create tables", ex)


def dispose_connection():
    _engine.dispose()


def get_session() -> Generator:
    with Session(_engine) as session:
        yield session
