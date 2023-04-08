import pytest

from service.main import Damage


simple_cases = [
    # dice    bonus    avg
    [    0,       0,     0],  # NOQA: BLK100
    [    1,       0,     1],
    [    1,       2,     3],
    [    0,       2,     2],
    [  4.5,      13,  17.5],
    [    1,      -1,     0],
    [    1,      -2,     0],
]


@pytest.mark.parametrize("dice,bonus,expected_avg", simple_cases)
def test_simple_cases(dice, bonus, expected_avg):
    dmg = Damage(dice=dice, bonus=bonus)
    assert dmg.avg() == expected_avg


power_attack_cases = [
    # dice    bonus    avg
    [    0,       0,    10],
    [    1,       0,    11],
    [    1,       2,    13],
    [    0,       2,    12],
    [  4.5,      13,  27.5],
    [    1,      -1,    10],
    [    1,      -2,     9],
    [    1,     -10,     1],
    [    1,     -11,     0],
    [    1,     -12,     0],
]


@pytest.mark.parametrize("dice,bonus,expected_avg", power_attack_cases)
def test_damage_with_power_attack(dice, bonus, expected_avg):
    dmg = Damage(dice=dice, bonus=bonus)
    assert dmg.power().avg() == expected_avg


critical_damage_cases = [
    # dice    bonus    avg
    [    0,       0,     0],
    [    1,       0,     2],
    [    1,       2,     4],
    [    0,       2,     2],
    [  4.5,      13,    22],
    [    1,      -2,     0],
    [    1,      -3,     0],
]


@pytest.mark.parametrize("dice,bonus,expected_avg", critical_damage_cases)
def test_damage_with_critical_hit(dice, bonus, expected_avg):
    dmg = Damage(dice=dice, bonus=bonus)
    assert dmg.critical().avg() == expected_avg


critical_power_cases = [
    # dice    bonus    avg
    [    0,       0,    10],
    [    1,       0,    12],
    [    1,       2,    14],
    [    0,       2,    12],
    [  4.5,      13,    32],
    [    1,      -1,    11],
    [    1,      -2,    10],
    [    1,     -10,     2],
    [    1,     -11,     1],
    [    1,     -12,     0],
    [    1,     -13,     0],
]


@pytest.mark.parametrize("dice,bonus,expected_avg", critical_power_cases)
def test_damage_with_critical_hit_and_power_attack(dice, bonus, expected_avg):
    dmg = Damage(dice=dice, bonus=bonus)
    assert dmg.critical().power().avg() == expected_avg
    assert dmg.power().critical().avg() == expected_avg
