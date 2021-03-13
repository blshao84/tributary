import tributary.lazy as tl
from priceable import Priceable


class Payoff:
    pass


class PayoffModel:
    def payoff(self, param: tl.Node) -> tl.Node:  # Priceable->Payoff
        pass
