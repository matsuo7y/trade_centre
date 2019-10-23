import pandas as pd

from ..api import CandleType
from ..api.get import account, accounts, candles, open_trades


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

        resp = account.get(account_id)
        last_transaction_id = resp['lastTransactionID']

        self.material = TradeMaterial(account_id, last_transaction_id)

        resp = open_trades.get(account_id)
        if resp['trades']:
            self.material.trade_id = resp['trades'][0]['id']

        return self

    def __next__(self):
        resp = candles.get(granularity=self.candle_type, count=self.candle_count)
        df = pd.DataFrame(resp['candles'])

        self.material.candles_df = pd.DataFrame([x for x in df['mid']])
        self.material.indicator_value = self.indicator.get(self.material.candles_df)

        return self.material
