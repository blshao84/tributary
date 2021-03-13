from datetime import date

from example.fruit_market import ListedFruitInstrument
from payoff import Payoff
from priceable import Priceable


class FruitPayoff(Payoff):
    def __init__(self, weight: float, delivery_date: date, instrument: ListedFruitInstrument):
        self.weight = weight
        self.delivery_date = delivery_date
        self.instrument = instrument


class Fruit(Priceable):
    def __init__(self, name: str, weight: float, delivery_date: date):
        self.name = name
        self.weight = weight
        self.delivery_date = delivery_date


class Apple(Fruit):
    def __init__(self, name: str, weight: float, delivery_date: date, country: str):
        Fruit.__init__(self, "Apple", weight, delivery_date)
        self.country = country
        self.pvrm_key = "FRUIT_PVRM"
