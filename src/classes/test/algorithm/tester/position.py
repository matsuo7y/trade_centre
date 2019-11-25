from enum import Enum

from ....config import RATIO_TO_PIP_UNIT, SPREAD_PIP


class OrderDirection(Enum):
    LONG = 1
    SHORT = 2


class NoPositionException(Exception):
    pass


class Position:

    def __init__(self, candles_df):
        self.df = candles_df
        self.spread = SPREAD_PIP * RATIO_TO_PIP_UNIT
        self.order_direction = None
        self.entry_index = None
        self.order_price = None
        self.take_profit_price = None
        self.profit_pips = None
        self.current_profit_pips = None
        self.max_profit_pips = -1000.0
        self.min_profit_pips = 1000.0
        self.time = None

    def market_order(self, index, direction):
        self.order_direction = direction
        self.entry_index = index

        price = self.df['c'].iloc[index]
        if direction == OrderDirection.LONG.name:
            self.order_price = price + self.spread
        else:
            self.order_price = price - self.spread

    def __current_price_profit(self, index):
        current_price = self.df['c'].iloc[index]

        if self.order_direction == OrderDirection.LONG.name:
            profit = current_price - self.order_price
        else:
            profit = self.order_price - current_price

        profit /= RATIO_TO_PIP_UNIT
        return current_price, profit

    def set_current_profit(self, index):
        _, self.current_profit_pips = self.__current_price_profit(index)

    def set_max_profit(self, index):
        _, profit = self.__current_price_profit(index)
        if profit > self.max_profit_pips:
            self.max_profit_pips = profit

    def set_min_profit(self, index):
        _, profit = self.__current_price_profit(index)
        if profit < self.min_profit_pips:
            self.min_profit_pips = profit

    def take_profit_order(self, index):
        if self.order_price is None:
            raise NoPositionException("You don't have any positions.")

        self.time = index - self.entry_index
        self.take_profit_price, self.profit_pips = self.__current_price_profit(index)
