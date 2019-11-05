from ..progress_recorder import TradeProgressBuilder


class RecordLoader:

    def __init__(self, file_path):
        record = TradeProgressBuilder.load(file_path)
        self.moment_record = record['moment']
        self.series_record = record['series']
        self.sorted_index = []
        self.current_pos = 0
        self.interval = 1

    def __get(self):
        index = self.sorted_index[self.current_pos]
        return self.moment_record[index], self.series_record[index]

    def initialize(self, sort_key='profit'):
        self.sorted_index = self.moment_record.sort_values(sort_key).index.to_numpy().tolist()
        self.current_pos = 0

    def first(self):
        self.current_pos = 0
        return self.__get()

    def next(self):
        self.current_pos += self.interval
        if self.current_pos >= len(self.sorted_index):
            self.current_pos = -1
        return self.__get()

    def last(self):
        self.current_pos = -1
        return self.__get()
