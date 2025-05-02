from datetime import date, datetime


def get_today() -> date:
    return datetime.now().date()
