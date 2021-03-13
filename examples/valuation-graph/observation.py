class Observable:
    def __init__(self, name: str):
        self.name = name


class ObservableSource:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description


class Observation:
    def __init__(self, observable: Observable, source: ObservableSource, value: float, unit: str):
        self.observable = observable
        self.source = source
        self.value = value
        self.unit = unit


Bloomberg = ObservableSource("Bloomberg", "Bloomberg")
