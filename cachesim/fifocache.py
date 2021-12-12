from cachesim import Cache, Obj
from typing import Optional


class FIFOCache(Cache):
    """
    First in First out cache model.
    """

    def __init__(self, maxsize: int, logger=None):
        super().__init__(maxsize, logger)

        # implement a FIFO for the cache itself
        self._cache = []

    def lookup(self, requested: Obj) -> Optional[Obj]:
        # check if object already in cache
        stored = next((x for x in self._cache if x == requested), None)
        if stored is not None:
            # HIT
            return stored

        return None

    def admit(self, fetched: Obj) -> bool:
        return True

    def store(self, fetched: Obj):
        # trigger cache eviction if needed
        while fetched.size <= self.maxsize < sum(self._cache) + fetched.size:
            self._cache.pop(0)

        # put the new object at the end of the cache
        self._cache.append(fetched)
