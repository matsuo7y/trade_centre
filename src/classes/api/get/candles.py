from enum import Enum

from .abstract_get_client import AbstractGetClient

from ..deserializer import Deserializer


class CandleType(Enum):
    S10 = 1
    M1 = 2
    M30 = 3
    H1 = 4
    H4 = 5
    D = 6


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
                candle['time'] = Deserializer.unix_time_int(candle['time'])
                if 'bid' in candle:
                    deserialize_candle(candle['bid'])
                if 'ask' in candle:
                    deserialize_candle(candle['ask'])
                if 'mid' in candle:
                    deserialize_candle(candle['mid'])
        return resp

    def get(self, instrument='USD_JPY', price='M', granularity=CandleType.S10.name, count=500,
            alignment_timezone='Asia/Tokyo'):
        path_query = {'instrument': instrument}
        params = {
            'granularity': granularity,
            'price': price,
            'count': count,
            'alignmentTimezone': alignment_timezone
        }
        return self.exec(path_query=path_query, params=params)
