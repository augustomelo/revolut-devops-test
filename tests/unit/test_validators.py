from datetime import datetime

from pytest_mock import MockerFixture

from app.internal.validators import is_dob_valid, is_username_valid


def test_valid_username_is_username_valid():
    assert is_username_valid("username")


def test_invalid_username_is_username_valid():
    assert not is_username_valid("")


def test_before_dob_is_dob_valid(mocker: MockerFixture):
    mock_date = mocker.patch("app.internal.validators.get_today")
    mock_date.return_value = datetime(2025, 4, 1).date()

    assert is_dob_valid(datetime(2025, 3, 30).date())


# must be a date before the today date
def test_equal_dob_is_dob_valid(mocker: MockerFixture):
    mock_date = mocker.patch("app.internal.validators.get_today")
    mock_date.return_value = datetime(2025, 4, 1).date()

    assert not is_dob_valid(datetime(2025, 4, 1).date())


def test_after_dob_is_dob_valid(mocker: MockerFixture):
    mock_date = mocker.patch("app.internal.validators.get_today")
    mock_date.return_value = datetime(2025, 4, 1).date()

    assert not is_dob_valid(datetime(2025, 4, 2).date())
