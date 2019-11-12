import pickle

import numpy as np
import pandas as pd

from .abstract_progress_builder import AbstractProgressBuilder


def dict_list_appender(x, y):
    for key, value in y.items():
        if key not in x:
            x[key] = [value]
        else:
            x[key].append(value)
    return x


class TradeProgressBuilder(AbstractProgressBuilder):

    def __init__(self, recorders):
        super().__init__()
        self.recorders = recorders
        self.dict_list_appender = np.frompyfunc(dict_list_appender, 2, 1)

    def entry(self, material):
        for recorder in self.recorders:
            recorder.entry(material)

    def progress(self, material):
        for recorder in self.recorders:
            recorder.progress(material)

    def exit(self, material):
        for recorder in self.recorders:
            recorder.exit(material)

    def build(self):
        records = []
        for recorder in self.recorders:
            if recorder.is_series_record:
                record = pd.Series([pd.DataFrame(x) for x in recorder.build()])
                record.describe(include='all')
            else:
                record = pd.DataFrame(self.dict_list_appender.reduce(recorder.build(), initial={}))

            records.append(record)

        return records

    def dump(self, dump_file_path):
        records = self.build()
        with open(dump_file_path, mode='wb') as f:
            pickle.dump(records, f)

    @staticmethod
    def load(load_file_path):
        with open(load_file_path, mode='rb') as f:
            return pickle.load(f)
