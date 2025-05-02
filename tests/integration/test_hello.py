from datetime import datetime

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.database.session import get_session
from app.main import app


@pytest.fixture
def session(mocker: MockerFixture):
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture
def test_client(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_insert_upsert_birthday(test_client: TestClient):
    respput = test_client.put("/hello/augusto", json={"dateOfBirth": "1992-08-06"})
    respget = test_client.get("/hello/augusto")

    assert respput.status_code == status.HTTP_204_NO_CONTENT
    assert respget.status_code == status.HTTP_200_OK


def test_update_upsert_birthday(mocker: MockerFixture, test_client: TestClient):
    mock_date = mocker.patch("app.internal.utils.datetime")
    mock_date.now.return_value = datetime(2025, 4, 2)

    respput = test_client.put("/hello/augusto", json={"dateOfBirth": "1992-08-06"})
    respget = test_client.get("/hello/augusto")
    respupdt = test_client.put("/hello/augusto", json={"dateOfBirth": "2024-04-02"})
    respgetbday = test_client.get("/hello/augusto")

    assert respput.status_code == status.HTTP_204_NO_CONTENT
    assert respget.status_code == status.HTTP_200_OK
    assert "Your birthday" in respget.json()["message"]
    assert respupdt.status_code == status.HTTP_204_NO_CONTENT
    assert "Happy birthday!" in respgetbday.json()["message"]


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


def test_no_username_database_get_birthday(test_client: TestClient):
    resp = test_client.get("/hello/augusto")

    assert resp.status_code == status.HTTP_404_NOT_FOUND


def test_get_birthday(test_client: TestClient):
    resp = test_client.put("/hello/augusto", json={"dateOfBirth": "1992-08-06"})
    resp = test_client.get("/hello/augusto")

    assert resp.status_code == status.HTTP_200_OK
    assert "augusto" in resp.json()["message"]
