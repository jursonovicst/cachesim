from cachesim import Request
from cachesim import Status, PBarMixIn
from cachesim.caches import FIFOCache
from cachesim.readers import ConstantReader


class ProtectedFIFOCache(FIFOCache):
    """
    Same as FIFOCache, but big (> totalsize * limit) object are not allowed to enter the caches to avoid eviction of a
    large number of small objects.
    """

    def __init__(self, totalsize: int, limit: int):
        super().__init__(totalsize)

        assert 0 < limit < totalsize, f"limit must be between 0 and {self.totalsize}, got: '{limit}'"
        self._limit = limit

    def _admit(self, fetched: Request) -> bool:
        # allow only small objects to enter the caches
        if fetched.size > self._limit:
            return False

        return super()._admit(fetched)


if __name__ == "__main__":
    totalcount = 10000000
    reader = ConstantReader(totalcount, Request(0, 'abc', 1, 3600))


    class MyCache(PBarMixIn, FIFOCache):
        pass


    cache = MyCache(totalsize=int(totalcount * 0.1))

    req, sta, cac = zip(*list(cache.map(reader)))

    hit = sta.count(Status.HIT)
    print(f"Requests: {len(sta)}")
    print(f"CHR: {hit / len(sta) * 100:.2f}%")
    print(f"Bytes sent: {sum(r.size for r in req)} Byte")
