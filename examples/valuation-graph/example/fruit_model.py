from datetime import date
from typing import Dict, Tuple

import tributary.lazy as tl
from example.fruit_market import FruitMarketState
from market_model import CalibratedMarketModel, MarketState, MarketModel, MarketModelConfiguration


class CurveMarketState(MarketState):
    def __init__(self, name: str):
        self.name = name

    def observations(self) -> tl.Node:
        return tl.Node(name="curve_observations", value=[])


class CurveMarketModelConfiguration(MarketModelConfiguration):
    def __init__(self, curve_starting_date: date):
        self.curve_starting_date = curve_starting_date


class CurveMarketModel(MarketModel):
    def __init__(self, config: CurveMarketModelConfiguration):
        self.config = config

    def market_model_configuration(self) -> tl.Node:
        return tl.Node(name="curve_market_model_configuration", value=self.config)

    def calibrate(self, market_state: tl.Node) -> tl.Node:
        config = self.market_model_configuration()
        return tl.Node(name="curve_calibrated_market_model",
                       callable=self.do_calibrate,
                       callable_kwargs={"ms": market_state, "mc": config})

    def do_calibrate(self, ms: tl.Node, mc: tl.Node) -> tl.Node:
        print("evaluating node curve_market_state")
        curve_ms = ms()
        print("evaluating node curve_market_model_config")
        config = mc()
        return DiscountCurveCalibratedMarketModel(curve_ms, config.curve_starting_date)


class DiscountCurveCalibratedMarketModel(CalibratedMarketModel):
    def __init__(self, curve_market: CurveMarketState, curve_starting_date: date):
        self.curve_market = curve_market
        self.curve_starting_date = curve_starting_date

    def market_state(self) -> MarketState:
        return self.curve_market

    def discount_factor(self, discount_date: date):
        days = (discount_date - self.curve_starting_date).days
        if days <= 0:
            return 1.0
        else:
            return 1 / days


class FruitCalibratedMarketModel(CalibratedMarketModel):
    def __init__(self, curve_model: DiscountCurveCalibratedMarketModel, fruit_market: FruitMarketState):
        self.curve_model = curve_model
        self.fruit_market = fruit_market

    def market_state(self) -> FruitMarketState:
        return self.fruit_market

    def discount_curve(self) -> DiscountCurveCalibratedMarketModel:
        return self.curve_model

    def market_prices(self) -> Dict[Tuple[str, str], float]:
        ms = self.fruit_market
        print("evaluating fruit observations")
        obs = ms.observations
        return dict(map(lambda o: (o.observable.key(), o.value), obs))


class FruitMarketModel(MarketModel):
    def __init__(self, curve_config: CurveMarketModelConfiguration):
        self.curve_config = curve_config

    def market_model_configuration(self) -> tl.Node:
        return tl.Node(name="fruit_market_model_config", value=self.curve_config)

    def calibrate(self, market_state: tl.Node) -> tl.Node:
        curve_model = CurveMarketModel(self.curve_config)
        curve_market = tl.Node(name="curve_market_state", value=CurveMarketState("stupid discount curve"))
        curve_cmm_node = curve_model.calibrate(curve_market)
        return tl.Node(name="fruit_market_model_calibrate", callable=self.do_calibrate,
                       callable_kwargs={"fruit_ms": market_state, "curve_cmm": curve_cmm_node})

    def do_calibrate(self, fruit_ms: tl.Node, curve_cmm: tl.Node):
        print("evaluating fruit market state")
        fr_ms = fruit_ms()
        print("evaluating curve cmm")
        crv_cmm = curve_cmm()
        return FruitCalibratedMarketModel(crv_cmm, fr_ms)
