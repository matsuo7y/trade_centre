from .abstract_get_client import AbstractGetClient
from ..deserializer import Deserializer
from ..serializer import Serializer


class AccountChanges(AbstractGetClient):

    def __init__(self):
        super().__init__()

    def make_path(self, path_query=None):
        return '/accounts/{}/changes'.format(path_query['accountID'])

    def serialize_params(self, params):
        key = 'sinceTransactionID'
        params[key] = Serializer.number_id(params[key])
        return params

    def deserialize_response(self, resp):
        key = 'lastTransactionID'
        if key in resp:
            resp[key] = Deserializer.number_id(resp[key])

        key = 'state'
        if key in resp:
            resp[key]['NAV'] = Deserializer.unit_float(resp[key]['NAV'])

        return resp

    def get(self, account_id, since_transaction_id):
        path_query = {'accountID': account_id}
        params = {'sinceTransactionID': since_transaction_id}
        return self.exec(path_query=path_query, params=params)
