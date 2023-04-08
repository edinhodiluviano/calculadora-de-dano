import fastapi


app = fastapi.FastAPI()


@app.get("/ping2")
def ping2():
    return "pong"


class Damage:
    def __init__(self, dice, bonus):
        self.dice = dice
        self.bonus = bonus

    def avg(self):
        return max(self.dice + self.bonus, 0)

    def critical(self):
        return self.__class__(self.dice * 2, self.bonus)

    def power(self):
        return self.__class__(self.dice, self.bonus + 10)

    def to_dict(self):
        return dict(
            simple=self.avg(),
            power=self.power().avg(),
            critical=self.critical().avg(),
            power_critical=self.power().critical().avg(),
        )


class AttackProbability:
    def __init__(self, ca, bonus, crit):
        self.ca = ca
        self.bonus = bonus
        self.crit = crit
        self.effective_ca = ca - bonus

    def _n_miss(self):
        return min(max(self.effective_ca - 1, 1), 19)

    def _n_hit(self):
        return max(self.crit - self._n_miss() - 1, 0)

    def _n_crit(self):
        return 20 - self._n_miss() - self._n_hit()

    def miss(self):
        return round(self._n_miss() * 0.05, 4)

    def hit(self):
        return round(self._n_hit() * 0.05, 4)

    def critical(self):
        return round(self._n_crit() * 0.05, 4)
