from abc import *
from ..indicator import IndicatorsBuilder, IndicatorType, CandleIndicator
from ..progress_recorder import CandleRecorder, PositionRecorder


class AbstractTradeStrategy(ABC):

    def __init__(self, is_test=False):
        self.is_test = is_test
        self.indicator_builder = IndicatorsBuilder()
        self.indicator_builder.add(IndicatorType.CANDLE.name, CandleIndicator(is_test=is_test))
        self.progress_recorders = [CandleRecorder()]
        if self.is_test:
            self.progress_recorders.append(PositionRecorder())

    def get_indicators(self):
        self.indicator_builder_adder()
        return self.indicator_builder.build()

    def get_progress_recorders(self):
        self.progress_recorders_appender()
        return self.progress_recorders

    @staticmethod
    def make_key(indicator_type, suffix=''):
        return '{}{}'.format(indicator_type, suffix)

    @abstractmethod
    def indicator_builder_adder(self):
        raise NotImplementedError()

    @abstractmethod
    def progress_recorders_appender(self):
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
