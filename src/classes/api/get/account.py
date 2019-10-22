from .abstract_get_client import AbstractGetClient
from ..deserializer import Deserializer


class Account(AbstractGetClient):

    def __init__(self):
        super().__init__()

    def make_path(self, path_query=None):
        return '/accounts/{}'.format(path_query['accountID'])

    def serialize_params(self, params):
        return params

    def deserialize_response(self, resp):
        key = 'lastTransactionID'
        if key in resp:
            resp[key] = Deserializer.number_id(resp[key])
        return resp

    def get(self, account_id):
        path_query = {'accountID': account_id}
        return self.exec(path_query=path_query)
