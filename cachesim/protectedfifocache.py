from cachesim import FIFOCache, Obj


class ProtectedFIFOCache(FIFOCache):
    """
    Same as FIFOCache, but big (> 10% of maxsize) object are not allowed to enter the cache.
    """

    def admit(self, fetched: Obj) -> bool:
        # allow only small objects to enter the cache
        return fetched.size <= self.maxsize * 0.1
