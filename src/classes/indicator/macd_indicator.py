import logging
from enum import Enum

import talib

from .indicator import Indicator, IndicatorValue


class MACDIndicatorSign(Enum):
    MACD_UNDER = 1
    BOTH_UNDER_MACD_LESS = 2
    BOTH_UNDER_SIGNAL_LESS = 3
    MACD_OVER = 4
    BOTH_OVER_MACD_GREATER = 5
    BOTH_OVER_SIGNAL_GREATER = 6


class MACDIndicator(Indicator):

    def __init__(self, fastperiod=12, slowperiod=26, signalperiod=9):
        super().__init__()
        self.fastperiod = fastperiod
        self.slowperiod = slowperiod
        self.signalperiod = signalperiod

    def get(self, df):
        macd, macd_signal, _ = talib.MACD(
            df['c'], fastperiod=self.fastperiod, slowperiod=self.slowperiod, signalperiod=self.signalperiod)

        latest_macd = macd.iloc[-1]
        latest_signal = macd_signal.iloc[-1]

        material = dict(macd=latest_macd, signal=latest_signal)

        indicator_value = None
        if latest_macd < 0:
            if latest_signal < 0:
                if latest_macd < latest_signal:
                    indicator_value = IndicatorValue(MACDIndicatorSign.BOTH_UNDER_MACD_LESS, material=material)
                else:
                    indicator_value = IndicatorValue(MACDIndicatorSign.BOTH_UNDER_SIGNAL_LESS, material=material)
            else:
                indicator_value = IndicatorValue(MACDIndicatorSign.MACD_UNDER, material=material)

        if latest_macd > 0:
            if latest_signal > 0:
                if latest_macd > latest_signal:
                    indicator_value = IndicatorValue(MACDIndicatorSign.BOTH_OVER_MACD_GREATER, material=material)
                else:
                    indicator_value = IndicatorValue(MACDIndicatorSign.BOTH_OVER_SIGNAL_GREATER, material=material)
            else:
                indicator_value = IndicatorValue(MACDIndicatorSign.MACD_OVER, material=material)

        logging.info("sign=>%s macd=>%s signal=>%s", indicator_value.value.name, latest_macd, latest_signal)

        return indicator_value