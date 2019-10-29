from abc import *

from .position import OrderDirection, Position
from .test_iterator import TestIterator


class AbstractAlgorithmTester(ABC):

    def __init__(self, candles_file_path, process_file_path, start=-100000, end=-1, window_size=500):
        self.test_iterator = TestIterator(
            candles_file_path, self.get_indicators(), start=start, end=end, window_size=window_size)

        self.process_builder = self.get_process_builder(process_file_path)
        self.position = None

    @abstractmethod
    def get_process_builder(self, process_file_path):
        raise NotImplementedError()

    @abstractmethod
    def get_indicators(self):
        raise NotImplementedError()

    @abstractmethod
    def should_make_long_order(self, indicator_values):
        raise NotImplementedError()

    @abstractmethod
    def should_make_short_order(self, indicator_values):
        raise NotImplementedError()

    @abstractmethod
    def should_take_profit_long_order(self, indicator_values):
        raise NotImplementedError()

    @abstractmethod
    def should_take_profit_short_order(self, indicator_values):
        raise NotImplementedError()

    def work(self, log_interval=10000):
        df = self.test_iterator.df

        for indicator_values, index in self.test_iterator:
            if index % log_interval == 0:
                print('progress: {}'.format(index))

            if self.position is None:

                order_direction = None

                if self.should_make_short_order(indicator_values):
                    order_direction = OrderDirection.SHORT.name
                elif self.should_make_long_order(indicator_values):
                    order_direction = OrderDirection.LONG.name

                if order_direction is not None:
                    self.position = Position(df)
                    self.position.market_order(index, order_direction)
                    self.process_builder.entry(self.position, indicator_values)

                continue

            close_long_order_cond = \
                self.position.order_direction == OrderDirection.LONG.name and \
                self.should_take_profit_long_order(indicator_values)

            close_short_order_cond = \
                self.position.order_direction == OrderDirection.SHORT.name and \
                self.should_take_profit_short_order(indicator_values)

            if close_long_order_cond or close_short_order_cond:
                self.position.take_profit_order(index)
                self.process_builder.exit(self.position, indicator_values)
                self.position = None
