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
