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

        self.position_recorder_index = position_recorder_index
        self.sorted_index = []
        self.current_pos = 0
        self.current_index = 0
        self.interval = 1

    def __get(self):
        self.current_index = self.sorted_index[self.current_pos]
        return [x.iloc[self.current_index] for x in self.records]

    def initialize(self, sort_key='profit'):
        position_record = self.records[self.position_recorder_index]
        self.sorted_index = position_record.sort_values(sort_key).index.to_numpy().tolist()
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
