from abc import *
from enum import Enum


class IndicatorType(Enum):
    MACD = 1
    ADX = 2


class IndicatorValue:

    def __init__(self, value, material=None):
        self.value = value
        self.material = material


class Indicator(ABC):

    def __init__(self, is_test=False):
        self.is_test = is_test

    @abstractmethod
    def get(self, df):
        raise NotImplementedError()


class IndicatorBuilder:
    def __init__(self):
        self.indicators = {}

    def add(self, indicator_type, value):
        try:
            key = IndicatorType[indicator_type].name
            self.indicators[key] = value
        except KeyError as e:
            print(e)

    def build(self):
        return self.indicators
