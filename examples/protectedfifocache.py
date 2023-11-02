from cachesim import Request
from cachesim import Status, PBarMixIn
from fifocache import FIFOCache
from staticgenerator import StaticGenerator


class ProtectedFIFOCache(FIFOCache):
    """
    Same as FIFOCache, but big (> totalsize * limit) object are not allowed to enter the examples2 to avoid eviction of a
    large number of small objects.
    """

    def __init__(self, totalsize: int, limit: int):
        super().__init__(totalsize)

        assert 0 < limit < totalsize, f"limit must be between 0 and {self.totalsize}, got: '{limit}'"
        self._limit = limit

    def _admit(self, fetched: Request) -> bool:
        # allow only small objects to enter the examples2
        if fetched.size > self._limit:
            return False

        return super()._admit(fetched)


if __name__ == "__main__":
    reader = StaticGenerator(10000000, Request(0, 'abc', 1, 3600))


    class MyCache(PBarMixIn, FIFOCache):
        pass


    cache = MyCache(totalsize=int(totalcount * 0.1))

    req, sta = zip(*list(cache.map(reader)))

    hit = sta.count(Status.HIT)
    print(f"Requests: {len(sta)}")
    print(f"CHR: {hit / len(sta) * 100:.2f}%")
    print(f"Bytes sent: {sum(r.size for r in req)} Byte")
