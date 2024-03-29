from typing import Annotated

import fastapi
from fastapi import Query
from pydantic import BaseModel


app = fastapi.FastAPI()


@app.get("/ping2")
def ping2():
    return "pong"


class Attack:
    def __init__(
        self, att_bonus: int, dmg_bonus: int, dmg_dice: float, crit: int
    ):
        self.att_bonus = att_bonus
        self.dmg_bonus = dmg_bonus
        self.dmg_dice = dmg_dice
        self.crit = crit

    def power(self) -> "Attack":
        return self.__class__(
            att_bonus=self.att_bonus - 5,
            dmg_bonus=self.dmg_bonus + 10,
            dmg_dice=self.dmg_dice,
            crit=self.crit,
        )

    def damage(self) -> float:
        return max(self.dmg_dice + self.dmg_bonus, 0)

    def critical(self) -> float:
        return max(self.dmg_dice * 2 + self.dmg_bonus, 0)


class AttackProbability:
    def __init__(self, ac: int, attack: Attack):
        self.ac = ac
        self.attack = attack
        self.effective_ac = ac - attack.att_bonus

    def _n_miss(self):
        return min(max(self.effective_ac - 1, 1), 19)

    def _n_hit(self):
        return max(self.attack.crit - self._n_miss() - 1, 0)

    def _n_crit(self):
        return 20 - self._n_miss() - self._n_hit()

    def miss(self):
        return round(self._n_miss() * 0.05, 4)

    def hit(self):
        return round(self._n_hit() * 0.05, 4)

    def critical(self):
        return round(self._n_crit() * 0.05, 4)

    def damage(self):
        dmg = (
            self.attack.damage() * self.hit()
            + self.attack.critical() * self.critical()
        )
        return round(dmg, 4)

    def power(self):
        return self.__class__(ac=self.ac, attack=self.attack.power())


class Damage(BaseModel):
    simple: float
    power: float

    @classmethod
    def from_attack(cls, attack: AttackProbability):
        simple_dmg = attack.damage()
        power_dmg = attack.power().damage()
        return cls(simple=simple_dmg, power=power_dmg)


@app.get("/average_damage")
def get_average_damage(
    ac: Annotated[int, Query(ge=0, le=40)],
    att_bonus: Annotated[int, Query(ge=-5, le=50)],
    dmg_dice: Annotated[float, Query(ge=-10, le=100)],
    dmg_bonus: Annotated[float, Query(ge=-5, le=100)],
    crit: Annotated[int, Query(ge=1, le=20)] = 20,
):
    att = Attack(
        att_bonus=att_bonus, dmg_dice=dmg_dice, dmg_bonus=dmg_bonus, crit=crit
    )
    att_probs = AttackProbability(attack=att, ac=ac)
    damage = Damage.from_attack(attack=att_probs)
    return {"damage": damage.dict()}


@app.get("/damage_curve")
def get_damage_curve(
    ac_min: int,
    ac_max: int,
    att_bonus: int,
    dmg_dice: float,
    dmg_bonus: float,
    crit: int = 20,
):
    att = Attack(
        att_bonus=att_bonus, dmg_dice=dmg_dice, dmg_bonus=dmg_bonus, crit=crit
    )

    def _calc_damage(ac):
        return Damage.from_attack(attack=AttackProbability(attack=att, ac=ac))

    damage_curve = {
        ac: _calc_damage(ac=ac) for ac in range(ac_min, ac_max + 1)
    }
    return {"damage_curve": damage_curve}
