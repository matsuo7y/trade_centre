from .abstract_progress_recorder import AbstractProgressRecorder
from ..indicator import IndicatorType


class BBANDRecorder(AbstractProgressRecorder):

    def __init__(self):
        super().__init__(is_series_record=True)
        self.upper_2_key = 'upper_2'
        self.upper_1_key = 'upper_1'
        self.middle_key = 'middle'
        self.lower_1_key = 'lower_1'
        self.lower_2_key = 'lower_2'
        self.indicator_key = IndicatorType.BBAND.name

    def get_value(self, iter_info):
        return iter_info.indicator_values[self.indicator_key].material

    def make_entry_record(self, value):
        upper_2 = value['upper_2'].iloc[-self.margin_period:].to_numpy().tolist()
        upper_1 = value['upper_1'].iloc[-self.margin_period:].to_numpy().tolist()
        middle = value['middle'].iloc[-self.margin_period:].to_numpy().tolist()
        lower_1 = value['lower_1'].iloc[-self.margin_period:].to_numpy().tolist()
        lower_2 = value['lower_2'].iloc[-self.margin_period:].to_numpy().tolist()

        return {
            self.upper_2_key: upper_2,
            self.upper_1_key: upper_1,
            self.middle_key: middle,
            self.lower_1_key: lower_1,
            self.lower_2_key: lower_2
        }

    def make_progress_record(self, current_record, value):
        latest_upper_2 = value['upper_2'].iloc[-1]
        latest_upper_1 = value['upper_1'].iloc[-1]
        latest_middle = value['middle'].iloc[-1]
        latest_lower_1 = value['lower_1'].iloc[-1]
        latest_lower_2 = value['lower_2'].iloc[-1]

        current_record[self.upper_2_key].append(latest_upper_2)
        current_record[self.upper_1_key].append(latest_upper_1)
        current_record[self.middle_key].append(latest_middle)
        current_record[self.lower_1_key].append(latest_lower_1)
        current_record[self.lower_2_key].append(latest_lower_2)

        return current_record

    def make_exit_record(self, current_record, value):
        return self.make_progress_record(current_record, value)
