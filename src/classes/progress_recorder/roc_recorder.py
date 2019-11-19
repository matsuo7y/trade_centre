from .abstract_progress_recorder import AbstractProgressRecorder
from ..indicator import IndicatorType


class ROCRecorder(AbstractProgressRecorder):

    def __init__(self, suffix=''):
        super().__init__(is_series_record=True)
        self.roc_key = 'roc{}'.format(suffix)
        self.indicator_key = '{}{}'.format(IndicatorType.ROC.name, suffix)

    def get_value(self, iter_info):
        return iter_info.indicator_values[self.indicator_key].material

    def make_entry_record(self, value):
        roc = value['roc'].iloc[-self.margin_period:].to_numpy().tolist()
        return {
            self.roc_key: roc
        }

    def make_progress_record(self, current_record, value):
        latest_roc = value['roc'].iloc[-1]
        current_record[self.roc_key].append(latest_roc)

        return current_record

    def make_exit_record(self, current_record, value):
        return self.make_progress_record(current_record, value)
