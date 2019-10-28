import json
import logging
from abc import *

from ..config import OANDA_DOMAIN, OANDA_TOKEN, OANDA_VERSION


def success(code):
    return 200 <= code < 300


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

    def exec(self, path_query=None, params=None, data=None, retry_count=1):
        path = self.make_path(path_query=path_query)
        url = '{}{}'.format(self.base_url, path)

        if params is not None:
            params = self.serialize_params(params)

        if data is not None:
            data = self.serialize_data(data)

        resp = None
        while retry_count:
            resp = self.make_request(url=url, params=params, data=json.dumps(data))
            if success(resp.status_code):
                return self.deserialize_response(resp.json())

            logging.warning(resp.json())
            if retry_count > 0:
                retry_count -= 1

        raise ValueError(resp.json())
