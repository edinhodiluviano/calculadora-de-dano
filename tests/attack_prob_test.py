import pytest

from service.main import Attack, AttackProbability


cases = [
    #  ac   bonus    crit  n_miss   n_hit  n_crit
    [  10,      0,     20,      9,     10,      1],  # NOQA: BLK100
    [  11,      1,     20,      9,     10,      1],
    [  11,      0,     20,     10,      9,      1],
    [   1,      0,     20,      1,     18,      1],
    [   0,      0,     20,      1,     18,      1],
    [   0,      1,     20,      1,     18,      1],
    [  -1,      0,     20,      1,     18,      1],  # NOQA: E221
    [  18,      0,     20,     17,      2,      1],
    [  19,      0,     20,     18,      1,      1],
    [  20,      0,     20,     19,      0,      1],
    [  21,      0,     20,     19,      0,      1],
    [  18,      1,     20,     16,      3,      1],
    [  19,      1,     20,     17,      2,      1],
    [  20,      1,     20,     18,      1,      1],
    [  21,      1,     20,     19,      0,      1],
    [  10,      0,     19,      9,      9,      2],
    [  11,      1,     19,      9,      9,      2],
    [  11,      0,     19,     10,      8,      2],
    [   1,      0,     19,      1,     17,      2],
    [   0,      0,     19,      1,     17,      2],
    [   0,      1,     19,      1,     17,      2],
    [  -1,      0,     19,      1,     17,      2],  # NOQA: E221
    [  18,      0,     19,     17,      1,      2],
    [  19,      0,     19,     18,      0,      2],
    [  20,      0,     19,     19,      0,      1],
    [  21,      0,     19,     19,      0,      1],
    [  18,      1,     19,     16,      2,      2],
    [  19,      1,     19,     17,      1,      2],
    [  20,      1,     19,     18,      0,      2],
    [  21,      1,     19,     19,      0,      1],
    [  22,      1,     19,     19,      0,      1],
]


@pytest.mark.parametrize("ac,bonus,crit,n_miss,n_hit,n_crit", cases)
def test_miss_prob(ac, bonus, crit, n_miss, n_hit, n_crit):
    expected_miss_prob = round(n_miss * 0.05, 4)
    att = Attack(att_bonus=bonus, crit=crit, dmg_dice=0, dmg_bonus=0)
    att_prob = AttackProbability(ac=ac, attack=att)
    assert att_prob.miss() == expected_miss_prob


@pytest.mark.parametrize("ac,bonus,crit,n_miss,n_hit,n_crit", cases)
def test_hit_prob(ac, bonus, crit, n_miss, n_hit, n_crit):
    expected_hit_prob = round(n_hit * 0.05, 4)
    att = Attack(att_bonus=bonus, crit=crit, dmg_dice=0, dmg_bonus=0)
    att_prob = AttackProbability(ac=ac, attack=att)
    assert att_prob.hit() == expected_hit_prob


@pytest.mark.parametrize("ac,bonus,crit,n_miss,n_hit,n_crit", cases)
def test_crit_prob(ac, bonus, crit, n_miss, n_hit, n_crit):
    expected_crit_prob = round(n_crit * 0.05, 4)
    att = Attack(att_bonus=bonus, crit=crit, dmg_dice=0, dmg_bonus=0)
    att_prob = AttackProbability(ac=ac, attack=att)
    assert att_prob.critical() == expected_crit_prob
