from .abstract_progress_recorder import AbstractProgressRecorder
from ..indicator import IndicatorType


class CandleRecorder(AbstractProgressRecorder):

    def __init__(self):
        super().__init__(is_series_record=True)

    def get_value(self, iter_info):
        return iter_info.indicator_values[IndicatorType.CANDLE.name].material

    def make_entry_record(self, value):
        o = value['open'].iloc[-self.margin_period:].to_numpy().tolist()
        h = value['high'].iloc[-self.margin_period:].to_numpy().tolist()
        l = value['low'].iloc[-self.margin_period:].to_numpy().tolist()
        c = value['close'].iloc[-self.margin_period:].to_numpy().tolist()

        return {'open': o, 'high': h, 'low': l, 'close': c}

    def make_progress_record(self, current_record, value):
        latest_o = value['open'].iloc[-1]
        latest_h = value['high'].iloc[-1]
        latest_l = value['low'].iloc[-1]
        latest_c = value['close'].iloc[-1]

        current_record['open'].append(latest_o)
        current_record['high'].append(latest_h)
        current_record['low'].append(latest_l)
        current_record['close'].append(latest_c)

        return current_record

    def make_exit_record(self, current_record, value):
        return self.make_progress_record(current_record, value)
