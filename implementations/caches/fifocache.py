from typing import Tuple

from cachesim import Cache, Status
from cachesim import Request
from cachesim.tools import PBarMixIn
from readers.populationreader import PopulationReader


class FIFOCache(Cache):
    """
    First in First out xxx model.
    """

    def __init__(self, totalsize: int, **kwargs):
        super().__init__(totalsize=totalsize, **kwargs)

        # store metadata indexed by hash
        self._cache = {}  # hash:fetched

        # keep track of indexes entering the xxx
        self._index = []  # hash

        # actual size of the xxx
        self._size = 0

    @property
    def size(self) -> int:
        return self._size

    @size.setter
    def size(self, v: int):
        assert v >= 0, f"Size must be non negative, received '{v}'"
        self._size = v

    def _lookup(self, requested: Request) -> Tuple[bool, float | None]:
        if requested.hash not in self._index:
            return False, None

        return True, self._cache[requested.hash].time

    def _admit(self, fetched: Request) -> bool:
        # check if object fit into the xxx (should not normally happen, eviction should be triggered first)
        return self.size + fetched.size <= self.totalsize

    def _store(self, fetched: Request):
        assert fetched.hash not in self._index, f"Object {fetched} already in xxx: {self._cache[fetched.hash]}"
        self._cache[fetched.hash] = fetched
        self._index.append(fetched.hash)
        self.size += fetched.size

    @property
    def thlow(self):
        return .9

    @property
    def thhigh(self):
        return .95

    def _evict(self):
        """
        FIFO xxx, evict oldest objects first
        """

        # evict till xxx reaches 90%
        while self.size / self.totalsize > self.thlow:
            hash_to_delete = self._index.pop(0)
            evicted = self._cache.pop(hash_to_delete)
            self.size -= evicted.size

    @property
    def _treshold(self) -> bool:
        return self.size / self.totalsize > self.thhigh


if __name__ == "__main__":
    count = 100000
    cbase = count // 10
    reader = PopulationReader(count, [Request(0, chash, 1, 3600) for chash in range(count // 10)], [1] * cbase)


    class MyCache(PBarMixIn, FIFOCache):
        pass


    cache = MyCache(totalsize=cbase // 10)

    req, sta, age = zip(*list(cache.map(reader)))

    hit = sta.count(Status.HIT)
    print(f"Requests: {len(sta)}")
    print(f"CHR: {hit / len(sta) * 100:.2f}%")
    print(f"Bytes server: {sum(r.size for r in req)} Byte")
