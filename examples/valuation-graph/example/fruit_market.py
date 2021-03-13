from typing import List, Tuple

from market_model import MarketState
from observation import Observable, Observation, ObservableSource, Bloomberg
import tributary.lazy as tl


class ListedFruitInstrument(Observable):
    def __init__(self, market: str, product: str):
        self.market = market
        self.product = product

    def key(self):
        return self.market, self.product


class FruitObservation(Observation):
    def __init__(self, instrument: ListedFruitInstrument, source: ObservableSource, price: float):
        self.observable = instrument
        self.price = price
        self.unit = "price"
        self.source = source
        self.value = price


class FruitMarketState(MarketState):
    def __init__(self, market: str, observations):
        self.market = market
        self.observations = observations


AmericanOrange = ListedFruitInstrument("U.S", "Orange")
ChinaApple = ListedFruitInstrument("China", "Apple")

FruitInstrumentRepo = [
    AmericanOrange, ChinaApple
]

FruitObservationRepo = [
    FruitObservation(AmericanOrange, Bloomberg, 11.2),
    FruitObservation(ChinaApple, Bloomberg, 4.2),
    FruitObservation(ChinaApple, Bloomberg, 5.8)
]
