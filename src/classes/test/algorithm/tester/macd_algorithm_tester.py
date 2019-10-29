from .abstract_algorithm_tester import AbstractAlgorithmTester
from ..process import TradeProcessBuilder
from ....indicator import IndicatorBuilder, IndicatorType, MACDIndicator, MACDIndicatorSign


class MACDAlgorithmTester(AbstractAlgorithmTester):

    def __init__(self, candles_file_path, process_file_path, start=-100000, end=-1, window_size=500):
        super().__init__(candles_file_path, process_file_path, start=start, end=end, window_size=window_size)

    def get_process_builder(self, process_file_path):
        return TradeProcessBuilder(process_file_path)

    def get_indicators(self):
        indicator_builder = IndicatorBuilder()
        indicator_builder.add(IndicatorType.MACD.name, MACDIndicator(is_test=True))
        return indicator_builder.build()

    def should_make_long_order(self, indicator_values):
        return indicator_values[IndicatorType.MACD.name].value == MACDIndicatorSign.BOTH_UNDER_SIGNAL_LESS.name

    def should_make_short_order(self, indicator_values):
        return indicator_values[IndicatorType.MACD.name].value == MACDIndicatorSign.BOTH_OVER_SIGNAL_GREATER.name

    def should_take_profit_long_order(self, indicator_values):
        return indicator_values[IndicatorType.MACD.name].value == MACDIndicatorSign.BOTH_OVER_SIGNAL_GREATER.name

    def should_take_profit_short_order(self, indicator_values):
        return indicator_values[IndicatorType.MACD.name].value == MACDIndicatorSign.BOTH_UNDER_SIGNAL_LESS.name
