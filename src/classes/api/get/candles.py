from enum import Enum

from .abstract_get_client import AbstractGetClient

from ..deserializer import Deserializer


class CandleType(Enum):
    S5 = 1
    S10 = 2
    M1 = 3
    M15 = 4
    H1 = 5
    H4 = 6
    D = 7


def deserialize_candle(candle):
    for key in ['o', 'h', 'l', 'c']:
        candle[key] = Deserializer.price(candle[key])


class Candles(AbstractGetClient):

    def __init__(self):
        super().__init__()

    def make_path(self, path_query=None):
        return '/instruments/{}/candles'.format(path_query['instrument'])

    def serialize_params(self, params):
        return params

    def deserialize_response(self, resp):
        key = 'candles'
        if key in resp:
            for candle in resp[key]:
                candle['time'] = Deserializer.formatted_time(candle['time'])
                if 'bid' in candle:
                    deserialize_candle(candle['bid'])
                if 'ask' in candle:
                    deserialize_candle(candle['ask'])
                if 'mid' in candle:
                    deserialize_candle(candle['mid'])
        return resp

    def get(self, instrument='USD_JPY', price='M', granularity=CandleType.S5.name, count=500,
            alignment_timezone='Asia/Tokyo'):
        path_query = {'instrument': instrument}
        params = {
            'granularity': granularity,
            'price': price,
            'count': count,
            'alignmentTimezone': alignment_timezone
        }
        return self.exec(path_query=path_query, params=params)
