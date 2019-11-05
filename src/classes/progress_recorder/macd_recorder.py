from .abstract_progress_recorder import AbstractProgressRecorder
from ..indicator import IndicatorType


class MACDRecorder(AbstractProgressRecorder):

    def __init__(self, suffix=''):
        super().__init__(is_series_record=True)
        self.macd_key = 'macd{}'.format(suffix)
        self.signal_key = 'signal{}'.format(suffix)
        self.indicator_key = '{}{}'.format(IndicatorType.MACD.name, suffix)

    def get_value(self, iter_info):
        return iter_info.indicator_values[self.indicator_key].material

    def make_entry_record(self, value):
        macd = value['macd'].iloc[-self.margin_period:].to_numpy().tolist()
        signal = value['signal'].iloc[-self.margin_period:].to_numpy().tolist()

        return {
            self.macd_key: macd,
            self.signal_key: signal
        }

    def make_progress_record(self, current_record, value):
        latest_macd = value['macd'].iloc[-1]
        latest_signal = value['signal'].iloc[-1]

        current_record[self.macd_key].append(latest_macd)
        current_record[self.signal_key].append(latest_signal)

        return current_record

    def make_exit_record(self, current_record, value):
        return self.make_progress_record(current_record, value)
