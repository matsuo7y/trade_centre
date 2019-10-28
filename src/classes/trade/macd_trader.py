from .trader import Trader
from ..api import CandleType
from ..indicator import MACDIndicator, MACDIndicatorSign


class MACDTrader(Trader):

    def __init__(self, order_units=10, candle_type=CandleType.S5.name, candle_count=500):
        super().__init__(order_units=order_units, candle_type=candle_type, candle_count=candle_count)

    def get_indicator(self):
        return MACDIndicator()

    def should_make_long_order(self, indicate):
        return indicate.value == MACDIndicatorSign.BOTH_UNDER_SIGNAL_LESS.name

    def should_make_short_order(self, indicate):
        return indicate.value == MACDIndicatorSign.BOTH_OVER_SIGNAL_GREATER.name

    def should_take_profit_long_order(self, indicate):
        return indicate.value == MACDIndicatorSign.BOTH_OVER_SIGNAL_GREATER.name

    def should_take_profit_short_order(self, indicate):
        return indicate.value == MACDIndicatorSign.BOTH_UNDER_SIGNAL_LESS.name
