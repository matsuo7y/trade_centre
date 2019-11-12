import logging
from enum import Enum

import talib

from .indicator import AbstractIndicator, IndicatorValue


class ADXIndicatorSign(Enum):
    TREND_PLUS = 1
    TREND_MINUS = 2
    NO_TREND_PLUS = 3
    NO_TREND_MINUS = 4


class ADXIndicator(AbstractIndicator):
    trend_threshold = 34.0

    def __init__(self, time_period=9, is_test=False):
        super().__init__(is_test=is_test)
        self.time_period = time_period

    def get(self, df):
        h, l, c = df['h'], df['l'], df['c']

        adx = talib.ADX(h, l, c, timeperiod=self.time_period)
        plus_di = talib.PLUS_DI(h, l, c, timeperiod=self.time_period)
        minus_di = talib.MINUS_DI(h, l, c, timeperiod=self.time_period)

        last_adx, last_plus_di, last_minus_di = adx.iloc[-1], plus_di.iloc[-1], minus_di.iloc[-1]

        material = dict(adx=adx, plus_di=plus_di, minus_di=minus_di)

        if last_adx > self.trend_threshold:
            if last_plus_di > last_minus_di:
                indicator_value = IndicatorValue(ADXIndicatorSign.TREND_PLUS.name, material=material)
            else:
                indicator_value = IndicatorValue(ADXIndicatorSign.TREND_MINUS.name, material=material)
        else:
            if last_plus_di > last_minus_di:
                indicator_value = IndicatorValue(ADXIndicatorSign.NO_TREND_PLUS.name, material=material)
            else:
                indicator_value = IndicatorValue(ADXIndicatorSign.NO_TREND_MINUS.name, material=material)

        if not self.is_test:
            logging.info('sign=>%s ADX=>%s +DI=>%s -DI=>%s', indicator_value.value, last_adx, last_plus_di,
                         last_minus_di)

        return indicator_value
