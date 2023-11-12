from typing import Tuple, Callable, TypeVar

import cachetools

from cachesim import Cache
from cachesim import Request

_VT = TypeVar("_VT")


class TLFUCache(cachetools.LFUCache):

    def __init__(self,
                 maxsize: float,
                 ttl: float,
                 timer: Callable[[], float] = ...,
                 getsizeof: Callable[[_VT], float] | None = ...):
        super().__init__(maxsize=maxsize, getsizeof=getsizeof)

        cachetools.TLRUCache()


class TLFUCache(Cache):
    """
    LFU (least frequently used) model by cachetools.
    """

    def __init__(self, totalsize: int, **kwargs):
        super().__init__(totalsize=totalsize, **kwargs)

        # store metadata indexed by hash
        self._cache = cachetools.LFUCache(totalsize, lambda x: x.size)

    @property
    def size(self) -> int:
        return int(self._cache.currsize)

    def _lookup(self, requested: Request) -> Tuple[bool, float | None]:
        if requested.hash not in self._cache:
            return False, None

        # match, update count and return

        return True, self._cache[requested.hash].time

    def _admit(self, fetched: Request) -> bool:
        # check if object fit into the xxx (should not normally happen, eviction should be triggered first)
        return self.size + fetched.size <= self.totalsize

    def _store(self, fetched: Request) -> None:
        self._cache[fetched.hash] = fetched
