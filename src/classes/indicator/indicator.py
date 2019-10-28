from abc import *


class IndicatorValue:

    def __init__(self, value, material=None):
        self.value = value
        self.material = material


class Indicator(ABC):

    @abstractmethod
    def get(self, df):
        raise NotImplementedError()
