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


fields = ["ca", "att_bonus", "dmg_dice", "dmg_bonus"]


@pytest.mark.parametrize("field", fields)
def test_when_get_average_with_missing_field_then_return_422(client, field):
    params = dict(ca=10, att_bonus=0, dmg_dice=0, dmg_bonus=0)
    del params[field]
    r = client.get("average_damage", params=params)
    assert r.status_code == 422, r.text


def test_when_get_average_damage_then_return_200(client):
    params = dict(ca=10, att_bonus=0, dmg_dice=0, dmg_bonus=0)
    r = client.get("average_damage", params=params)
    assert r.status_code == 200, r.text


def test_when_get_average_damage_then_return_dict_with_damage_field(client):
    params = dict(ca=10, att_bonus=0, dmg_dice=0, dmg_bonus=0)
    r = client.get("average_damage", params=params)
    assert "damage" in r.json()


def test_when_get_average_damage_then_return_damage_object(client):
    params = dict(ca=10, att_bonus=0, dmg_dice=0, dmg_bonus=0)
    r = client.get("average_damage", params=params)
    assert is_damage_object(r.json()["damage"])


def is_damage_object(damage):
    if not isinstance(damage, dict):
        return False
    expected_fields = ["simple", "power"]
    if set(damage.keys()) != set(expected_fields):
        return False
    for field in expected_fields:
        if not isinstance(damage[field], (int, float)):
            return False
    return True


def test_when_get_average_damage_then_return_expected_values(client):
    params = dict(ca=11, att_bonus=0, dmg_dice=2, dmg_bonus=20)
    r = client.get("average_damage", params=params)
    damage = r.json()["damage"]
    assert 11 < damage["simple"] < 12
    assert 8 < damage["power"] < 9
