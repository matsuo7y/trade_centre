from .progress_view_application import ProgressViewApplication
from ..trade_strategy import BBandMACDTradeStrategy


def progress_view(web=True):
    strategy = BBandMACDTradeStrategy(is_test=True)
    app = ProgressViewApplication(strategy.get_progress_recorders())

    if web:
        app.start_web()
    else:
        app.summary()
