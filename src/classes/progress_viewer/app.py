import dash
import dash_html_components as html

from .record_loader import RecordLoader
from .progress_view_creater import ProgressViewCreator
from ..config import PROGRESS_ABS_FILE_PATH
from ..trade_strategy import MACDADXTradeStrategy


def create_app(recorders):
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    record_loader = RecordLoader(PROGRESS_ABS_FILE_PATH, recorders)
    progress_view_creator = ProgressViewCreator(recorders)

    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    record_loader.initialize()

    record_loader.interval = 300
    records = record_loader.next()

    table = progress_view_creator.table(records)
    graph = progress_view_creator.graph(records)

    app.layout = html.Div(children=[
        # html.H4(children='Pos:{} Index:{}'.format(record_loader.current_pos, record_loader.current_index)),
        table,
        graph
    ])

    return app


def start_progress_view():
    strategy = MACDADXTradeStrategy(is_test=True)
    app = create_app(strategy.get_progress_recorders())
    app.run_server(debug=True)
