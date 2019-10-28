from .abstract_put_client import AbstractPutClient
from ..deserializer import Deserializer


class CloseTrade(AbstractPutClient):

    def __init__(self):
        super().__init__()

    def make_path(self, path_query=None):
        return '/accounts/{}/trades/{}/close'.format(path_query['accountID'], path_query['tradeID'])

    def serialize_data(self, data):
        return data

    def deserialize_response(self, resp):
        key = 'lastTransactionID'
        if key in resp:
            resp[key] = Deserializer.number_id(resp[key])
        return resp

    def put(self, account_id, trade_id):
        path_query = {'accountID': account_id, 'tradeID': trade_id}
        return self.exec(path_query=path_query, retry_count=-1)
