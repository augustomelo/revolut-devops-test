import logging
from typing import Annotated

from fastapi import APIRouter, Body, status

router = APIRouter()

logger = logging.getLogger(__name__)


@router.put("/{username}", status_code=status.HTTP_204_NO_CONTENT)
async def upsert_birthday(username: str, dob: Annotated[str, Body(alias="dateOfBirth", embed=True)]):
    logger.info(f"Received username={username} dateOfBirth={dob}")


@router.get("/{username}")
async def get_birthday(username: str):
    msg = f"Hello, {username}! Your birthday is in N day(s)"
    return {"message": msg}
