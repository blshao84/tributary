from datetime import date

import tributary.lazy as tl
from present_value import PresentValue
from priceable import Priceable


class PricingAlgorithm:
    def present_value(self, payoff: tl.Node, cmm: tl.Node) -> PresentValue:
        pass


class ValuationModel:
    def __init__(self, priceable: Priceable, valuation_date: date):
        self.priceable = priceable

    def market_model(self) -> tl.Node:
        pass

    def market_state(self) -> tl.Node:
        pass

    def payoff_model(self) -> tl.Node:
        pass

    def pricing_algorithm(self) -> tl.Node:
        pass

    def payoff(self) -> tl.Node:
        pm: tl.Node = self.payoff_model()
        return tl.Node(name="payoff",
                       callable=lambda pm, p: pm().payoff(p),
                       callable_kwargs={"pm": pm, "p": self.priceable})

    def calibrated_market_model(self) -> tl.Node:
        mm_node: tl.Node = self.market_model()
        ms_node: tl.Node = self.market_state()
        return tl.Node(name="market_model_calibrate",
                       callable=lambda mm, ms: mm().calibrate(ms),
                       callable_kwargs={"mm": mm_node, "ms": ms_node})

    def present_value(self) -> tl.Node:
        po_node: tl.Node = self.payoff()
        cmm_node: tl.Node = self.calibrated_market_model()
        pa_node: tl.Node = self.pricing_algorithm()
        return tl.Node(name="present_value",
                       callable=lambda pa, po, cmm: pa().present_value(po(), cmm()),
                       callable_kwargs={"pa": pa_node, "po": po_node, "cmm": cmm_node})

    def measure_map(self) -> tl.Node:
        pass
