from abc import ABC, abstractmethod
from typing import Any


class AbstractAdapter(ABC):

    @abstractmethod
    def execute(self, query: Any):
        raise NotImplemented

    @abstractmethod
    def get(self, query: Any):
        raise NotImplemented

    @abstractmethod
    def add(self, query: Any):
        raise NotImplemented

    @abstractmethod
    def create(self, query: Any):
        raise NotImplemented
