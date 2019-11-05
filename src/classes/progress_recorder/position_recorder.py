from enum import Enum

from .abstract_progress_recorder import AbstractProgressRecorder


class ProfitType(Enum):
    LOSS = 0
    PROFIT = 1


class PositionRecorder(AbstractProgressRecorder):

    def __init__(self):
        super().__init__(is_series_record=False)

    def get_value(self, test_iter_info):
        return test_iter_info.position

    def make_entry_record(self, value):
        return {'direction': value.order_direction}

    def make_progress_record(self, current_record, value):
        return current_record

    def make_exit_record(self, current_record, value):
        exit_record = {
            'profit': value.profit_pips,
            'max_profit': value.max_profit_pips,
            'position_time': value.time,
            'profit_or_loss': ProfitType.PROFIT.value if value.profit_pips > 0 else ProfitType.LOSS.value
        }
        current_record.update(exit_record)
        return current_record
