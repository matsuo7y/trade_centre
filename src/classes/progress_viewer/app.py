from .progress_view_application import ProgressViewApplication
from ..trade_strategy import DualMACDTradeStrategy


def progress_view(web=True):
    strategy = DualMACDTradeStrategy(is_test=True)
    app = ProgressViewApplication(strategy.get_progress_recorders())

    if web:
        app.start_web()
    else:
        app.summary()
