import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def test_client():
    return TestClient(app)

def test_upsert_birthday(test_client: TestClient):
    resp = test_client.put("/hello/augusto", json={"dateOfBirth": "1991-08-06"})

    assert resp.status_code == 204

def test_get_birthday(test_client: TestClient):
    resp = test_client.get("/hello/augusto")

    assert resp.status_code == 200
    assert (resp.json() is not None and resp.json() != "")
