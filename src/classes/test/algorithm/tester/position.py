from enum import Enum


class OrderDirection(Enum):
    LONG = 1
    SHORT = 2


class NoPositionException(Exception):
    pass


class Position:

    def __init__(self, candles_df):
        self.df = candles_df
        self.spread = 0.008
        self.order_direction = None
        self.entry_index = None
        self.order_price = None
        self.take_profit_price = None
        self.profit_pips = None
        self.max_profit_pips = -1000.0
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

        profit *= 100.
        return current_price, profit

    def set_max_profit(self, index):
        _, profit = self.__current_price_profit(index)
        if profit > self.max_profit_pips:
            self.max_profit_pips = profit

    def take_profit_order(self, index):
        if self.order_price is None:
            raise NoPositionException("You don't have any positions.")

        self.time = index - self.entry_index
        self.take_profit_price, self.profit_pips = self.__current_price_profit(index)
