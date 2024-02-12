from abc import ABC, abstractmethod
from typing import Iterator

from cachesim import Request


class Reader(ABC):
    """

    """

    def __init__(self, count: int):
        assert count >= 0, f"I expect a non negative count, got '{count}'"
        self._count = int(count)

    @property
    def count(self) -> int:
        """
        Number of items in this reader, -1 if not known.
        """
        return self._count

    def __iter__(self) -> Iterator:
        """
        Overload to initialize if needed
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
