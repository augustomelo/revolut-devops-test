import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def test_client():
    return TestClient(app)


def test_upsert_birthday(test_client: TestClient):
    resp = test_client.put("/hello/augusto", json={"dateOfBirth": "1992-08-06"})

    assert resp.status_code == status.HTTP_204_NO_CONTENT


def test_invalid_username_upsert_birthday(test_client: TestClient):
    resp = test_client.put(
        "/hello/invalid-username", json={"dateOfBirth": "1992-08-06"}
    )

    assert resp.status_code == status.HTTP_400_BAD_REQUEST


def test_invalid_dob_format_upsert_birthday(test_client: TestClient):
    resp = test_client.put("/hello/augusto", json={"dateOfBirth": "06-08-1992"})

    assert resp.status_code == status.HTTP_400_BAD_REQUEST


def test_invalid_dob_future_upsert_birthday(test_client: TestClient):
    resp = test_client.put("/hello/augusto", json={"dateOfBirth": "3000-08-02"})

    assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_birthday(test_client: TestClient):
    resp = test_client.get("/hello/augusto")

    assert resp.status_code == status.HTTP_200_OK
    assert resp.json() is not None and resp.json() != ""
