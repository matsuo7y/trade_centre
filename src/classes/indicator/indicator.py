from abc import *
from enum import Enum


class IndicatorType(Enum):
    CANDLE = 1
    MACD = 2
    ADX = 3


class IndicatorValue:

    def __init__(self, value, material=None):
        self.value = value
        self.material = material


class AbstractIndicator(ABC):

    def __init__(self, is_test=False):
        self.is_test = is_test

    @abstractmethod
    def get(self, df):
        raise NotImplementedError()


class Indicators:

    def __init__(self, contents):
        self.contents = contents

    def get_values(self, df):
        indicator_value_builder = IndicatorTypeDictBuilder()
        for indicator_type, indicator in self.contents.items():
            indicator_value_builder.add(indicator_type, indicator.get(df))
        return indicator_value_builder.build()


class IndicatorTypeDictBuilder:
    def __init__(self):
        self.contents = {}

    def add(self, indicator_type, value):
        try:
            key = IndicatorType[indicator_type].name
            self.contents[key] = value
        except KeyError as e:
            print(e)

    def build(self):
        return self.contents


class IndicatorsBuilder(IndicatorTypeDictBuilder):
    def __init__(self):
        super().__init__()

    def build(self):
        return Indicators(super().build())
