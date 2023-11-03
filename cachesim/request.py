from typing import Hashable

from cachesim import Status


class Request:
    """
    Represents the metadata of the cache request
    """

    @classmethod
    def fromlist(cls, l: list):
        assert len(l) >= 4, f"I need 'ts, chash, size, maxage, [fetched]' elements, but got '{l}'"
        return cls(l[0], l[1], l[2], l[3], l[4] if len(l) > 4 else False)

    def __init__(self, time: float, chash: Hashable, size: int, maxage: int, retrieved: bool = False):
        """

        :param time: Timestamp (unix time) at the request was placed (and stored in case of a cache hit)
        :param chash: Uniq identifier of the requested object (hash).
        :param size: Size of the requested object.
        :param maxage: Maximum caching time. For non cacheable objects, use a non-positive value.
        """
        # metadata
        self._time = time
        self._hash = chash
        self._retrieved = retrieved  # object fetched (retrieved from origin)
        self._stored = False

        # metadata only known after fetch
        self._size = size
        self._maxage = maxage
        self._status = None

    ######################
    # properties available

    @property
    def time(self) -> float:
        return self._time

    @property
    def hash(self) -> Hashable:
        return self._hash

    @property
    def retrieved(self) -> bool:
        return self._retrieved

    def retrieve(self, status: Status):
        """
        Simulates object fetch
        """
        self._retrieved = True
        self._status = status

    ######################
    # properties after retrieve

    @property
    def status(self) -> Status:
        assert self.retrieved, f"size property can be accessed after object fetch!"
        return self._status

    @property
    def size(self) -> int:
        assert self.retrieved, f"size property can be accessed after object fetch!"
        return self._size

    @property
    def maxage(self) -> int:
        assert self.retrieved, f"maxage property can be accessed after object fetch!"
        return self._maxage

    @property
    def cacheable(self) -> bool:
        assert self.retrieved, f"cacheable property can be accessed after object fetch!"
        return self.maxage > 0

    def __add__(self, other):
        """For sum() function"""
        assert isinstance(other, Request), f"Operator add has been implemented only for {self.__class__.__name__} type."
        return self.size + other.size

    # def __radd__(self, other):
    #     """For sum() function"""
    #     assert isinstance(other, int), f"Operator radd has been implemented only for {self.__class__.__name__} type."
    #     return other + self.size

    def __str__(self):
        """For logging"""
        return f"{self._time} {self._hash} {self._size if self.retrieved else '-'} {self._maxage if self.retrieved else '-'}"

    def __copy__(self):
        return type(self)(self._time, self._hash, self._size, self._maxage, self._retrieved)
