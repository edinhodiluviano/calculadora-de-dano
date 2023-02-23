import bisect
import itertools
import random
from abc import ABC, abstractmethod
from dataclasses import dataclass
from fractions import Fraction


@dataclass
class Distribution:
    values: list[int]
    probabilities: list[Fraction]

    def __post_init__(self):
        if sum(self.probabilities) != 1:
            raise ValueError("Probabilities should sum up to 1.")

    @classmethod
    def uniform(cls, values):
        n = len(values)
        return cls(
            values=values, probabilities=[Fraction(1, n) for _ in range(n)]
        )

    @property
    def weights(self):
        return list(itertools.accumulate(self.probabilities))

    def __add__(self, other):
        if isinstance(other, (int, float, Fraction)):
            new_values = [v + other for v in self.values]
            return self.__class__(
                values=new_values, probabilities=self.probabilities
            )

        elif isinstance(other, self.__class__):
            new_values = [
                v[0] + v[1]
                for v
                in itertools.product(self.values, other.values)
            ]
            new_probs = [
                p[0] * p[1]
                for p
                in itertools.product(self.probabilities, other.probabilities)
            ]
            d = {}
            for val, p in zip(new_values, new_probs):
                if val not in d:
                    d[val] = 0
                d[val] += p
            return self.__class__(
                values=list(d.keys()), probabilities=list(d.values()),
            )
        else:
            raise TypeError

    def __radd__(self, other):
        return self.__add__(other)

    def __mul__(self, other):
        if isinstance(other, int):
            if other == 0:
                return self.__class__(values=[0], probabilities=[1])
            r = sum(self for _ in range(abs(other)))
            if other < 0:
                r.values = [-v for v in r.values]
                r.values.reverse()
                r.probabilities.reverse()
            return r
        else:
            raise TypeError

    def inverse(self, x: (int, float, Fraction)) -> int:
        index = bisect.bisect_left(self.weights, x)
        return self.values[index]

    def random(self, seeded_random: random.Random = None):
        if seeded_random is None:
            seeded_random = random
        x = seeded_random.random()
        y = self.inverse(x=x)
        return y


class BaseDie(ABC):
    @abstractmethod
    def from_string(cls, s):
        ...

    @abstractmethod
    def __add__(self, other):
        ...

    @abstractmethod
    def __multiply__(self, other):
        ...


@dataclass
class Die(BaseDie):
    ...


@dataclass
class Bonus(BaseDie):
    ...
