from .abstract_process_builder import AbstractProcessBuilder


class MACDProcessBuilder(AbstractProcessBuilder):
    def __init__(self, period=18):
        super().__init__()
        self.period = period
        self.macds = []
        self.signals = []

    def _entry(self, position, indicator_value):
        macd_signal = indicator_value.material[['macd', 'signal']].iloc[-self.period:, :]
        macd_signal.reset_index(inplace=True, drop=True)

        self.macds.append(macd_signal['macd'])
        self.signals.append(macd_signal['signal'])

    def _exit(self, position, indicator_value):
        pass

    def build(self):
        if self.num_entry > self.num_exit:
            self.macds = self.macds[:self.num_exit]
            self.signals = self.signals[:self.num_exit]

        return {
            'macd': self.macds,
            'signal': self.signals,
        }
