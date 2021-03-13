import functools
from typing import List, Dict, Tuple, Callable

from present_value import PresentValue
from priceable import Priceable


class MeasureDefinition:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description


class Measure:
    def __init__(self, identifier: str, definition: MeasureDefinition):
        self.identifier = identifier
        self.definition = definition

#
# class RiskMeasure(Measure):
#     def scenarios(self) -> List[Scenario]:
#         return []
#
#     def value(self, priceable: Priceable):
#         return priceable.present_value()
#
#     def transform(self, result_map: Dict[str, PresentValue]):
#         pass
#
#     def calculate(self, priceable: Priceable) -> PresentValue:
#         scen_calc = functools.partial(self.__calc_one, priceable=priceable)
#         result = dict(scen_calc(scen) for scen in self.scenarios())
#         return self.transform(result)
#
#     def __calc_one(self, scenario: Scenario, priceable: Priceable) -> Tuple[str, PresentValue]:
#         return scenario.name, self.value(priceable)
#
#
# class MeasureEntry:
#     def __init__(self, measure_identifier: str, measure_lambda: Callable[[], RiskMeasure]):
#         self.measure_identifier = measure_identifier
#         self.measure_lambda = measure_lambda
#
#
# class MeasureMap:
#     @staticmethod
#     def empty():
#         return MeasureMap(dict())
#
#     def __init__(self, measure_map: Dict[MeasureDefinition, List[MeasureEntry]]):
#         self.measure_map = measure_map
#
#     def register(self, definition, entry):
#         existing_measures = self.measure_map.get(definition)
#         if existing_measures is None:
#             self.measure_map.update({definition: [entry]})
#         else:
#             duplicate_entry = filter(lambda e: e.measure_identifier == entry.measure_identifier, existing_measures)
#             if len(duplicate_entry) != 0:
#                 raise RuntimeError(f"duplicate measure for ${definition}:${entry.measure_identifier}")
#             new_measures = existing_measures.append(entry)
#             self.measure_map.update({definition: new_measures})
#
#     def find(self, definition):
#         existing_measures = self.measure_map.get(definition)
#         if existing_measures is None:
#             []
#         else:
#             existing_measures
#
#     def measure(self, definition: MeasureDefinition, identifier: str) -> RiskMeasure:
#         existing_measures = self.measure_map.get(definition)
#         if existing_measures is None:
#             raise RuntimeError(f"measure definition is not defined: ${definition}")
#         measures = filter(lambda e: e.measure_identifier == identifier, existing_measures)
#         measure_count = len(measures)
#         if measure_count == 0:
#             raise RuntimeError(f"measure identifier ${identifier} is not defined for ${definition}")
#         elif measure_count == 1:
#             return measures[0].measure_lambda()
#         else:
#             raise RuntimeError(f"find duplicate measures for ${definition}")
