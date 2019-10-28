from enum import Enum

from .abstract_post_client import AbstractPostClient
from ..serializer import Serializer
from ..deserializer import Deserializer


class OrderType(Enum):
    MARKET = 1
    STOP = 2
    LIMIT = 3
    TAKE_PROFIT = 4
    STOP_LOSS = 5


class OrderDirection(Enum):
    LONG = 1
    SHORT = 2


class Order(AbstractPostClient):

    def __init__(self):
        super().__init__()

    def make_path(self, path_query=None):
        return '/accounts/{}/orders'.format(path_query['accountID'])

    def serialize_data(self, data):
        data['order']['units'] = Serializer.unit(data['order']['units'])
        return data

    def deserialize_response(self, resp):
        key = 'lastTransactionID'
        if key in resp:
            resp[key] = Deserializer.number_id(resp[key])
        return resp

    def post(self, account_id, direction=OrderDirection.LONG.name, order_type=OrderType.MARKET.name,
             instrument='USD_JPY', units=1000):
        path_query = {'accountID': account_id}
        data = {
            'order': {
                'type': order_type,
                'instrument': instrument,
                'units': abs(units) if direction == OrderDirection.LONG.name else -abs(units)
            }
        }
        return self.exec(path_query=path_query, data=data, retry_count=-1)
