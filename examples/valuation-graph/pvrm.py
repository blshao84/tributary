from datetime import date

import tributary.lazy as tl
from priceable import Priceable
from valuation import ValuationModel


class PVRMManager:
    def pvrm_configuration(self) -> tl.Node:
        default_pvrm_config = PVRMConfiguration(date.today())
        return tl.Node(name="pvrm_config", value=default_pvrm_config)

    def valuation_model(self, priceable: Priceable) -> ValuationModel:
        pass

    def present_value(self, priceable: Priceable) -> tl.Node:
        vm: ValuationModel = self.valuation_model(priceable)
        return vm.present_value()


class PVRMConfiguration:
    def __init__(self, pricing_date: date):
        self.pricing_date = pricing_date


# class PVRMKey(Enum):
#     FRUIT_PVRM = "fruit_pvrm"
#
#
# class PVRM:
#     @staticmethod
#     def pvrm_map():
#         pm = {
#             PVRMKey.FRUIT_PVRM: FruitPVRM()
#         }
#         return pm
#
#     @staticmethod
#     def pvrm(priceable: Priceable) -> PVRMManager:
#         return PVRM.pvrm_map()(priceable.pvrm_key)
