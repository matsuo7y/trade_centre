from .position import OrderDirection
from .test_iterator import TestIterator
from ....trade_strategy import MACDTradeStrategy


class AlgorithmTester:

    def __init__(self, candles_file_path, strategy=MACDTradeStrategy(is_test=True), start=-100000, end=-1,
                 window_size=500, dump_file_path=None):
        self.strategy = strategy

        self.test_iterator = TestIterator(
            candles_file_path, self.strategy.get_indicators(), self.strategy.get_progress_recorders(), start=start,
            end=end, window_size=window_size, dump_file_path=dump_file_path
        )

    def work(self):
        for iter_state in self.test_iterator:

            if iter_state.position is None:

                order_direction = None

                if self.strategy.should_make_short_order(iter_state.indicator_values):
                    order_direction = OrderDirection.SHORT.name
                elif self.strategy.should_make_long_order(iter_state.indicator_values):
                    order_direction = OrderDirection.LONG.name

                if order_direction is not None:
                    iter_state.entry(order_direction)

                continue

            close_long_order_cond = \
                iter_state.position.order_direction == OrderDirection.LONG.name and \
                self.strategy.should_take_profit_long_order(iter_state.indicator_values)

            close_short_order_cond = \
                iter_state.position.order_direction == OrderDirection.SHORT.name and \
                self.strategy.should_take_profit_short_order(iter_state.indicator_values)

            if close_long_order_cond or close_short_order_cond:
                iter_state.exit()
