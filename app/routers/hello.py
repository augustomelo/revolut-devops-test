import logging
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlmodel import Session

from app.database.models import Birthday
from app.database.session import get_session
from app.internal.validators import is_dob_valid, is_username_valid

_date_format = "%Y-%m-%d"

router = APIRouter()

logger = logging.getLogger(__name__)


@router.put("/{username}", status_code=status.HTTP_204_NO_CONTENT)
async def upsert_birthday(
    *,
    session: Session = Depends(get_session),
    username: str,
    dobstr: Annotated[str, Body(alias="dateOfBirth", embed=True)],
):
    logger.info(f"Received username={username} dateOfBirth={dobstr}")

    if not is_username_valid(username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid username"
        )

    try:
        dob = datetime.strptime(dobstr, "%Y-%m-%d").date()
    except ValueError:
        logger.warning(f"Unable to parse with format={_date_format}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ivalid dateOfBirth format, corret one is: '{_date_format}'",
        )

    if not is_dob_valid(dob):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid dateOfBirth value, it must be a date before the today date",
        )

    db_birthday = session.get(Birthday, username)

    if not db_birthday:
        db_birthday = Birthday(username=username, date_of_birth=dob)
    else:
        db_birthday.date_of_birth = dob

    session.add(db_birthday)
    session.commit()
    session.refresh(db_birthday)


@router.get("/{username}")
async def get_birthday(*, session: Session = Depends(get_session), username: str):
    logger.info(f"Trying to find brirthday for username={username}")

    db_birthday = session.get(Birthday, username)
    if not db_birthday:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Birthday not found"
        )

    days = db_birthday.days_until_birthday()

    if days > 0:
        msg = f"Hello, {username}! Your birthday is in {db_birthday.days_until_birthday()} day(s)"
    else:
        msg = f"Hello, {username}! Happy birthday!"

    return {"message": msg}
