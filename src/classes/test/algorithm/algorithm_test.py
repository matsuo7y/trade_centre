from ...trade_strategy import MACDADXTradeStrategy
from ...config import CANDLES_ABS_FILE_PATH
from .tester import AlgorithmTester


def algorithm_test():
    tester = AlgorithmTester(CANDLES_ABS_FILE_PATH, strategy=MACDADXTradeStrategy(is_test=True), start=-100000,
                             window_size=500)

    tester.work()
    tester.process_builder.build()
