from enum import Enum

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from ..progress_recorder import ADXRecorder, MACDRecorder, PositionRecorder, ROCRecorder, TradeProgressBuilder


class RecordExtractType(Enum):
    start = 1
    start_diff = 2
    sign_reverse_distance = 3


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

    @staticmethod
    def __sign_distance(values, key, sub_key):
        distance = 0
        start_diff = values.iloc[47][key] - values.iloc[47][sub_key]
        if start_diff == 0:
            return distance

        sign = 1 if start_diff > 0 else -1
        for i in range(46, 0, -1):
            if sign * (values.iloc[i][key] - values.iloc[i][sub_key]) > 0:
                continue
            distance = 47 - i
            break

        return distance

    def __get_start_records(self, recorder_class, key, sub_key=None, suffix=None,
                            extract_type=RecordExtractType.start.name,
                            sample_num=None):
        index = None
        for i in range(len(self.recorders)):
            if isinstance(self.recorders[i], recorder_class):
                if suffix is not None and self.recorders[i].suffix != suffix:
                    continue
                index = i
                break

        record = self.records[index]
        if extract_type == RecordExtractType.start.name:
            ret_value = [abs(x.iloc[47][key]) for x in record]
        elif extract_type == RecordExtractType.start_diff.name:
            ret_value = [abs(x.iloc[47][key] - x.iloc[46][key]) for x in record]
        else:
            ret_value = [self.__sign_distance(x, key, sub_key) for x in record]

        if sample_num is not None:
            ret_value = np.random.choice(ret_value, sample_num, replace=False)

        return ret_value

    def print_quad_sign_trade_strategy_statistics(self):
        macd_start_record = self.__get_start_records(MACDRecorder, 'macd1', suffix='1')
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

        # df_profit_macd = pd.DataFrame(dict(profit=self.position_record.profit, macd=macd_start_record))
        #
        # print(df_profit_macd[df_profit_macd.macd <= 0.004].describe(include='all'))
        # print(df_profit_macd[df_profit_macd.macd > 0.004].describe(include='all'))
        #
        # df_max_profit_macd = pd.DataFrame(dict(profit=self.position_record.max_profit, macd=macd_start_record))
        #
        # print(df_max_profit_macd[df_profit_macd.macd <= 0.004].describe(include='all'))
        # print(df_max_profit_macd[df_profit_macd.macd > 0.004].describe(include='all'))

    def print_dual_trade_strategy_statistics(self):
        macd_1_start_difference_record = self.__get_start_records(
            MACDRecorder, 'macd1', suffix='1', extract_type=RecordExtractType.start_diff.name, sample_num=400)
        macd_2_start_difference_record = self.__get_start_records(
            MACDRecorder, 'macd2', suffix='2', extract_type=RecordExtractType.start_diff.name, sample_num=400)

        fig = make_subplots(rows=1, cols=2)

        profit_macd_1_diff = go.Scatter(
            x=self.position_record.profit, y=macd_1_start_difference_record, mode='markers')
        profit_macd_2_diff = go.Scatter(
            x=self.position_record.max_profit, y=macd_2_start_difference_record, mode='markers')

        fig.add_trace(profit_macd_1_diff, row=1, col=1)
        fig.add_trace(profit_macd_2_diff, row=1, col=2)

        fig.show()

        # macd_1_sign_distance = self.__get_start_records(
        #     MACDRecorder, 'macd1', sub_key='signal1', suffix='1',
        #     extract_type=RecordExtractType.sign_reverse_distance.name)
        #
        # df_profit_macd_sign = pd.DataFrame(dict(profit=self.position_record.profit, distance=macd_1_sign_distance))
        #
        # print(df_profit_macd_sign[df_profit_macd_sign.distance == 1].describe(include='all'))
        # print(df_profit_macd_sign[df_profit_macd_sign.distance != 1].describe(include='all'))
        #
        # profit_macd_1_distance = go.Scatter(
        #     x=self.position_record.profit, y=macd_1_sign_distance, mode='markers')
        #
        # fig = go.Figure(data=[profit_macd_1_distance])
        #
        # fig.show()
