from abc import ABC, abstractmethod
from spec import Spec


class FileProcessor(ABC):
    @abstractmethod
    def process(self, spec: Spec) -> str:
        pass
