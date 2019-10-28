import logging
from abc import *

from .trade_iterator import TradeIterator, OperationMode
from ..api import CandleType, OrderDirection
from ..api.post import order
from ..api.put import close_trade


class Trader(ABC):

    def __init__(self, order_units=10, candle_type=CandleType.S5.name, candle_count=500):
        self.order_units = order_units
        self.trade_iterator = TradeIterator(self.get_indicator(), candle_type=candle_type, candle_count=candle_count)

    @abstractmethod
    def get_indicator(self):
        raise NotImplementedError()

    @abstractmethod
    def should_make_long_order(self, indicator_value):
        raise NotImplementedError()

    @abstractmethod
    def should_make_short_order(self, indicator_value):
        raise NotImplementedError()

    @abstractmethod
    def should_take_profit_long_order(self, indicator_value):
        raise NotImplementedError()

    @abstractmethod
    def should_take_profit_short_order(self, indicator_value):
        raise NotImplementedError()

    def work(self):
        for iter_info in self.trade_iterator:
            if iter_info.operation_mode == OperationMode.WATCH.name:
                continue

            if iter_info.trade_id is None and iter_info.operation_mode == OperationMode.TRADE.name:

                if self.should_make_short_order(iter_info.indicator_value):
                    iter_info.order_direction = OrderDirection.SHORT.name
                elif self.should_make_long_order(iter_info.indicator_value):
                    iter_info.order_direction = OrderDirection.LONG.name

                if iter_info.order_direction is not None:
                    order.post(iter_info.account_id, direction=iter_info.order_direction, units=self.order_units)
                    logging.info('Make %s order', iter_info.order_direction)

                continue

            close_long_order_cond = \
                iter_info.order_direction == OrderDirection.LONG.name and \
                self.should_take_profit_long_order(iter_info.indicator_value)

            close_short_order_cond = \
                iter_info.order_direction == OrderDirection.SHORT.name and \
                self.should_take_profit_short_order(iter_info.indicator_value)

            if close_long_order_cond or close_short_order_cond:
                close_trade.put(iter_info.account_id, iter_info.trade_id)
                iter_info.order_direction = None
                logging.info('Close order')

            continue
