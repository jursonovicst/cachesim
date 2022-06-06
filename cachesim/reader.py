from abc import ABC, abstractmethod
from typing import Iterator

from cachesim import Request


class Reader(ABC):
    """

    """

    def __init__(self, totalcount: int):
        assert totalcount >= 0, f"I expect a non negative totalsize, got '{totalcount}'"
        self._totalcount = int(totalcount)

    @property
    def totalcount(self) -> int:
        return self._totalcount

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
