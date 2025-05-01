import logging
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Body, HTTPException, status

from app.internal.validators import is_dob_valid, is_username_valid

router = APIRouter()

logger = logging.getLogger(__name__)


@router.put("/{username}", status_code=status.HTTP_204_NO_CONTENT)
async def upsert_birthday(
    username: str, dobstr: Annotated[str, Body(alias="dateOfBirth", embed=True)]
):
    logger.info(f"Received username={username} dateOfBirth={dobstr}")

    if not is_username_valid(username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid username"
        )

    try:
        dob = datetime.strptime(dobstr, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ivalid dateOfBirth format, corret one is: 'YYYY-MM-DD'",
        )

    if not is_dob_valid(dob):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid dateOfBirth value, it must be a date before the today date",
        )


@router.get("/{username}")
async def get_birthday(username: str):
    msg = f"Hello, {username}! Your birthday is in N day(s)"
    return {"message": msg}
