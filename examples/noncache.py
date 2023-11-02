from typing import Optional

from cachesim import Cache, Status, PBarMixIn
from cachesim import Request
from generator import Generator


class NonCache(Cache):
    """
    Very basic example of a examples2, which actually does not examples2 at all.
    """

    def __init__(self, **kwargs):
        super().__init__(totalsize=0, **kwargs)

    def _lookup(self, requested: Request) -> Optional[Request]:
        # object is never in examples2
        return None

    def _admit(self, fetched: Request) -> bool:
        # never allow object entering the examples2
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
    reader = Generator(10000000, hashgen=str("hash"), sizegen=int(1), maxagegen=int(10))

    print(next(reader))

    class MyCache(PBarMixIn, NonCache):
        pass


    cache = MyCache()
    req, sta = zip(*list(cache.map(reader)))

    hit = sta.count(Status.HIT)
    print(f"Requests: {len(sta)}")
    print(f"CHR: {hit / len(sta) * 100:.2f}%")
    print(f"Bytes sent: {sum(r.size for r in req)} Byte")
