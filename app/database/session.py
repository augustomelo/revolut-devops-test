import logging
import os
from typing import Generator

from sqlmodel import Session, SQLModel, create_engine

logger = logging.getLogger(__name__)

_database_url = os.getenv("DATABASE_URL")

if _database_url is None:
    logger.error("Environment variable 'DATABASE_URL' not set")
else:
    _engine = create_engine(_database_url, echo=True)


def create_db_and_tables():
    try:
        SQLModel.metadata.create_all(_engine)
    except Exception as ex:
        logger.error("Unable to setup the connection or create tables", ex)


def dispose_connection():
    _engine.dispose()


def get_session(database_url: str) -> Generator:
    try:
        with Session(_engine) as session:
            yield session
    except Exception as ex:
        logger.error("Unable to get a session", ex)
