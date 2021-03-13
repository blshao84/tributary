import tributary.lazy as tl
from priceable import Priceable


class MarketState:
    def __init__(self, name: str):
        self.name = name

    def observations(self) -> tl.Node:  # List[Observation]
        pass


class CalibratedMarketModel:
    def measure_map(self, priceable: Priceable) -> tl.Node:
        pass


class MarketModelConfiguration:
    pass


class MarketModel:
    def market_model_configuration(self) -> tl.Node:
        pass

    def calibrate(self, market_state: tl.Node) -> tl.Node:
        pass
