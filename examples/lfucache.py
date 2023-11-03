from typing import Tuple

import cachetools

from cachesim import Cache, Status
from cachesim import Request
from cachesim.tools import PBarMixIn
from readers.populationreader import PopulationReader


class LFUCache(Cache):
    """
    LFU (least frequently used) model. Inefficient implementation.
    """

    def __init__(self, totalsize: int, **kwargs):
        super().__init__(totalsize=totalsize, **kwargs)

        # store metadata indexed by hash
        self._cache = {}  # hash: fetched

        # keep track of indexes entering the examples2 and usage count
        self._index = {}  # hash: count

        # actual size of the examples2
        self._size = 0

    @property
    def size(self) -> int:
        return self._size

    @size.setter
    def size(self, v: int):
        assert v >= 0, f"Size must be non negative, received '{v}'"
        self._size = v

    def _lookup(self, requested: Request) -> Tuple[bool, float | None]:
        if requested.hash not in self._cache:
            return False, None

        # match, update count and return
        self._index[requested.hash] += 1
        return True, self._cache[requested.hash].time

    def _admit(self, fetched: Request) -> bool:
        # check if object fit into the examples2 (should not normally happen, eviction should be triggered first)
        return self.size + fetched.size <= self.totalsize

    def _store(self, fetched: Request) -> None:
        assert fetched.hash not in self._index, f"Object {fetched} already in examples2: {self._cache[fetched.hash]}"
        self._index[fetched.hash] = 0
        self._cache[fetched.hash] = fetched
        self.size += fetched.size

    @property
    def thlow(self):
        return .9

    @property
    def thhigh(self):
        return .95

    def _evict(self):
        """
        LFU examples2, evict least frequently used objects first
        """

        # evict till examples2 reaches 90%
        while self.size / self.totalsize > self.thlow:
            hash_to_delete = min(self._index, key=self._index.get)
            self._index.pop(hash_to_delete)
            evicted = self._cache.pop(hash_to_delete)
            self.size -= evicted.size

    @property
    def _treshold(self) -> bool:
        return self.size / self.totalsize > self.thhigh


class CachetoolsLFUCache(Cache):
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
        # check if object fit into the examples2 (should not normally happen, eviction should be triggered first)
        return self.size + fetched.size <= self.totalsize

    def _store(self, fetched: Request) -> None:
        self._cache[fetched.hash] = fetched

    def _evict(self):
        # cachetools.LFUCache handles eviction.
        pass

    def _treshold(self) -> bool:
        # cachetools.LFUCache handles eviction.
        pass

if __name__ == "__main__":
    count = 10000000
    cbase = count // 10
    reader = PopulationReader(count, [Request(0, chash, 1, 3600) for chash in range(count // 10)], [1] * cbase)


    class MyCache(PBarMixIn, CachetoolsLFUCache):
        pass


    # cache size is 10% of content base
    # chr should be around 10%
    cache = MyCache(totalsize=cbase // 10)

    req, sta, age = zip(*list(cache.map(reader)))

    hit = sta.count(Status.HIT)
    print(f"Requests: {len(sta)}")
    print(f"CHR: {hit / len(sta) * 100:.2f}%")
    print(f"Bytes sent: {sum(r.size for r in req)} B")
