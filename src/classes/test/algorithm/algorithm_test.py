from .tester import AlgorithmTester
from ...config import CANDLES_ABS_FILE_PATH, PROGRESS_ABS_FILE_PATH
from ...trade_strategy import MACDADXTradeStrategy


def algorithm_test():
    tester = AlgorithmTester(
        CANDLES_ABS_FILE_PATH, strategy=MACDADXTradeStrategy(is_test=True), start=-100000, window_size=500,
        dump_file_path=PROGRESS_ABS_FILE_PATH)

    tester.work()
