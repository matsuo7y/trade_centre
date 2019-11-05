from .abstract_progress_recorder import AbstractProgressRecorder
from ..indicator import IndicatorType


class ADXRecorder(AbstractProgressRecorder):

    def __init__(self, suffix=''):
        super().__init__(is_series_record=True)
        self.adx_key = 'adx{}'.format(suffix)
        self.plus_di_key = 'plus_di{}'.format(suffix)
        self.minus_di_key = 'minus_di{}'.format(suffix)
        self.indicator_key = '{}{}'.format(IndicatorType.ADX.name, suffix)

    def get_value(self, iter_info):
        return iter_info.indicator_values[self.indicator_key].material

    def make_entry_record(self, value):
        adx = value['adx'].iloc[-self.margin_period:].to_numpy().tolist()
        plus_di = value['plus_di'].iloc[-self.margin_period:].to_numpy().tolist()
        minus_di = value['minus_di'].iloc[-self.margin_period:].to_numpy().tolist()

        return {
            self.adx_key: adx,
            self.plus_di_key: plus_di,
            self.minus_di_key: minus_di
        }

    def make_progress_record(self, current_record, value):
        latest_adx = value['adx'].iloc[-1]
        latest_plus_di = value['plus_di'].iloc[-1]
        latest_minus_di = value['minus_di'].iloc[-1]

        current_record[self.adx_key].append(latest_adx)
        current_record[self.plus_di_key].append(latest_plus_di)
        current_record[self.minus_di_key].append(latest_minus_di)

        return current_record

    def make_exit_record(self, current_record, value):
        return self.make_progress_record(current_record, value)
