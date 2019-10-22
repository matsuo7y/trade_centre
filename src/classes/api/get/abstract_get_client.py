from abc import *

import requests

from ..abstract_client import AbstractClient


class AbstractGetClient(AbstractClient, ABC):

    def __init__(self):
        super().__init__()

    def make_request(self, url, params=None, data=None):
        return requests.get(url, params=params, headers=self.headers)

    def serialize_data(self, data):
        pass
