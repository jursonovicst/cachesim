from typing import Tuple

from cachesim import Cache, Status
from cachesim import Request
from cachesim.tools import PBarMixIn
from generator import Generator


class NonCache(Cache):
    """
    Very basic example of a xxx, which actually does not xxx at all.
    """

    def __init__(self, **kwargs):
        super().__init__(totalsize=0, **kwargs)

    def _lookup(self, requested: Request) -> Tuple[bool, float | None]:
        # object is never in xxx
        return False, None

    def _admit(self, fetched: Request) -> bool:
        # never allow object entering the xxx
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


    class MyCache(PBarMixIn, NonCache):
        pass


    cache = MyCache()
    req, sta, age = zip(*list(cache.map(reader)))

    hit = sta.count(Status.HIT)
    print(f"Requests: {len(sta)}")
    print(f"CHR: {hit / len(sta) * 100:.2f}%")
    print(f"Bytes sent: {sum(r.size for r in req)} Byte")
