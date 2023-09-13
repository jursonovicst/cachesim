from typing import Optional

from cachesim import Request
from cachesim import Cache, Status, PBarMixIn
from cachesim.readers import RandomReader


class LFUCache(Cache):
    """
    LFU (least frequently used) caches model.
    """

    def __init__(self, totalsize: int):
        super().__init__(totalsize)

        # store metadata indexed by hash
        self._cache = {}    # hash: request

        # keep track of indexes entering the caches and usage count
        self._index = {}    # hash: count

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

        # match, update count and return object
        self._index[requested.hash] += 1
        return self._cache[requested.hash]

    def _admit(self, fetched: Request) -> bool:
        # check if object fit into the caches (should not normally happen, eviction should be triggered first)
        return self.size + fetched.size <= self.totalsize

    def _store(self, fetched: Request):
        assert fetched.hash not in self._index, f"Object {fetched} already in caches: {self._cache[fetched.hash]}"
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
        LFU caches, evict least frequently used objects first
        """

        # evict till caches reaches 90%
        while self.size / self.totalsize > self.thlow:
            hash_to_delete = min(self._index, key=self._index.get)
            self._index.pop(hash_to_delete)
            evicted = self._cache.pop(hash_to_delete)
            self.size -= evicted.size

    @property
    def _treshold(self) -> bool:
        return self.size / self.totalsize > self.thhigh

    def _log(self, request: Request, status: Status):
        return super()._log(request, status) + (self.size,)


if __name__ == "__main__":
    totalcount = 200000
    reader = RandomReader(totalcount, hashlen=2, sizegen=int(1))


    class MyCache(PBarMixIn, LFUCache):
        pass

    # caches size is 10% of content base (2 byte hashlen allows 2^16 different objects)
    # chr should be around 10%
    cache = MyCache(totalsize=int(2**16*0.1))

    req, sta, cac = zip(*list(cache.map(reader)))

    hit = sta.count(Status.HIT)
    print(f"Requests: {len(sta)}")
    print(f"CHR: {hit / len(sta) * 100:.2f}%")
    print(f"Bytes sent: {sum(r.size for r in req)} Byte")
