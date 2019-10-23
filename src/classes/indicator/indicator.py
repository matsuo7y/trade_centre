from abc import *


class Indicator(ABC):

    @abstractmethod
    def get(self, df):
        raise NotImplementedError()
