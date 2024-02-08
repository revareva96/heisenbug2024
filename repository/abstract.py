from abc import ABC, abstractmethod
from typing import Any


class AbstractAdapter(ABC):

    @abstractmethod
    def execute(self, query: Any):
        raise NotImplemented
