from .abstract_trade_strategy import AbstractTradeStrategy
from ..indicator import IndicatorType, MACDIndicator, MACDIndicatorSign, ADXIndicator, ADXIndicatorSign
from ..progress_recorder import MACDRecorder, ADXRecorder


class MACDADXTradeStrategy(AbstractTradeStrategy):

    def __init__(self, is_test=False):
        super().__init__(is_test=is_test)

    def indicator_builder_adder(self):
        self.indicator_builder.add(
            IndicatorType.MACD.name,
            MACDIndicator(fast_period=12, slow_period=26, signal_period=9, is_test=self.is_test)
        )
        self.indicator_builder.add(IndicatorType.ADX.name, ADXIndicator(time_period=9, is_test=self.is_test))

    def progress_recorders_appender(self):
        self.progress_recorders.append(MACDRecorder())
        self.progress_recorders.append(ADXRecorder())

    @staticmethod
    def _get_indicator_value(indicator_values):
        return indicator_values[IndicatorType.MACD.name].value, indicator_values[IndicatorType.ADX.name].value

    def should_make_long_order(self, indicator_values):
        macd, adx = self._get_indicator_value(indicator_values)
        cond_macd_1 = macd == MACDIndicatorSign.BOTH_UNDER_SIGNAL_LESS.name
        cond_adx = adx == ADXIndicatorSign.TREND_PLUS.name

        return cond_macd_1 and cond_adx

    def should_make_short_order(self, indicator_values):
        macd, adx = self._get_indicator_value(indicator_values)
        cond_macd_1 = macd == MACDIndicatorSign.BOTH_OVER_SIGNAL_GREATER.name
        cond_adx = adx == ADXIndicatorSign.TREND_MINUS.name

        return cond_macd_1 and cond_adx

    def should_take_profit_long_order(self, indicator_values):
        macd, adx = self._get_indicator_value(indicator_values)
        cond_macd_1 = macd == MACDIndicatorSign.BOTH_OVER_SIGNAL_GREATER.name
        cond_adx = adx == ADXIndicatorSign.TREND_PLUS.name

        return cond_macd_1 and not cond_adx

    def should_take_profit_short_order(self, indicator_values):
        macd, adx = self._get_indicator_value(indicator_values)
        cond_macd_1 = macd == MACDIndicatorSign.BOTH_UNDER_SIGNAL_LESS.name
        cond_adx = adx == ADXIndicatorSign.TREND_MINUS.name

        return cond_macd_1 and not cond_adx
