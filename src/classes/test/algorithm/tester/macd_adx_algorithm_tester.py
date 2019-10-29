from .abstract_algorithm_tester import AbstractAlgorithmTester
from ..process import TradeProcessBuilder
from ....indicator import (
    IndicatorType, IndicatorBuilder, MACDIndicator, MACDIndicatorSign, ADXIndicator, ADXIndicatorSign
)


class MACDADXAlgorithmTester(AbstractAlgorithmTester):

    def __init__(self, candles_file_path, process_file_path, start=-10000, end=-1, window_size=500):
        super().__init__(candles_file_path, process_file_path, start=start, end=end, window_size=window_size)

    def get_process_builder(self, process_file_path):
        return TradeProcessBuilder(process_file_path)

    def get_indicators(self):
        indicator_builder = IndicatorBuilder()
        indicator_builder.add(IndicatorType.MACD.name, MACDIndicator(is_test=True))
        indicator_builder.add(IndicatorType.ADX.name, ADXIndicator(is_test=True))
        return indicator_builder.build()

    @staticmethod
    def _get_indicator_value(indicator_values):
        return indicator_values[IndicatorType.MACD.name].value, indicator_values[IndicatorType.ADX.name].value

    def should_make_long_order(self, indicator_values):
        macd, adx = self._get_indicator_value(indicator_values)
        cond_macd = macd == MACDIndicatorSign.BOTH_OVER_MACD_GREATER.name
        cond_adx = adx == ADXIndicatorSign.TREND_PLUS.name

        return cond_macd and cond_adx

    def should_make_short_order(self, indicator_values):
        macd, adx = self._get_indicator_value(indicator_values)
        cond_macd = macd == MACDIndicatorSign.BOTH_UNDER_MACD_LESS.name
        cond_adx = adx == ADXIndicatorSign.TREND_MINUS.name

        return cond_macd and cond_adx

    def should_take_profit_long_order(self, indicator_values):
        macd, adx = self._get_indicator_value(indicator_values)
        cond_macd = macd == MACDIndicatorSign.BOTH_OVER_SIGNAL_GREATER.name
        cond_adx1 = adx == ADXIndicatorSign.TREND_MINUS.name
        cond_adx2 = adx == ADXIndicatorSign.NO_TREND_MINUS.name

        return cond_macd or cond_adx1 or cond_adx2

    def should_take_profit_short_order(self, indicator_values):
        macd, adx = self._get_indicator_value(indicator_values)
        cond_macd = macd == MACDIndicatorSign.BOTH_UNDER_SIGNAL_LESS.name
        cond_adx1 = adx == ADXIndicatorSign.TREND_PLUS.name
        cond_adx2 = adx == ADXIndicatorSign.NO_TREND_PLUS.name

        return cond_macd or cond_adx1 or cond_adx2
