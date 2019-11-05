from abc import *
from enum import Enum
from operator import attrgetter

from .abstract_progress_builder import AbstractProgressBuilder


class RecordStatus(Enum):
    AFTER_ENTRY = 1
    AFTER_EXIT = 2
    FINISHED = 3


class RecordEntity:

    def __init__(self, index, margin_period_after_trade, initialized_record):
        self.index = index
        self.status = RecordStatus.AFTER_ENTRY.value
        self.period_to_record = margin_period_after_trade
        self.record = initialized_record


class AbstractProgressRecorder(AbstractProgressBuilder, ABC):

    def __init__(self, is_series_record=False, margin_period=48):
        self.latest_index = 0
        self.progress_entities = []
        self.finished_entities = []
        self.margin_period = margin_period
        self.is_series_record = is_series_record

    @abstractmethod
    def get_value(self, material):
        raise NotImplementedError()

    @abstractmethod
    def make_entry_record(self, value):
        raise NotImplementedError()

    @abstractmethod
    def make_progress_record(self, current_record, value):
        raise NotImplementedError()

    @abstractmethod
    def make_exit_record(self, current_record, value):
        raise NotImplementedError()

    def entry(self, material):
        value = self.get_value(material)
        entry_record = self.make_entry_record(value)
        entity = RecordEntity(self.latest_index, self.margin_period, entry_record)
        self.progress_entities.append(entity)
        self.latest_index += 1

    def progress(self, material):
        value = self.get_value(material)
        for entity in self.progress_entities:
            if entity.status == RecordStatus.AFTER_EXIT.value:
                if not self.is_series_record or entity.period_to_record <= 0:
                    entity.status = RecordStatus.FINISHED.value
                    continue

                entity.period_to_record -= 1

            progress_record = self.make_progress_record(entity.record, value)
            entity.record = progress_record

        progress_entities = [x for x in self.progress_entities if x.status != RecordStatus.FINISHED.value]
        finished_entities = [x for x in self.progress_entities if x.status == RecordStatus.FINISHED.value]

        self.progress_entities = progress_entities
        self.finished_entities.extend(finished_entities)

    def exit(self, material):
        value = self.get_value(material)
        exit_entities = [x for x in self.progress_entities if x.status == RecordStatus.AFTER_ENTRY.value]
        if len(exit_entities) != 1:
            raise ValueError('Only one AFTER_ENTRY entity permitted at a time')

        entity = exit_entities[0]
        exit_record = self.make_exit_record(entity.record, value)
        entity.record = exit_record
        entity.status = RecordStatus.AFTER_EXIT.value

    def build(self):
        after_exit_entities = [x for x in self.progress_entities if x.status != RecordStatus.AFTER_ENTRY.value]
        self.finished_entities.extend(after_exit_entities)

        sorted_entities = sorted(self.finished_entities, key=attrgetter('index'))
        return [x.record for x in sorted_entities]
