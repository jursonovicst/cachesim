from typing import Hashable


class Request:
    """
    Represents the metadata of the cache request
    """

    @classmethod
    def fromlist(cls, l: list):
        assert len(l) >= 4, f"I need 'time, hash, size, maxage, [fetched]' elements, but got '{l}'"
        return cls(l[0], l[1], l[2], l[3], l[4] if len(l) > 4 else False)

    def __init__(self, time: float, chash: Hashable, size: int, maxage: int, fetched: bool = False):
        """

        :param time: Timestamp (unix time) at the request was placed (and stored in case of a cache hit)
        :param chash: Uniq identifier of the requested object (hash).
        :param size: Size of the requested object.
        :param maxage: Maximum caching time. For non cacheable objects, use a non-positive value.
        """
        # metadata to be known before fetch
        self._time = time
        self._hash = chash

        # metadata only known after fetch
        self._size = size
        self._maxage = maxage

        # misc
        self._fetched = fetched  # object fetched (retrieved from origin)

    @property
    def requestedat(self) -> float:
        assert not self.fetched, f"fetched object has no request time, use the {self.storedat.__class__.__name__} property instead!"
        return self._time

    @property
    def storedat(self) -> float:
        assert self.fetched, f"requested object has no stored time, use the {self.requestedat.__class__.__name__} property instead!"
        return self._time

    @property
    def hash(self) -> Hashable:
        return self._hash

    @property
    def size(self) -> int:
        assert self.fetched, f"size property cannot be known before object fetch!"
        return self._size

    @property
    def maxage(self) -> int:
        assert self.fetched, f"maxage property cannot be known before object fetch!"
        return self._maxage

    @property
    def cacheable(self) -> bool:
        assert self.fetched, f"cacheable cannot be known before object fetch!"
        return self.maxage > 0

    def isexpired(self, now: float) -> bool:
        assert self.fetched, f"Object must first enter the cache to determine if it is expired."
        return self._time + self.maxage < now

    @property
    def fetched(self) -> bool:
        return self._fetched

    @fetched.setter
    def fetched(self, val: bool):
        self._fetched = val

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
        return f"{self._time} {self._hash} {self._size if self.fetched else '-'} {self._maxage if self.fetched else '-'}"

    def __copy__(self):
        return type(self)(self._time, self._hash, self._size, self._maxage, self._fetched)
