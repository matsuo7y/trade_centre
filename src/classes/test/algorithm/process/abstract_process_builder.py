from abc import *


class AbstractProcessBuilder(ABC):

    def __init__(self):
        self.num_entry = 0
        self.num_exit = 0

    def entry(self, position, indicator_value):
        self.num_entry += 1
        self._entry(position, indicator_value)

    def exit(self, position, indicator_value):
        self.num_exit += 1
        self._exit(position, indicator_value)

    @abstractmethod
    def _entry(self, position, indicator_value):
        raise NotImplementedError()

    @abstractmethod
    def _exit(self, position, indicator_value):
        raise NotImplementedError()

    @abstractmethod
    def build(self):
        raise NotImplementedError
