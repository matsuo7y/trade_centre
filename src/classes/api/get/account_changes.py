from .abstract_get_client import AbstractGetClient
from ..deserializer import Deserializer


class AccountChanges(AbstractGetClient):

    def __init__(self):
        super().__init__()

    def make_path(self, path_query=None):
        key = 'account_id'
        if key not in path_query:
            raise ValueError('no account_id')
        return '/accounts/{}/changes'.format(path_query[key])

    def serialize_params(self, params):
        pass

    def deserialize_response(self, resp):
        key = 'lastTransactionID'
        if key in resp:
            i = resp[key]
            resp[key] = Deserializer.number_id(i)
        return resp

    def get(self, account_id):
        return self.exec(path_query={'account_id': account_id})
