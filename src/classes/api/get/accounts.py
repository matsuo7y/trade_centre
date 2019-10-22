from .abstract_get_client import AbstractGetClient


class Accounts(AbstractGetClient):

    def __init__(self):
        super().__init__()

    def make_path(self, path_query=None):
        return '/accounts'

    def serialize_params(self, params):
        return params

    def deserialize_response(self, resp):
        return resp

    def get(self):
        return self.exec()
