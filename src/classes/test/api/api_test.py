import logging
import time

from ...api.get import account_changes, accounts, account, candles, open_trades
from ...api.post import order
from ...api.put import close_trade


def api_test():
    resp = accounts.get()
    logging.info('accounts: %s', resp)

    account_id = resp['accounts'][0]['id']

    resp = account.get(account_id)
    logging.info('account: %s', resp)

    last_transaction_id = resp['lastTransactionID']

    resp = candles.get(count=2)
    logging.info('candles: %s', resp)

    order.post(account_id)

    time.sleep(2)

    resp = open_trades.get(account_id)
    logging.info('open_trades: %s', resp)

    if resp['trades']:
        trade_id = resp['trades'][0]['id']
        close_trade.put(account_id, trade_id)

    resp = account_changes.get(account_id, last_transaction_id)
    logging.info('account_changes: %s', resp)
