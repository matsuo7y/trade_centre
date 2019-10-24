import pandas as pd
import logging

from ..api import CandleType
from ..api.get import account, accounts, account_changes, candles, open_trades


class TradeMaterial:

    def __init__(self, account_id, last_transaction_id):
        self.account_id = account_id
        self.last_transaction_id = last_transaction_id
        self.trade_id = None
        self.candles_df = None
        self.indicator_value = None


class TradeIterator:

    def __init__(self, indicator, candle_type=CandleType.S10.name, candle_count=500):
        self.indicator = indicator
        self.candle_type = candle_type
        self.candle_count = candle_count
        self.material = None

    def __iter__(self):
        resp = accounts.get()
        account_id = resp['accounts'][0]['id']

        resp = account.get(self.material.account_id)
        last_transaction_id = resp['lastTransactionID']

        self.material = TradeMaterial(account_id, last_transaction_id)

        return self

    def __next__(self):
        resp = account_changes.get(self.material.account_id, self.material.last_transaction_id)
        self.material.last_transaction_id = resp['lastTransactionID']

        logging.info('NAV: %s', resp['state']['NAV'])

        resp = open_trades.get(self.material.account_id)
        self.material.trade_id = resp['trades'][0]['id'] if resp['trades'] else None

        if self.material.trade_id is not None:
            trade = resp['trades'][0]
            logging.info('Open: time=>%s unrealizedPL=>%s price=>%s units=>%s', trade['open'], trade['unrealizedPL'],
                         trade['price'], trade['initialUnits'])

        resp = candles.get(granularity=self.candle_type, count=self.candle_count)
        df = pd.DataFrame(resp['candles'])
        candles_df = pd.DataFrame([x for x in df['mid']])
        self.material.candles_df = candles_df

        logging.info('Price: time=>%s close=>%s', df.iloc[-1, 'time'], candles_df.iloc[-1, 'c'])

        indicator_value = self.indicator.get(self.material.candles_df)
        self.material.indicator_value = indicator_value

        logging.info('Indicator: value=>%s material=>%s', indicator_value.value, indicator_value.material)

        return self.material
