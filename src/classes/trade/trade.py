from .trader import Trader
from ..trade_strategy import MACDADXTradeStrategy


def trade():
    Trader(strategy=MACDADXTradeStrategy()).work()
