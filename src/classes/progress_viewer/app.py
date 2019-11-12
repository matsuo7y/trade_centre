import dash
import dash_html_components as html
import dash_bootstrap_components as dbc

from .record_loader import RecordLoader
from .progress_view_creater import ProgressViewCreator
from ..config import PROGRESS_ABS_FILE_PATH
from ..trade_strategy import MACDADXTradeStrategy


def create_app(recorders):
    record_loader = RecordLoader(PROGRESS_ABS_FILE_PATH, recorders)
    progress_view_creator = ProgressViewCreator(recorders)

    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

    record_loader.initialize()

    record_loader.interval = 300
    records = record_loader.next()

    table = progress_view_creator.table(records)
    graph = progress_view_creator.graph(records)

    app.layout = html.Div(children=[
        html.Div(children=[
            dbc.Button('<<', color='info', className='ml-2 mr-2'),
            dbc.Button('<', color='secondary', className='mr-2'),
            dbc.Input(id='interval', type='number', value=10, min=1, max=1000, step=1, style={'width': '80px'},
                      className='mr-2'),
            dbc.Badge('POS\n{}'.format(record_loader.current_pos), color='primary', style={'width': '40px'},
                      className='mr-2 text-wrap'),
            dbc.Badge('IDX\n{}'.format(record_loader.current_index), color='danger', style={'width': '40px'},
                      className='mr-2 text-wrap'),
            dbc.Button('>', color='secondary', className='mr-2'),
            dbc.Button('>>', color='info', className='mr-2'),
        ], className='d-flex flex-row justify-content-center p-2'),
        html.Div(children=[table], className='d-flex flex-row justify-content-center'),
        graph
    ], className='bg-light')

    return app


def start_progress_view():
    strategy = MACDADXTradeStrategy(is_test=True)
    app = create_app(strategy.get_progress_recorders())
    app.run_server(debug=True)
