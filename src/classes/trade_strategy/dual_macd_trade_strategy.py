from .abstract_trade_strategy import AbstractTradeStrategy
from ..indicator import IndicatorType, MACDIndicator, MACDIndicatorSign
from ..progress_recorder import MACDRecorder


class DualMACDTradeStrategy(AbstractTradeStrategy):

    def __init__(self, is_test=False):
        super().__init__(is_test=is_test)

    def indicator_builder_adder(self):
        self.indicator_builder.add(
            IndicatorType.MACD.name,
            MACDIndicator(fast_period=12, slow_period=26, signal_period=9, is_test=self.is_test),
            suffix='1'
        )
        self.indicator_builder.add(
            IndicatorType.MACD.name,
            MACDIndicator(fast_period=4, slow_period=9, signal_period=4, is_test=self.is_test),
            suffix='2'
        )

    def progress_recorders_appender(self):
        self.progress_recorders.append(MACDRecorder(suffix='1'))
        self.progress_recorders.append(MACDRecorder(suffix='2'))

    def _get_indicator_value(self, indicator_values):
        return (
            indicator_values[self.make_key(IndicatorType.MACD.name, suffix='1')].value,
            indicator_values[self.make_key(IndicatorType.MACD.name, suffix='2')].value
        )

    def _get_latest_macd_difference(self, indicator_values):
        macd_1 = indicator_values[self.make_key(IndicatorType.MACD.name, suffix='1')].material
        macd_2 = indicator_values[self.make_key(IndicatorType.MACD.name, suffix='2')].material
        return macd_1['macd'].iloc[-1] - macd_1['macd'].iloc[-2], macd_2['macd'].iloc[-1] - macd_2['macd'].iloc[-2]

    @staticmethod
    def __cond_macd_greater(sign):
        cond_1 = sign == MACDIndicatorSign.BOTH_OVER_MACD_GREATER.name
        cond_2 = sign == MACDIndicatorSign.BOTH_UNDER_SIGNAL_LESS.name
        cond_3 = sign == MACDIndicatorSign.SEPARATE_MACD_GREATER.name
        return cond_1 or cond_2 or cond_3

    @staticmethod
    def __cond_macd_less(sign):
        cond_1 = sign == MACDIndicatorSign.BOTH_OVER_SIGNAL_GREATER.name
        cond_2 = sign == MACDIndicatorSign.BOTH_UNDER_MACD_LESS.name
        cond_3 = sign == MACDIndicatorSign.SEPATATE_SIGNAL_GREATER.name
        return cond_1 or cond_2 or cond_3

    def should_make_long_order(self, indicator_values):
        macd_1, macd_2 = self._get_indicator_value(indicator_values)
        cond_macd_1 = self.__cond_macd_greater(macd_1)
        cond_macd_2 = self.__cond_macd_greater(macd_2)
        return cond_macd_1 and cond_macd_2

    def should_make_short_order(self, indicator_values):
        macd_1, macd_2 = self._get_indicator_value(indicator_values)
        cond_macd_1 = self.__cond_macd_less(macd_1)
        cond_macd_2 = self.__cond_macd_less(macd_2)
        return cond_macd_1 and cond_macd_2

    def should_take_profit_long_order(self, indicator_values):
        _, macd_2 = self._get_indicator_value(indicator_values)
        cond_macd_2 = self.__cond_macd_less(macd_2)
        return cond_macd_2

    def should_take_profit_short_order(self, indicator_values):
        _, macd_2 = self._get_indicator_value(indicator_values)
        cond_macd_2 = self.__cond_macd_greater(macd_2)
        return cond_macd_2
