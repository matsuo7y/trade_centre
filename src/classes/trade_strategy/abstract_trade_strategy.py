from abc import *


class AbstractTradeStrategy(ABC):

    def __init__(self, is_test=False):
        self.is_test = is_test

    @abstractmethod
    def get_indicators(self):
        raise NotImplementedError()

    @abstractmethod
    def should_make_long_order(self, indicator_value):
        raise NotImplementedError()

    @abstractmethod
    def should_make_short_order(self, indicator_value):
        raise NotImplementedError()

    @abstractmethod
    def should_take_profit_long_order(self, indicator_value):
        raise NotImplementedError()

    @abstractmethod
    def should_take_profit_short_order(self, indicator_value):
        raise NotImplementedError()
