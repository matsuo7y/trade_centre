import pandas as pd
from ....indicator import IndicatorBuilder


class TestIterator:

    def __init__(self, candles_file_path, indicators, start=-10000, end=-1, window_size=4000):
        df = pd.read_csv(candles_file_path)
        self.df = df.iloc[start:end, :]
        self.window_size = window_size
        self.current = 0
        self.indicators = indicators

    def __iter__(self):
        return self

    def __next__(self):
        length = len(self.df.index)

        end = self.current + self.window_size
        if end > length:
            raise StopIteration()

        df = self.df.iloc[self.current:end, :]
        self.current += 1

        indicator_value_builder = IndicatorBuilder()
        for indicator_type, indicator in self.indicators.items():
            indicator_value_builder.add(indicator_type, indicator.get(df))

        return indicator_value_builder.build(), end - 1
