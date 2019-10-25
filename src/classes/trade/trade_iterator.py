import logging

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

    def reset(self):
        self.last_transaction_id = None
        self.trade_id = None
        self.order_direction = None
        self.candles_df = None
        self.indicator_value = None


class TradeIterator:

    def __init__(self, indicator, candle_type=CandleType.S10.name, candle_count=500):
        self.indicator = indicator
        self.candle_type = candle_type
        self.candle_count = candle_count
        self.iter_info = None

    def __iter__(self):
        resp = accounts.get()
        account_id = resp['accounts'][0]['id']

        resp = account.get(self.iter_info.account_id)
        last_transaction_id = resp['lastTransactionID']

        self.iter_info = TradeInfo(account_id, last_transaction_id)

        return self

    def __next__(self):
        self.iter_info.reset()

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

        logging.info('Price: time=>%s close=>%s', df.iloc[-1, 'time'], candles_df.iloc[-1, 'c'])

        self.iter_info.indicator_value = self.indicator.get(self.iter_info.candles_df)

        return self.iter_info
