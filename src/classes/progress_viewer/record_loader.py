import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from ..progress_recorder import PositionRecorder, TradeProgressBuilder, MACDRecorder, ADXRecorder, ROCRecorder


class RecordLoader:

    def __init__(self, file_path, recorders):
        self.records = TradeProgressBuilder.load(file_path)
        self.recorders = recorders

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

    def __get_start_records(self, recorder_class, key):
        index = None
        for i in range(len(self.recorders)):
            if isinstance(self.recorders[i], recorder_class):
                index = i
                break

        record = self.records[index]
        return [abs(x.iloc[47][key]) for x in record]

    def print_quad_sign_trade_strategy_statistics(self):
        macd_start_record = self.__get_start_records(MACDRecorder, 'macd1')
        adx_start_record = self.__get_start_records(ADXRecorder, 'adx')
        roc_start_record = self.__get_start_records(ROCRecorder, 'roc')

        fig = make_subplots(rows=3, cols=2)

        profit_macd = go.Scatter(
            x=self.position_record.profit, y=macd_start_record, mode='markers')
        max_profit_macd = go.Scatter(
            x=self.position_record.max_profit, y=macd_start_record, mode='markers')

        profit_adx = go.Scatter(
            x=self.position_record.profit, y=adx_start_record, mode='markers')
        max_profit_adx = go.Scatter(
            x=self.position_record.max_profit, y=adx_start_record, mode='markers')

        profit_roc = go.Scatter(
            x=self.position_record.profit, y=roc_start_record, mode='markers')
        max_profit_roc = go.Scatter(
            x=self.position_record.max_profit, y=roc_start_record, mode='markers')

        fig.add_trace(profit_macd, row=1, col=1)
        fig.add_trace(max_profit_macd, row=1, col=2)
        fig.add_trace(profit_adx, row=2, col=1)
        fig.add_trace(max_profit_adx, row=2, col=2)
        fig.add_trace(profit_roc, row=3, col=1)
        fig.add_trace(max_profit_roc, row=3, col=2)

        fig.show()

        df_profit_macd = pd.DataFrame(dict(profit=self.position_record.profit, macd=macd_start_record))

        print(df_profit_macd[df_profit_macd.macd <= 0.005].describe(include='all'))
        print(df_profit_macd[df_profit_macd.macd > 0.005].describe(include='all'))

        df_max_profit_macd = pd.DataFrame(dict(profit=self.position_record.max_profit, macd=macd_start_record))

        print(df_max_profit_macd[df_profit_macd.macd <= 0.005].describe(include='all'))
        print(df_max_profit_macd[df_profit_macd.macd > 0.005].describe(include='all'))
