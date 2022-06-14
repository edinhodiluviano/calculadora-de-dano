import pytest
from fastapi.testclient import TestClient

from service import main


@pytest.fixture(scope="function")
def client():
    app = main.make_app()
    return TestClient(app)


def test_should_always_pass():
    return


def test_when_get_ping_then_return_200(client):
    resp = client.get("ping2")
    assert resp.status_code == 200
