from datetime import date

import tributary.lazy as tl
from example.fruit import Fruit, FruitPayoff
from example.fruit_market import FruitMarketState, FruitInstrumentRepo, FruitObservationRepo
from example.fruit_model import FruitMarketModel, CurveMarketModelConfiguration, FruitCalibratedMarketModel
from payoff import PayoffModel
from present_value import PresentValue
from priceable import Priceable
from pvrm import PVRMManager
from valuation import PricingAlgorithm, ValuationModel


class FruitPayoffModel(PayoffModel):
    def load_instrument(self, param: tl.Node):
        fruit = param()
        filtered = list(filter(lambda i: i.product == fruit.name, FruitInstrumentRepo))
        print(f"find instrument {filtered}")
        return FruitPayoff(fruit.weight, fruit.delivery_date, filtered[0])

    def payoff(self, param: Fruit) -> tl.Node:
        return tl.Node(name="fruit_payoff", callable=self.load_instrument, callable_kwargs={"param": param})


class FruitPricingAlgorithm(PricingAlgorithm):
    def present_value(self,
                      payoff: FruitPayoff,
                      cmm: FruitCalibratedMarketModel
                      ) -> PresentValue:
        # print("evaluating payoff from pricing algo")
        po = payoff
        # print("evaluating cmm from pricing algo")
        fruit_cmm = cmm
        all_marks = fruit_cmm.market_prices()
        instrument = po.instrument
        key = instrument.key()
        print(f"key={key}, all_marks={all_marks}")
        unit_price = all_marks.get(key)
        discount_curve = fruit_cmm.discount_curve()
        if unit_price is not None:
            value = unit_price * po.weight * discount_curve.discount_factor(po.delivery_date)
            return PresentValue(value, "CNY")
        else:
            raise RuntimeError(f"pricing failure due to missing market instrument ${instrument.product}")


class FruitValuationModel(ValuationModel):
    def __init__(self, priceable: Priceable, valuation_date: date):
        self.priceable = priceable
        self.valuation_date = valuation_date

    def region(self) -> tl.Node:
        return tl.Node(name="region", value="China")

    def market_model(self) -> tl.Node:  # FruitMarketModel
        curve_config = CurveMarketModelConfiguration(self.valuation_date)
        mm = FruitMarketModel(curve_config)
        return tl.Node(name="fruit_market_model", value=mm)

    def market_state(self) -> tl.Node:  # FruitMarketState
        region_node = self.region()
        observations: tl.Node = self.fruit_observations(region_node)
        return tl.Node(name="fruit_market_state",
                       callable=lambda obs, r: FruitMarketState(r(), obs()),
                       callable_kwargs={"obs": observations, "r": region_node})

    def fruit_observations(self, fruit_region: tl.Node) -> tl.Node:
        return tl.Node(name="fruit_observations",
                       callable=lambda r: list(filter(lambda observation: observation.observable.market == r(),
                                                      FruitObservationRepo)),
                       callable_kwargs={"r": fruit_region})

    def payoff_model(self) -> tl.Node:  # FruitPayoffModel
        pm = FruitPayoffModel()
        return tl.Node(name="fruit_payoff_model", value=pm)

    def pricing_algorithm(self) -> tl.Node:  # PricingAlgorithm
        pa = FruitPricingAlgorithm()
        return tl.Node(name="fruit_pricing_algo", value=pa)


class FruitPVRM(PVRMManager):
    def valuation_model(self, priceable):
        config_node = self.pvrm_configuration()
        print("evaluating pvrm config node")
        config = config_node()
        return FruitValuationModel(priceable, config.pricing_date)
