from .indicator import AbstractIndicator, IndicatorValue
import logging
from enum import Enum


class CandleIndicatorSign(Enum):
    NORMAL = 1


class CandleIndicator(AbstractIndicator):

    def __init__(self, is_test=False):
        super().__init__(is_test=is_test)

    def get(self, df):
        o, h, l, c, time = df['o'], df['h'], df['l'], df['c'], df['time']

        material = dict(open=o, high=h, low=l, close=c, time=time)
        indicator_value = IndicatorValue(None, material=material)

        if not self.is_test:
            logging.info(
                'Candle: time=>%s o=>%s h=>%s l=>%s c=>%s',
                time.iloc[-1], o.iloc[-1], h.iloc[-1], l.iloc[-1], c.iloc[-1]
            )

        return indicator_value
