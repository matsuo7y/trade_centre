from abc import *

import requests

from ..abstract_client import AbstractClient


class AbstractPostClient(AbstractClient, ABC):

    def __init__(self):
        super().__init__()

    def make_request(self, path, params=None, data=None):
        return requests.post(path, headers=self.headers, data=data)

    def serialize_params(self, params):
        pass
