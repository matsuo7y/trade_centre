from .abstract_trade_strategy import AbstractTradeStrategy
from ..indicator import IndicatorsBuilder, IndicatorType, MACDIndicator, MACDIndicatorSign


class MACDTradeStrategy(AbstractTradeStrategy):

    def __init__(self, is_test=False):
        super().__init__(is_test=is_test)

    def get_indicators(self):
        indicator_builder = IndicatorsBuilder()
        indicator_builder.add(
            IndicatorType.MACD.name,
            MACDIndicator(fast_period=12, slow_period=26, signal_period=9, is_test=self.is_test)
        )
        return indicator_builder.build()

    def should_make_long_order(self, indicator_values):
        return indicator_values[IndicatorType.MACD.name].value == MACDIndicatorSign.BOTH_UNDER_SIGNAL_LESS.name

    def should_make_short_order(self, indicator_values):
        return indicator_values[IndicatorType.MACD.name].value == MACDIndicatorSign.BOTH_OVER_SIGNAL_GREATER.name

    def should_take_profit_long_order(self, indicator_values):
        return indicator_values[IndicatorType.MACD.name].value == MACDIndicatorSign.BOTH_OVER_SIGNAL_GREATER.name

    def should_take_profit_short_order(self, indicator_values):
        return indicator_values[IndicatorType.MACD.name].value == MACDIndicatorSign.BOTH_UNDER_SIGNAL_LESS.name
