import dash_bootstrap_components as dbc
import dash_html_components as html
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from ..progress_recorder import ADXRecorder, CandleRecorder, MACDRecorder


class ProgressViewCreator:

    def __init__(self, recorders):
        self.recorders = recorders
        self.index_for_graph = [i for i, x in enumerate(recorders) if x.is_series_record]
        self.index_for_table = [i for i, x in enumerate(recorders) if not x.is_series_record]

    def series_figure(self, records):
        rows = len(self.index_for_graph)
        fig = make_subplots(rows=rows, cols=1, shared_xaxes=True, vertical_spacing=0.02)

        row = 1
        for i in self.index_for_graph:
            r = records[i]
            recorder = self.recorders[i]

            if isinstance(recorder, CandleRecorder):
                candle = go.Candlestick(
                    x=r.index, open=r['open'], high=r['high'], low=r['low'], close=r['close'], name='S5')
                fig.add_trace(candle, row=row, col=1)

            if isinstance(recorder, MACDRecorder):
                macd = go.Scatter(x=r.index, y=r[recorder.macd_key], name=recorder.macd_key)
                signal = go.Scatter(x=r.index, y=r[recorder.signal_key], name=recorder.signal_key)
                fig.add_trace(macd, row=row, col=1)
                fig.add_trace(signal, row=row, col=1)

            if isinstance(recorder, ADXRecorder):
                adx = go.Scatter(x=r.index, y=r[recorder.adx_key], name=recorder.adx_key)
                plus_di = go.Scatter(x=r.index, y=r[recorder.plus_di_key], name=recorder.plus_di_key)
                minus_di = go.Scatter(x=r.index, y=r[recorder.minus_di_key], name=recorder.minus_di_key)
                fig.add_trace(adx, row=row, col=1)
                fig.add_trace(plus_di, row=row, col=1)
                fig.add_trace(minus_di, row=row, col=1)

            row += 1

        fig.update_layout(height=800, xaxis_rangeslider_visible=False)
        return fig

    @staticmethod
    def __format(value):
        if isinstance(value, float):
            return '{:.3f}'.format(value)
        else:
            return value

    def table(self, records):
        header = []
        body = []
        for i in self.index_for_table:
            keys = records[i].keys()
            header += [html.Th(key) for key in keys]
            body += [html.Td(self.__format(records[i][key])) for key in keys]

        return dbc.Table([html.Tr(header), html.Tr(body)], bordered=True, size='sm', style={'width': '700px'},
                         className='ml-2 mb-2 mr-2 mt-1')
