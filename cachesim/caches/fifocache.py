from typing import Optional

from cachesim import Request
from cachesim import Cache, Status, PBarMixIn
from cachesim.readers import ConstantReader


class FIFOCache(Cache):
    """
    First in First out caches model.
    """

    def __init__(self, totalsize: int):
        super().__init__(totalsize)

        # store metadata indexed by hash
        self._cache = {}

        # keep track of indexes entering the caches
        self._index = []

        # actual size of the caches
        self._size = 0

    @property
    def size(self) -> int:
        return self._size

    @size.setter
    def size(self, v: int):
        assert v >= 0, f"Size must be non negative, received '{v}'"
        self._size = v

    def _lookup(self, requested: Request) -> Optional[Request]:
        if requested.hash not in self._index:
            return None

        return self._cache[requested.hash]

    def _admit(self, fetched: Request) -> bool:
        # check if object fit into the caches (should not normally happen, eviction should be triggered first)
        return self.size + fetched.size <= self.totalsize

    def _store(self, fetched: Request):
        assert fetched.hash not in self._index, f"Object {fetched} already in caches: {self._cache[fetched.hash]}"
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
        FIFO caches, evict oldest objects first
        """

        # evict till caches reaches 90%
        while self.size / self.totalsize > self.thlow:
            hash_to_delete = self._index.pop(0)
            evicted = self._cache.pop(hash_to_delete)
            self.size -= evicted.size

    @property
    def _treshold(self) -> bool:
        return self.size / self.totalsize > self.thhigh

    def _log(self, request: Request, status: Status):
        return super()._log(request, status) + (self.size,)


if __name__ == "__main__":
    totalcount = 10000000
    reader = ConstantReader(totalcount, Request(0, 'abc', 1, 3600))


    class MyCache(PBarMixIn, FIFOCache):
        pass


    cache = MyCache(totalsize=int(1000))

    req, sta, cac = zip(*list(cache.map(reader)))

    hit = sta.count(Status.HIT)
    print(f"Requests: {len(sta)}")
    print(f"CHR: {hit / len(sta) * 100:.2f}%")
    print(f"Bytes sent: {sum(r.size for r in req)} Byte")
