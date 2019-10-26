import logging
import sys
from enum import Enum
from os import path

import pandas as pd

from ..api import CandleType, OrderDirection
from ..api.get import account, account_changes, accounts, candles, open_trades


class TradeInfo:

    def __init__(self, account_id, last_transaction_id):
        self.account_id = account_id
        self.last_transaction_id = last_transaction_id
        self.trade_id = None
        self.order_direction = None
        self.candles_df = None
        self.indicator_value = None
        self.operation_mode = None

    def reset(self):
        self.trade_id = None
        self.order_direction = None
        self.candles_df = None
        self.indicator_value = None
        self.operation_mode = None


class OperationMode(Enum):
    WATCH = 1
    TRADE = 2
    TERMINATE = 3


class TradeIterator:

    def __init__(self, indicator, candle_type=CandleType.S10.name, candle_count=500):
        self.indicator = indicator
        self.candle_type = candle_type
        self.candle_count = candle_count
        self.iter_info = None

    def __iter__(self):
        resp = accounts.get()
        account_id = resp['accounts'][0]['id']

        resp = account.get(account_id)
        last_transaction_id = resp['lastTransactionID']

        self.iter_info = TradeInfo(account_id, last_transaction_id)

        return self

    @staticmethod
    def read_operation_mode():
        main = sys.modules['__main__']
        if not hasattr(main, '__file__'):
            return OperationMode.WATCH.name

        main_path = path.abspath(main.__file__)
        main_path_dir = path.dirname(main_path)
        operation_mode_path = path.join(main_path_dir, 'operation_mode.txt')

        with open(operation_mode_path, 'r') as f:
            key = f.readline().rstrip('\n')
            try:
                return OperationMode[key].name
            except KeyError as e:
                logging.warning('KeyError for operation mode setting: %s', e)

        return OperationMode.WATCH.name

    def __next__(self):
        self.iter_info.reset()

        self.iter_info.operation_mode = self.read_operation_mode()

        resp = account_changes.get(self.iter_info.account_id, self.iter_info.last_transaction_id)
        self.iter_info.last_transaction_id = resp['lastTransactionID']

        logging.info('NAV: %s', resp['state']['NAV'])

        resp = open_trades.get(self.iter_info.account_id)
        trades = resp['trades']

        if trades:
            trade = trades[0]

            self.iter_info.trade_id = trade['id']
            if trade['initialUnits'] > 0:
                self.iter_info.order_direction = OrderDirection.LONG.name
            else:
                self.iter_info.order_direction = OrderDirection.SHORT.name

            logging.info('Open: time=>%s unrealizedPL=>%s price=>%s units=>%s', trade['open'], trade['unrealizedPL'],
                         trade['price'], trade['initialUnits'])

        resp = candles.get(granularity=self.candle_type, count=self.candle_count)
        df = pd.DataFrame(resp['candles'])
        candles_df = pd.DataFrame([x for x in df['mid']])
        self.iter_info.candles_df = candles_df

        logging.info('Price: time=>%s close=>%s', df.iloc[-1]['time'], candles_df.iloc[-1]['c'])

        self.iter_info.indicator_value = self.indicator.get(self.iter_info.candles_df)

        return self.iter_info
