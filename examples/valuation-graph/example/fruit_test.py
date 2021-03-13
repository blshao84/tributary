from datetime import date, timedelta

from example.fruit import Apple
from example.fruit_valuation import FruitPVRM
from priceable import Priceable

if __name__ == '__main__':
    d1 = date.today() + timedelta(10)
    pvrm = FruitPVRM()
    apple1: Priceable = Apple("a1", 3.2, d1, "U.S")
    pv_graph = pvrm.present_value(apple1)
    pv = pv_graph()
    pv_graph.graphviz().view()
    print(pv.value)

