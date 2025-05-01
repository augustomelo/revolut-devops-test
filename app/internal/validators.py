import re
from datetime import date, datetime

_pattern_letters = re.compile("^[a-zA-Z]+$")


def is_username_valid(username: str) -> bool:
    if _pattern_letters.match(username):
        return True

    return False


def is_dob_valid(dob: date) -> bool:
    # must be a date before the today date
    if dob < get_today():
        return True

    return False


def get_today() -> date:
    return datetime.now().date()
