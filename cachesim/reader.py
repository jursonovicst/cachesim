from abc import ABC, abstractmethod
from typing import Iterator

from cachesim import Request


class Reader(ABC):
    """

    """

    def __init__(self, count: int):
        assert count >= 0, f"I expect a non negative totalsize, got '{count}'"
        self._count = int(count)

    @property
    def count(self) -> int:
        return self._count

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
