import pandas as pd

from ..progress_recorder import PositionRecorder, TradeProgressBuilder


class RecordLoader:

    def __init__(self, file_path, recorders):
        self.records = TradeProgressBuilder.load(file_path)

        position_recorder_index = None
        for i, recorder in enumerate(recorders):
            if isinstance(recorder, PositionRecorder):
                position_recorder_index = i
                break

        if position_recorder_index is None:
            raise ValueError('No Position Recorder included')

        self.position_record = self.records[position_recorder_index]
        self.sorted_index = []
        self.current_pos = 0
        self.current_index = 0
        self.last_index = 0
        self.interval = 10

    def __get(self):
        self.current_index = self.sorted_index[self.current_pos]
        return [x.iloc[self.current_index] for x in self.records]

    def initialize(self, sort_key='profit'):
        self.sorted_index = self.position_record.sort_values(sort_key).index.to_numpy().tolist()
        self.current_pos = 0
        self.last_index = len(self.sorted_index) - 1

    def first(self):
        self.current_pos = 0
        return self.__get()

    def next(self):
        self.current_pos += self.interval
        if self.current_pos > self.last_index:
            self.current_pos = self.last_index
        return self.__get()

    def prev(self):
        self.current_pos -= self.interval
        if self.current_pos < 0:
            self.current_pos = 0
        return self.__get()

    def last(self):
        self.current_pos = self.last_index
        return self.__get()

    def print_position_summary(self):
        print(self.position_record.describe(include='all'))

    def print_optimized_summary(self):
        max_limit = self.position_record.max_profit.max()
        min_stop_loss = self.position_record.profit.min()

        step = 0.01
        limits = []
        stop_losses = []
        average_profits = []
        for i, limit in enumerate([k * step for k in range(1, int(abs(max_limit) / step))]):
            for j, stop_loss in enumerate([-k * step for k in range(81, int(abs(min_stop_loss) / step))]):
                profits = []
                for position in self.position_record.itertuples():
                    if position.max_profit > limit:
                        profits.append(limit)
                    elif position.min_profit < stop_loss:
                        profits.append(stop_loss)
                    else:
                        profits.append(position.profit)

                limits.append(limit)
                stop_losses.append(stop_loss)
                average_profits.append(sum(profits) / len(profits))

                if i % 100 == 0 and j % 100 == 0:
                    print('progress: {}, {}'.format(i, j))

        results = pd.DataFrame(dict(limit=limits, stop_loss=stop_losses, profit=average_profits))
        results = results.sort_values('profit', ascending=False)

        print(results)
