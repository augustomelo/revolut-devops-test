from app.internal.validators import is_username_valid


def test_valid_username_is_username_valid():
    assert is_username_valid("username") is True

def test_invalid_username_is_username_valid():
    assert is_username_valid("") is False
