import math
import random
from fractions import Fraction as F

import pytest

from service import dice


def test_should_always_pass():
    ...


def test_when_init_distribution_then_return_distribution_instance():
    distribution = dice.Distribution(values=[1], probabilities=[1])
    assert isinstance(distribution, dice.Distribution)


def test_when_init_dist_with_incorrect_probs_then_raise_value_error():
    with pytest.raises(ValueError):
        dice.Distribution(values=[1], probabilities=[0.5])


def test_when_add_distribution_with_int_then_returns_distribution():
    distribution = dice.Distribution(values=[1], probabilities=[1])
    distribution2 = distribution + 1
    assert isinstance(distribution2, dice.Distribution)


def test_when_add_distribution_with_float_then_returns_distribution():
    distribution = dice.Distribution(values=[1], probabilities=[1])
    distribution2 = distribution + 1.5
    assert isinstance(distribution2, dice.Distribution)


def test_when_add_distribution_with_fraction_then_returns_distribution():
    distribution = dice.Distribution(values=[1], probabilities=[1])
    distribution2 = distribution + F(1, 2)
    assert isinstance(distribution2, dice.Distribution)


def test_when_add_distribution_then_return_values_added():
    distribution = dice.Distribution(values=[1], probabilities=[1])
    distribution2 = distribution + 1.5
    assert distribution2.values == [2.5]


def test_when_add_distribution_then_probabilities_are_equal():
    distribution = dice.Distribution(values=[1], probabilities=[1])
    distribution2 = distribution + 1.5
    assert distribution2.weights == distribution.weights


def test_when_add_distribution_to_other_then_returns_distribution():
    dist1 = dice.Distribution(values=[1], probabilities=[1])
    dist2 = dice.Distribution(values=[1, 2], probabilities=[F(1, 2), F(1, 2)])
    dist3 = dist1 + dist2
    assert isinstance(dist3, dice.Distribution)


def test_when_add_dist_to_other_then_returns_dist_with_correct_values():
    dist1 = dice.Distribution(values=[1, 2], probabilities=[F(1, 2), F(1, 2)])
    dist2 = dice.Distribution(
        values=[3, 4, 5], probabilities=[F(1, 3), F(1, 3), F(1, 3)]
    )
    dist3 = dist1 + dist2
    assert dist3.values == [4, 5, 6, 7]


def test_add_dist_to_other_then_returns_dist_with_correct_probabilities():
    dist1 = dice.Distribution(values=[1, 2], probabilities=[F(1, 2), F(1, 2)])
    dist2 = dice.Distribution(
        values=[3, 4, 5], probabilities=[F(1, 3), F(1, 3), F(1, 3)]
    )
    dist3 = dist1 + dist2
    assert dist3.probabilities == [F(1, 6), F(2, 6), F(2, 6), F(1, 6)]


def test_add_order_dont_matter():
    dist1 = dice.Distribution(values=[1, 2], probabilities=[F(1, 2), F(1, 2)])
    dist2 = dice.Distribution(
        values=[3, 4, 5], probabilities=[F(1, 3), F(1, 3), F(1, 3)]
    )
    assert dist1 + dist2 == dist2 + dist1


def test_weights():
    dist = dice.Distribution(
        values=list(range(5)),
        probabilities=[F(1, 11), F(1, 11), F(2, 11), F(3, 11), F(4, 11)],
    )
    assert dist.weights == [F(1, 11), F(2, 11), F(4, 11), F(7, 11), F(11, 11)]


def test_when_init_uniform_dist_then_return_dist_instance():
    dist = dice.Distribution.uniform([1, 2, 3, 4])
    assert isinstance(dist, dice.Distribution)


def test_when_init_uniform_dist_then_probabilities_are_correct():
    dist = dice.Distribution.uniform([1, 2, 3, 4])
    assert dist.probabilities == [F(1, 4), F(1, 4), F(1, 4), F(1, 4)]


def test_when_init_uniform_and_get_zero_prob_then_return_correct_value():
    dist = dice.Distribution.uniform([1, 2, 3, 4])
    assert dist.inverse(0) == 1


def test_when_init_uniform_and_get_one_prob_then_return_correct_value():
    dist = dice.Distribution.uniform([1, 2, 3, 4])
    assert dist.inverse(1) == 4


def test_when_init_uniform_and_get_trivial_prob_then_return_correct_value():
    dist = dice.Distribution.uniform([1, 2, 3, 4])
    assert dist.inverse(0.4) == 2


def test_when_init_uniform_and_get_limit_prob_then_return_correct_value():
    dist = dice.Distribution.uniform([1, 2, 3, 4])
    assert dist.inverse(0.5) == 2


def test_when_init_uniform_and_get_random_then_return_second_element():
    dist = dice.Distribution.uniform([11, 12, 13, 14, 15, 16, 17, 18, 19, 20])
    # random.Random(1).random() == 0.13
    assert dist.random(seeded_random=random.Random(1)) == 12


def test_when_multiply_by_0_then_return_single_value():
    dist = dice.Distribution.uniform([1, 2, 3, 4, 5, 6])
    dist2 = dist * 0
    assert dist2.values == [0]
    assert dist2.probabilities == [1]


def test_when_multiply_uniform_by_int_then_return_correct_values():
    dist = dice.Distribution.uniform([1, 2, 3, 4, 5, 6])
    dist2 = dist * 3
    assert dist2.values == list(range(3, 19))


def test_when_multiply_uniform_by_int_then_return_correct_probabilities():
    dist = dice.Distribution.uniform([1, 2, 3, 4, 5, 6])
    dist2 = dist * 3
    expected = [
        F(1, 216),
        F(3, 216),
        F(6, 216),
        F(10, 216),
        F(15, 216),
        F(21, 216),
        F(25, 216),
        F(27, 216),
        F(27, 216),
        F(25, 216),
        F(21, 216),
        F(15, 216),
        F(10, 216),
        F(6, 216),
        F(3, 216),
        F(1, 216),
    ]
    assert dist2.probabilities == expected


def test_then_multiply_by_negative_then_return_correct_values():
    dist = dice.Distribution.uniform([1, 2, 3, 4, 5, 6])
    dist2 = dist * -3
    assert dist2.values == [-i for i in range(3, 19)][::-1]


def test_when_multiply_by_negative_int_then_return_correct_probabilities():
    dist = dice.Distribution.uniform([1, 2, 3, 4])
    dist2 = dist * - 3
    expected = [
        F(1, 64),
        F(3, 64),
        F(6, 64),
        F(10, 64),
        F(12, 64),
        F(12, 64),
        F(10, 64),
        F(6, 64),
        F(3, 64),
        F(1, 64),
    ]
    assert dist2.probabilities == expected
