import logging
from datetime import date

from sqlmodel import Field, SQLModel

from app.internal.utils import get_today

logger = logging.getLogger(__name__)


class Birthday(SQLModel, table=True):
    username: str = Field(primary_key=True)
    date_of_birth: date

    def days_until_birthday(self) -> int:
        today = get_today()

        logger.info(f"Calculating days until birthday today={today} date_of_birth={self.date_of_birth}")
        days = 0

        if self.date_of_birth.replace(year=today.year) < today:
            days = (self.date_of_birth.replace(year=today.year + 1) - today).days
        else:
            days = (self.date_of_birth.replace(year=today.year) - today).days

        logger.info(f"days_until_birthday={days}")
        return days
