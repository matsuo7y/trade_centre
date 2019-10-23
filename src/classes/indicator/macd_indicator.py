import talib

from .indicator import Indicator


class MACDIndicator(Indicator):
    MACD_UNDER = 1
    BOTH_UNDER_MACD_LESS = 2
    BOTH_UNDER_SIGNAL_LESS = 3
    MACD_OVER = 4
    BOTH_OVER_MACD_GREATER = 5
    BOTH_OVER_SIGNAL_GREATER = 6

    def __init__(self, fastperiod=12, slowperiod=26, signalperiod=9):
        super().__init__()
        self.fastperiod = fastperiod
        self.slowperiod = slowperiod
        self.signalperiod = signalperiod

    def get(self, df):
        macd, macd_signal, _ = talib.MACD(
            df['o'], fastperiod=self.fastperiod, slowperiod=self.slowperiod, signalperiod=self.signalperiod)

        latest_macd = macd.iloc[-1]
        latest_signal = macd_signal.iloc[-1]

        if latest_macd < 0:
            if latest_signal < 0:
                if latest_macd < latest_signal:
                    return self.BOTH_UNDER_MACD_LESS
                else:
                    return self.BOTH_UNDER_SIGNAL_LESS
            else:
                return self.MACD_UNDER

        if latest_macd > 0:
            if latest_signal > 0:
                if latest_macd > latest_signal:
                    return self.BOTH_OVER_MACD_GREATER
                else:
                    return self.BOTH_OVER_SIGNAL_GREATER
            else:
                return self.MACD_OVER

        return None
