import logging
from enum import Enum

import talib

from .indicator import AbstractIndicator, IndicatorValue


class BBANDIndicatorSign(Enum):
    BEYOND_UPPER = 1
    UPPER_1_TO_2 = 2
    UPPER_0_TO_1 = 3
    LOWER_0_TO_1 = 4
    LOWER_1_TO_2 = 5
    BEYOND_LOWER = 6


class BBANDIndicator(AbstractIndicator):

    def __init__(self, time_period=6, is_test=False):
        super().__init__(is_test=is_test)
        self.time_period = time_period

    def get(self, df):
        c = df['c']

        upper_1, middle, lower_1 = talib.BBANDS(c, timeperiod=self.time_period, nbdevup=1, nbdevdn=1)
        upper_2, _, lower_2 = talib.BBANDS(c, timeperiod=self.time_period, nbdevup=2, nbdevdn=2)

        latest_c = c.iloc[-1]
        latest_upper_1, latest_middle, latest_lower_1 = upper_1.iloc[-1], middle.iloc[-1], lower_1.iloc[-1]
        latest_upper_2, latest_lower_2 = upper_2.iloc[-1], lower_2.iloc[-1]

        material = dict(upper_2=upper_2, upper_1=upper_1, middle=middle, lower_1=lower_1, lower_2=lower_2)

        if latest_c > latest_upper_2:
            indicator_value = IndicatorValue(BBANDIndicatorSign.BEYOND_UPPER.name, material=material)
        elif latest_upper_1 < latest_c <= latest_upper_2:
            indicator_value = IndicatorValue(BBANDIndicatorSign.UPPER_1_TO_2.name, material=material)
        elif latest_middle < latest_c <= latest_upper_1:
            indicator_value = IndicatorValue(BBANDIndicatorSign.UPPER_0_TO_1.name, material=material)
        elif latest_lower_1 < latest_c <= latest_middle:
            indicator_value = IndicatorValue(BBANDIndicatorSign.LOWER_0_TO_1.name, material=material)
        elif latest_lower_2 < latest_c <= latest_lower_1:
            indicator_value = IndicatorValue(BBANDIndicatorSign.LOWER_1_TO_2.name, material=material)
        else:
            indicator_value = IndicatorValue(BBANDIndicatorSign.BEYOND_LOWER.name, material=material)

        if not self.is_test:
            logging.info('sign=>%s upper_2=>%s lower_2=>%s', indicator_value.value, latest_upper_2, latest_lower_2)

        return indicator_value
