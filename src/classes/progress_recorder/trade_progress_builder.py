import pickle

import numpy as np
import pandas as pd

from .abstract_progress_builder import AbstractProgressBuilder


def dict_updater(x, y):
    x.update(y)
    return x


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
        self.dict_updater = np.frompyfunc(dict_updater, 2, 1)
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

    def _build(self, recorders):
        records = [x.build() for x in recorders]

        if records:
            records = np.array(records)
            return self.dict_updater.reduce(records, axis=0)

        return None

    def build(self):
        records = self._build([x for x in self.recorders if x.is_series_record])
        if records is not None:
            series_records = pd.Series([pd.DataFrame(x) for x in records])
        else:
            series_records = None

        records = self._build([x for x in self.recorders if not x.is_series_record])
        if records is not None:
            moment_records = pd.DataFrame(self.dict_list_appender.reduce(records, initial={}))
        else:
            moment_records = None

        return dict(moment=moment_records, series=series_records)

    def dump(self, dump_file_path):
        records = self.build()
        with open(dump_file_path, mode='wb') as f:
            pickle.dump(records, f)

        return records

    @staticmethod
    def load(load_file_path):
        with open(load_file_path, mode='rb') as f:
            return pickle.load(f)
