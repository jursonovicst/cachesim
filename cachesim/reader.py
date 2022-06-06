from abc import ABC, abstractmethod
from typing import Iterator

from cachesim.cache import Request


class Reader(ABC):
    """

    """

    def __iter__(self) -> Iterator:
        """
        Overload to initialize
        :return:
        """
        return self

    @abstractmethod
    def __next__(self) -> Request:
        """
        Implement to provide elements
        :return: Requests
        """
        pass

    @property
    @abstractmethod
    def totalsize(self) -> int:
        pass
