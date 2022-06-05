from cachesim.cache import Request
from example.cache import FIFOCache


class ProtectedFIFOCache(FIFOCache):
    """
    Same as FIFOCache, but big (> totalsize * limit) object are not allowed to enter the cache to avoid eviction of a
    large number of small objects.
    """

    def __init__(self, totalsize: int, limit: float = 0.1):
        super().__init__(totalsize)

        assert 0 < limit < 1, f"limit must be between 0 and 1, got: '{limit}'"
        self._limit = limit

    def _admit(self, fetched: Request) -> bool:
        # allow only small objects to enter the cache
        if fetched.size > self.totalsize * self._limit:
            return False

        return super()._admit(fetched)
