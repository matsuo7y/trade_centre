from .abstract_trade_strategy import AbstractTradeStrategy
from ..indicator import (
    IndicatorsBuilder, IndicatorType, MACDIndicator, MACDIndicatorSign, ADXIndicator, ADXIndicatorSign
)


class MACDADXTradeStrategy(AbstractTradeStrategy):

    def __init__(self, is_test=False):
        super().__init__(is_test=is_test)

    def get_indicators(self):
        indicator_builder = IndicatorsBuilder()
        indicator_builder.add(IndicatorType.MACD.name, MACDIndicator(is_test=self.is_test))
        indicator_builder.add(IndicatorType.ADX.name, ADXIndicator(is_test=self.is_test))
        return indicator_builder.build()

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
