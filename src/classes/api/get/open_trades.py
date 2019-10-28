from .abstract_get_client import AbstractGetClient
from ..deserializer import Deserializer


class OpenTrades(AbstractGetClient):

    def __init__(self):
        super().__init__()

    def make_path(self, path_query=None):
        return '/accounts/{}/openTrades'.format(path_query['accountID'])

    def serialize_params(self, params):
        return params

    def deserialize_response(self, resp):
        key = 'trades'
        if key in resp:
            resp['lastTransactionID'] = Deserializer.number_id(resp['lastTransactionID'])
            for trade in resp[key]:
                trade['price'] = Deserializer.price(trade['price'])
                trade['openTime'] = Deserializer.formatted_time(trade['openTime'])
                trade['initialUnits'] = Deserializer.unit_int(trade['initialUnits'])
                trade['unrealizedPL'] = Deserializer.unit_float(trade['unrealizedPL'])
        return resp

    def get(self, account_id):
        path_query = {'accountID': account_id}
        return self.exec(path_query=path_query)
