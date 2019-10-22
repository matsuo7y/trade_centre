import logging

from ..api.get import account_changes, accounts, account, candles


def api_test():
    resp = accounts.get()
    logging.info('accounts: %s', resp)

    account_id = resp['accounts'][0]['id']

    resp = account.get(account_id)
    logging.info('account: %s', resp)

    last_transaction_id = resp['lastTransactionID']

    resp = account_changes.get(account_id, last_transaction_id)
    logging.info('account_changes: %s', resp)

    resp = candles.get(count=2)
    logging.info('candles: %s', resp)
