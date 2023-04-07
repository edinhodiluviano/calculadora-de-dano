import fastapi
import fastapi.testclient
import pytest

from service import main


@pytest.fixture(scope="session")
def client():
    client_ = fastapi.testclient.TestClient(main.app)
    return client_


def test_should_always_pass():
    ...


def test_ping2_return_200(client):
    r = client.get("ping2")
    assert r.status_code == 200
