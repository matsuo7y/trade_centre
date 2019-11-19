from .tester import AlgorithmTester
from ...config import CANDLES_ABS_FILE_PATH, PROGRESS_ABS_FILE_PATH
from ...trade_strategy import QuadSignTradeStrategy


def algorithm_test():
    strategy = QuadSignTradeStrategy(is_test=True)
    tester = AlgorithmTester(
        CANDLES_ABS_FILE_PATH, strategy=strategy, start=-400000, window_size=500, dump_file_path=PROGRESS_ABS_FILE_PATH)

    tester.work()
