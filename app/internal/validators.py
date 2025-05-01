import logging
import re
from datetime import date, datetime

_pattern_letters = re.compile("^[a-zA-Z]+$")

logger = logging.getLogger(__name__)

def is_username_valid(username: str) -> bool:
    logger.info(f"Validating username={username}")
    if _pattern_letters.match(username):
        return True

    logger.warning(f"Invalid username={username}, didn't match pattern={_pattern_letters}")
    return False


def is_dob_valid(dob: date) -> bool:
    logger.info(f"Validating dateOfBirth={dob}")
    # must be a date before the today date
    if dob < get_today():
        return True

    logger.warning(f"Invalid dateOfBirth={dob}, dob >= today")
    return False


def get_today() -> date:
    return datetime.now().date()
