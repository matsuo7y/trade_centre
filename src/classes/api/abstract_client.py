import json
from abc import *

from ..config import OANDA_DOMAIN, OANDA_TOKEN, OANDA_VERSION


class AbstractClient(ABC):

    def __init__(self):
        self.base_url = 'https://{}.oanda.com/{}'.format(OANDA_DOMAIN, OANDA_VERSION)
        self.headers = {
            'Authorization': 'Bearer {}'.format(OANDA_TOKEN),
            'Connection': 'Keep-Alive',
            'Content-Type': 'application/json',
            'Accept-Datetime-Format': 'UNIX'
        }

    @abstractmethod
    def make_path(self, path_query=None):
        raise NotImplementedError()

    @abstractmethod
    def make_request(self, url, params=None, data=None):
        raise NotImplementedError()

    @abstractmethod
    def serialize_params(self, params):
        raise NotImplementedError()

    @abstractmethod
    def serialize_data(self, data):
        raise NotImplementedError()

    @abstractmethod
    def deserialize_response(self, resp):
        raise NotImplementedError()

    def exec(self, path_query=None, params=None, data=None):
        path = self.make_path(path_query=path_query)
        url = '{}{}'.format(self.base_url, path)

        if params is not None:
            params = self.serialize_params(params)

        if data is not None:
            data = self.serialize_data(data)

        resp = self.make_request(url=url, params=params, data=data)
        return self.deserialize_response(resp.json())
