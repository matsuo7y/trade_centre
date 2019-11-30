import logging
from enum import Enum

import numpy as np
import pandas as pd

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

    def __bbands(self, close, width=100):
        if width < self.time_period:
            raise ValueError('width should be greater than time period.')

        c = close.iloc[-width:] if len(close) > width else close

        upper_2, upper_1, middle, lower_1, lower_2 = [], [], [], [], []
        for i in range(width, self.time_period, -1):
            _c = c.iloc[-i:-i + self.time_period - 1].to_numpy()

            mean = np.mean(_c, dtype='float64')
            std = np.std(_c, dtype='float64')

            upper_2.append(mean + 2. * std)
            upper_1.append(mean + std)
            middle.append(mean)
            lower_1.append(mean - std)
            lower_2.append(mean - 2. * std)

        return pd.Series(upper_2), pd.Series(upper_1), pd.Series(middle), pd.Series(lower_1), pd.Series(lower_2)

    def get(self, df):
        c = df['c']

        upper_2, upper_1, middle, lower_1, lower_2 = self.__bbands(c)

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
