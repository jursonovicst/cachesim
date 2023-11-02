from typing import Optional

from cachesim import Cache, Status, PBarMixIn
from cachesim import Request
from generator import Generator


class LFUCache(Cache):
    """
    LFU (least frequently used) model. inefficient implementation.
    """

    def __init__(self, totalsize: int, **kwargs):
        super().__init__(totalsize=totalsize, **kwargs)

        # store metadata indexed by hash
        self._cache = {}  # hash: request

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

    def _lookup(self, requested: Request) -> Optional[Request]:
        if requested.hash not in self._index:
            return None

        # match, update count and return object
        self._index[requested.hash] += 1
        return self._cache[requested.hash]

    def _admit(self, fetched: Request) -> bool:
        # check if object fit into the examples2 (should not normally happen, eviction should be triggered first)
        return self.size + fetched.size <= self.totalsize

    def _store(self, fetched: Request):
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


if __name__ == "__main__":
    reader = Generator(10000000, hashgen=lambda: "tom", sizegen=lambda: 1, maxagegen=lambda: 1)
    #reader = StaticGenerator(10000000, Request(0, 'abc', 1, 3600))

    class MyCache(PBarMixIn, LFUCache):
        pass


    # examples2 size is 10% of content base (2 byte hashlen allows 2^16 different objects)
    # chr should be around 10%
    cache = MyCache(totalsize=int(2 ** 16 * 0.1))

    req, sta = zip(*list(cache.map(reader)))

    hit = sta.count(Status.HIT)
    print(f"Requests: {len(sta)}")
    print(f"CHR: {hit / len(sta) * 100:.2f}%")
    print(f"Bytes sent: {sum(r.size for r in req)} Byte")
