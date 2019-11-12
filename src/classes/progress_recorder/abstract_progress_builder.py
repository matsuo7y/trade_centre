from abc import *


class AbstractProgressBuilder(ABC):

    @abstractmethod
    def entry(self, material):
        raise NotImplementedError()

    @abstractmethod
    def progress(self, material):
        raise NotImplementedError()

    @abstractmethod
    def exit(self, material):
        raise NotImplementedError()

    @abstractmethod
    def build(self):
        raise NotImplementedError
