import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from .progress_view_creater import ProgressViewCreator
from .record_loader import RecordLoader
from ..config import PROGRESS_ABS_FILE_PATH
from ..trade_strategy import MACDADXTradeStrategy


def start_app(recorders):
    record_loader = RecordLoader(PROGRESS_ABS_FILE_PATH, recorders)
    progress_view_creator = ProgressViewCreator(recorders)

    record_loader.initialize()
    records = record_loader.first()

    table = progress_view_creator.table(records)
    fig = progress_view_creator.series_figure(records)

    def pos():
        return 'POS\n{}'.format(record_loader.current_pos)

    def idx():
        return 'IDX\n{}'.format(record_loader.current_index)

    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

    app.layout = html.Div(children=[
        html.Div(children=[
            dbc.Button('<<', id='first', color='info', className='ml-2 mr-2'),
            dbc.Button('<', id='decrease', color='secondary', className='mr-2'),
            dbc.Input(id='interval', type='number', value=record_loader.interval, min=1, max=1000, step=1,
                      style={'width': '80px'}, className='mr-2'),
            dbc.Badge(children=pos(), id='pos', color='primary', style={'width': '40px'}, className='mr-2 text-wrap'),
            dbc.Badge(children=idx(), id='idx', color='danger', style={'width': '40px'}, className='mr-2 text-wrap'),
            dbc.Button('>', id='increase', color='secondary', className='mr-2'),
            dbc.Button('>>', id='last', color='info', className='mr-2'),
        ], className='d-flex flex-row justify-content-center p-2'),

        html.Div(id='table', children=table, className='d-flex flex-row justify-content-center'),

        dcc.Graph(id='graph', figure=fig, className='mt-0')
    ], className='bg-light')

    @app.callback(
        [Output('table', 'children'),
         Output('graph', 'figure'),
         Output('pos', 'children'),
         Output('idx', 'children')],

        [Input('first', 'n_clicks'),
         Input('decrease', 'n_clicks'),
         Input('increase', 'n_clicks'),
         Input('last', 'n_clicks')],

        [State('interval', 'value')]
    )
    def update(_a, _b, _c, _d, interval):
        ctx = dash.callback_context

        if not ctx.triggered:
            return

        clicked = ctx.triggered[0]['prop_id'].split('.')[0]

        if clicked == 'first':
            _records = record_loader.first()
        elif clicked == 'decrease':
            record_loader.interval = interval
            _records = record_loader.prev()
        elif clicked == 'increase':
            record_loader.interval = interval
            _records = record_loader.next()
        else:
            _records = record_loader.last()

        _table = progress_view_creator.table(_records)
        _fig = progress_view_creator.series_figure(_records)

        return _table, _fig, pos(), idx()

    app.run_server(debug=True)


def start_progress_view():
    strategy = MACDADXTradeStrategy(is_test=True)
    start_app(strategy.get_progress_recorders())
