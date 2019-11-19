import logging
from enum import Enum

import talib

from .indicator import AbstractIndicator, IndicatorValue


class ROCIndicatorSign(Enum):
    TREND_PLUS = 1
    NO_TREND_PLUS = 2
    TREND_MINUS = 3
    NO_TREND_MINUS = 4


class ROCIndicator(AbstractIndicator):
    trend_threshold = 0.015

    def __init__(self, time_period=9, is_test=False):
        super().__init__(is_test=is_test)
        self.time_period = time_period

    def get(self, df):
        roc = talib.ROC(df['c'], timeperiod=self.time_period)
        latest_roc = roc.iloc[-1]

        material = dict(roc=roc)

        if latest_roc > self.trend_threshold:
            indicator_value = IndicatorValue(ROCIndicatorSign.TREND_PLUS.name, material=material)

        if 0 <= latest_roc <= self.trend_threshold:
            indicator_value = IndicatorValue(ROCIndicatorSign.NO_TREND_PLUS.name, material=material)

        if -self.trend_threshold <= latest_roc < 0:
            indicator_value = IndicatorValue(ROCIndicatorSign.NO_TREND_MINUS.name, material=material)

        if latest_roc < -self.trend_threshold:
            indicator_value = IndicatorValue(ROCIndicatorSign.TREND_MINUS.name, material=material)

        if not self.is_test:
            logging.info('sign=>{} ROC=>{}'.format(indicator_value.value, latest_roc))

        return indicator_value
