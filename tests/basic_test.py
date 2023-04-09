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


fields = ["ac", "att_bonus", "dmg_dice", "dmg_bonus"]


@pytest.mark.parametrize("field", fields)
def test_when_get_average_with_missing_field_then_return_422(client, field):
    params = dict(ac=10, att_bonus=0, dmg_dice=0, dmg_bonus=0)
    del params[field]
    r = client.get("average_damage", params=params)
    assert r.status_code == 422, r.text


def test_when_get_average_damage_then_return_200(client):
    params = dict(ac=10, att_bonus=0, dmg_dice=0, dmg_bonus=0)
    r = client.get("average_damage", params=params)
    assert r.status_code == 200, r.text


def test_when_get_average_damage_then_return_dict_with_damage_field(client):
    params = dict(ac=10, att_bonus=0, dmg_dice=0, dmg_bonus=0)
    r = client.get("average_damage", params=params)
    assert "damage" in r.json()


def test_when_get_average_damage_then_return_damage_object(client):
    params = dict(ac=10, att_bonus=0, dmg_dice=0, dmg_bonus=0)
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
    params = dict(ac=11, att_bonus=0, dmg_dice=2, dmg_bonus=20)
    r = client.get("average_damage", params=params)
    damage = r.json()["damage"]
    assert 11 < damage["simple"] < 12
    assert 8 < damage["power"] < 9


def test_when_get_damage_curve_then_return_200(client):
    params = dict(ac_min=10, ac_max=30, att_bonus=0, dmg_dice=2, dmg_bonus=20)
    r = client.get("damage_curve", params=params)
    assert r.status_code == 200


def test_when_get_damage_curve_then_return_dict_with_damage_curve_key(client):
    params = dict(ac_min=10, ac_max=30, att_bonus=0, dmg_dice=2, dmg_bonus=20)
    r = client.get("damage_curve", params=params)
    assert "damage_curve" in r.json()


def test_when_get_damage_curve_then_return_damage_curve_object(client):
    params = dict(ac_min=10, ac_max=30, att_bonus=0, dmg_dice=2, dmg_bonus=20)
    r = client.get("damage_curve", params=params)
    dmg_curve = r.json()["damage_curve"]
    assert is_damage_curve_object(dmg_curve)


def is_damage_curve_object(damage_curve):
    try:
        assert isinstance(damage_curve, dict)
        for key, value in damage_curve.items():
            assert isinstance(key, str)
            assert key.isdecimal()
            assert is_damage_object(value)
    except AssertionError:
        return False
    return True


def test_when_get_damage_curve_then_damages_are_increasing(client):
    params = dict(ac_min=10, ac_max=30, att_bonus=0, dmg_dice=2, dmg_bonus=20)
    r = client.get("damage_curve", params=params)
    dmg_curve = r.json()["damage_curve"]
    damages = list(dmg_curve.values())
    for damage_lower_ac, damage_higher_ac in zip(damages[0:], damages[1:]):
        assert damage_lower_ac["simple"] >= damage_higher_ac["simple"]
        assert damage_lower_ac["power"] >= damage_higher_ac["power"]
