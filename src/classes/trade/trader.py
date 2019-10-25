import logging
from abc import *

from .trade_iterator import TradeIterator
from ..api import CandleType, OrderDirection
from ..api.post import order
from ..api.put import close_trade


class Trader(ABC):

    def __init__(self, order_units=10000, candle_type=CandleType.S10.name, candle_count=500):
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
            if iter_info.trade_id is None:

                order_direction = None

                if self.should_make_short_order(iter_info.indicator_value):
                    order_direction = OrderDirection.SHORT.name
                elif self.should_make_long_order(iter_info.indicator_value):
                    order_direction = OrderDirection.LONG.name

                if order_direction is not None:
                    order.post(iter_info.account_id, direction=order_direction, units=self.order_units)
                    logging.info('Make {} order', order_direction)

                continue

            close_long_order_cond = \
                iter_info.order_direction == OrderDirection.LONG and \
                self.should_take_profit_long_order(iter_info.indicator_value)

            close_short_order_cond = \
                iter_info.order_direction == OrderDirection.SHORT and \
                self.should_take_profit_short_order(iter_info.indicator_value)

            if close_long_order_cond or close_short_order_cond:
                close_trade.put(iter_info.account_id, iter_info.trade_id)

            continue
