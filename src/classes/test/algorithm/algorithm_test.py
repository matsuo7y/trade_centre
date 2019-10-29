from .tester import MACDADXAlgorithmTester
from ...config import CANDLES_ABS_FILE_PATH, PROCESS_ABS_FILE_PATH


def algorithm_test():
    tester = MACDADXAlgorithmTester(CANDLES_ABS_FILE_PATH, PROCESS_ABS_FILE_PATH, start=-100000, window_size=500)

    tester.work()
    tester.process_builder.build()
