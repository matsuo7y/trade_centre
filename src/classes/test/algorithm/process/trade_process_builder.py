import pickle

import pandas as pd

from .abstract_process_builder import AbstractProcessBuilder


class TradeProcessBuilder(AbstractProcessBuilder):
    loss = 0
    profit = 1

    def __init__(self, indicator_process_builders=None):
        super().__init__()

        if indicator_process_builders is None:
            indicator_process_builders = {}

        self.indicator_process_builders = indicator_process_builders
        self.directions = []
        self.profits = []
        self.pls = []
        self.position_times = []

    def _entry(self, position, indicator_values):
        self.directions.append(position.order_direction)

        for indicator_type, indicator_process_builder in self.indicator_process_builders.items():
            indicator_value = indicator_values[indicator_type]
            indicator_process_builder.entry(position, indicator_value)

    def _exit(self, position, indicator_values):
        self.profits.append(position.profit_pips)
        self.position_times.append(position.time)
        profit_loss = self.profit if position.profit_pips > 0 else self.loss
        self.pls.append(profit_loss)

        for indicator_type, indicator_process_builder in self.indicator_process_builders.items():
            indicator_value = indicator_values[indicator_type]
            indicator_process_builder.exit(position, indicator_value)

    def build(self):
        if self.num_entry > self.num_exit:
            self.directions = self.directions[:self.num_exit]

        data = {
            'direction': self.directions,
            'profit': self.profits,
            'profit_loss': self.pls,
            'position_time': self.position_times
        }

        for indicator_process_builder in self.indicator_process_builders.values():
            data.update(indicator_process_builder.build())

        df = pd.DataFrame(data)
        print(df.describe(include='all'))
        return df

    def dump(self, dump_file_path):
        df = self.build()
        with open(dump_file_path, mode='wb') as f:
            pickle.dump(df, f)

    def load(self, dump_file_path):
        with open(dump_file_path, mode='rb') as f:
            df = pickle.load(f)
            return df
