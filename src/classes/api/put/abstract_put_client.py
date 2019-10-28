from abc import *

import requests

from ..abstract_client import AbstractClient


class AbstractPutClient(AbstractClient, ABC):

    def __init__(self):
        super().__init__()

    def make_request(self, url, params=None, data=None):
        return requests.put(url, headers=self.headers, data=data)

    def serialize_params(self, params):
        pass
