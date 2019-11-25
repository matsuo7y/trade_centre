from .abstract_trade_strategy import AbstractTradeStrategy
from ..config import RATIO_TO_PIP_UNIT
from ..indicator import (ADXIndicator, ADXIndicatorSign, IndicatorType, MACDIndicator, MACDIndicatorSign, ROCIndicator,
                         ROCIndicatorSign)
from ..progress_recorder import ADXRecorder, MACDRecorder, ROCRecorder


class QuadSignTradeStrategy(AbstractTradeStrategy):

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
        self.indicator_builder.add(IndicatorType.ADX.name, ADXIndicator(time_period=9, is_test=self.is_test))
        self.indicator_builder.add(IndicatorType.ROC.name, ROCIndicator(time_period=9, is_test=self.is_test))

    def progress_recorders_appender(self):
        self.progress_recorders.append(MACDRecorder(suffix='1'))
        self.progress_recorders.append(MACDRecorder(suffix='2'))
        self.progress_recorders.append(ADXRecorder())
        self.progress_recorders.append(ROCRecorder())

    def _get_indicator_value(self, indicator_values):
        return (
            indicator_values[self.make_key(IndicatorType.MACD.name, suffix='1')].value,
            indicator_values[self.make_key(IndicatorType.MACD.name, suffix='2')].value,
            indicator_values[IndicatorType.ADX.name].value,
            indicator_values[IndicatorType.ROC.name].value
        )

    def _get_latest_macd(self, indicator_values):
        macd = indicator_values[self.make_key(IndicatorType.MACD.name, suffix='1')].material
        return macd['macd'].iloc[-1]

    def should_make_long_order(self, indicator_values):
        macd_1, _, adx, roc = self._get_indicator_value(indicator_values)
        latest_macd = self._get_latest_macd(indicator_values)
        cond_macd_1 = macd_1 == MACDIndicatorSign.BOTH_UNDER_SIGNAL_LESS.name
        cond_adx = adx == ADXIndicatorSign.TREND_PLUS.name
        cond_roc = roc == ROCIndicatorSign.TREND_PLUS.name

        return cond_macd_1 and cond_adx and cond_roc and latest_macd < -0.4 * RATIO_TO_PIP_UNIT

    def should_make_short_order(self, indicator_values):
        macd_1, _, adx, roc = self._get_indicator_value(indicator_values)
        latest_macd = self._get_latest_macd(indicator_values)
        cond_macd_1 = macd_1 == MACDIndicatorSign.BOTH_OVER_SIGNAL_GREATER.name
        cond_adx = adx == ADXIndicatorSign.TREND_MINUS.name
        cond_roc = roc == ROCIndicatorSign.TREND_MINUS.name

        return cond_macd_1 and cond_adx and cond_roc and latest_macd > 0.4 * RATIO_TO_PIP_UNIT

    def should_take_profit_long_order(self, indicator_values):
        macd_1, _, adx, _ = self._get_indicator_value(indicator_values)
        cond_macd_1 = macd_1 == MACDIndicatorSign.BOTH_OVER_SIGNAL_GREATER.name
        cond_adx = adx == ADXIndicatorSign.TREND_PLUS.name

        return cond_macd_1 and not cond_adx

    def should_take_profit_short_order(self, indicator_values):
        macd_1, _, adx, _ = self._get_indicator_value(indicator_values)
        cond_macd_1 = macd_1 == MACDIndicatorSign.BOTH_UNDER_SIGNAL_LESS.name
        cond_adx = adx == ADXIndicatorSign.TREND_MINUS.name

        return cond_macd_1 and not cond_adx
