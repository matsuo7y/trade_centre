from .trader import Trader
from ..api import CandleType
from ..indicator import MACDIndicator, MACDIndicatorSign


class MACDTrader(Trader):

    def __init__(self, order_units=10000, candle_type=CandleType.S10.name, candle_count=500):
        super().__init__(order_units=order_units, candle_type=candle_type, candle_count=candle_count)

    def get_indicator(self):
        return MACDIndicator()

    def should_make_long_order(self, indicate):
        return indicate == MACDIndicatorSign.MACD_OVER

    def should_make_short_order(self, indicate):
        return indicate == MACDIndicatorSign.MACD_UNDER

    def should_take_profit_long_order(self, indicate):
        return indicate == MACDIndicatorSign.MACD_UNDER or indicate == MACDIndicatorSign.BOTH_OVER_SIGNAL_GREATER

    def should_take_profit_short_order(self, indicate):
        return indicate == MACDIndicatorSign.MACD_OVER or indicate == MACDIndicatorSign.BOTH_UNDER_SIGNAL_LESS
