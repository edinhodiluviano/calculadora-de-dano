import pytest

from service.main import Damage


simple_cases = [
    # dice    bonus    avg
    [    0,       0,     0],  # NOQA E201
    [    1,       0,     1],  # NOQA E201
    [    1,       2,     3],  # NOQA E201
    [    0,       2,     2],  # NOQA E201
    [  4.5,      13,  17.5],  # NOQA E201
    [    1,      -1,     0],  # NOQA E201
    [    1,      -2,     0],  # NOQA E201
]


@pytest.mark.parametrize("dice,bonus,expected_avg", simple_cases)
def test_simple_cases(dice, bonus, expected_avg):
    dmg = Damage(dice=dice, bonus=bonus)
    assert dmg.avg() == expected_avg


power_attack_cases = [
    # dice    bonus    avg
    [    0,       0,    10],  # NOQA E201
    [    1,       0,    11],  # NOQA E201
    [    1,       2,    13],  # NOQA E201
    [    0,       2,    12],  # NOQA E201
    [  4.5,      13,  27.5],  # NOQA E201
    [    1,      -1,    10],  # NOQA E201
    [    1,      -2,     9],  # NOQA E201
    [    1,     -10,     1],  # NOQA E201
    [    1,     -11,     0],  # NOQA E201
    [    1,     -12,     0],  # NOQA E201
]


@pytest.mark.parametrize("dice,bonus,expected_avg", power_attack_cases)
def test_damage_with_power_attack(dice, bonus, expected_avg):
    dmg = Damage(dice=dice, bonus=bonus)
    assert dmg.power().avg() == expected_avg


critical_damage_cases = [
    # dice    bonus    avg
    [    0,       0,     0],  # NOQA E201
    [    1,       0,     2],  # NOQA E201
    [    1,       2,     4],  # NOQA E201
    [    0,       2,     2],  # NOQA E201
    [  4.5,      13,    22],  # NOQA E201
    [    1,      -2,     0],  # NOQA E201
    [    1,      -3,     0],  # NOQA E201
]


@pytest.mark.parametrize("dice,bonus,expected_avg", critical_damage_cases)
def test_damage_with_critical_hit(dice, bonus, expected_avg):
    dmg = Damage(dice=dice, bonus=bonus)
    assert dmg.critical().avg() == expected_avg


critical_power_cases = [
    # dice    bonus    avg
    [    0,       0,    10],  # NOQA E201
    [    1,       0,    12],  # NOQA E201
    [    1,       2,    14],  # NOQA E201
    [    0,       2,    12],  # NOQA E201
    [  4.5,      13,    32],  # NOQA E201
    [    1,      -1,    11],  # NOQA E201
    [    1,      -2,    10],  # NOQA E201
    [    1,     -10,     2],  # NOQA E201
    [    1,     -11,     1],  # NOQA E201
    [    1,     -12,     0],  # NOQA E201
    [    1,     -13,     0],  # NOQA E201
]


@pytest.mark.parametrize("dice,bonus,expected_avg", critical_power_cases)
def test_damage_with_critical_hit_and_power_attack(dice, bonus, expected_avg):
    dmg = Damage(dice=dice, bonus=bonus)
    assert dmg.critical().power().avg() == expected_avg
    assert dmg.power().critical().avg() == expected_avg
