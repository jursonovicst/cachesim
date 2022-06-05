from cachesim.cache import Cache, Request, Status
from typing import Optional


class FIFOCache(Cache):
    """
    First in First out cache model.
    """

    def __init__(self, totalsize: int):
        super().__init__(totalsize)

        # store metadata indexed by hash
        self._cache = {}

        # keep track of indexes entering the cache
        self._index = []

        # actual size of the cache
        self._size = 0

    @property
    def size(self) -> int:
        return self._size

    @size.setter
    def size(self, v: int):
        assert v >= 0, f"Size must be non negative, received '{v}'"
        self._size = v

    def _lookup(self, requested: Request) -> Optional[Request]:
        try:
            return self._cache[requested]
        except KeyError:
            return None

    def _admit(self, fetched: Request) -> bool:
        # check if object fit into the cache (should not normally happen, eviction should be triggered first)
        return self.size + fetched.size <= self.totalsize

    def _store(self, fetched: Request):
        self._cache[fetched.hash] = fetched
        self._index.append(fetched.hash)

    def _evict(self):
        """
        FIFO cache, evict oldest objects first
        """

        # evict till cache reaches 90%
        while self.size / self.totalsize > 0.9:
            hash_to_delete = self._index.pop(-1)
            evicted = self._cache.pop(hash_to_delete)
            self.size -= evicted.size

    def treshold(self) -> bool:
        return self.size / self.totalsize > 0.95

    def log(self, request: Request, status: Status):
        return request, status, self.size / self.totalsize
