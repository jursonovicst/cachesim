from typing import Optional

from cachesim import Request
from cachesim.cache import Cache, Status, PBarMixIn
from example.reader import ConstantReader


class NonCache(Cache):
    """
    Very basic example of a cache, which actually does not cache at all.
    """

    def __init__(self):
        super().__init__(totalsize=0)

    def _lookup(self, requested: Request) -> Optional[Request]:
        # object is never in cache
        return None

    def _admit(self, fetched: Request) -> bool:
        # never allow object entering the cache
        return False

    def _store(self, fetched: Request):
        pass

    def _evict(self):
        pass

    @property
    def _treshold(self) -> bool:
        # no need to eviction
        return False


if __name__ == "__main__":
    totalcount = 10000000
    reader = ConstantReader(totalcount, Request(0, 'abc', 1, 3600))


    class MyCache(PBarMixIn, NonCache): pass


    cache = MyCache()

    req, sta = zip(*list(cache.map(reader)))

    hit = sta.count(Status.HIT)
    print(f"Requests: {len(sta)}")
    print(f"CHR: {hit / len(sta) * 100:.2f}%")
    print(f"Bytes sent: {sum(r.size for r in req)} Byte")
