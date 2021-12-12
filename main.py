from cachesim import Cache, Obj
from typing import Optional


class NonCache(Cache):
    """
    Very basic example of a cache, which actually does not cache at all.
    """

    def lookup(self, requested: Obj) -> Optional[Obj]:
        return None

    def admit(self, fetched: Obj) -> bool:
        return True

    def store(self, fetched: Obj):
        pass


class FIFOCache(Cache):
    """
    First in First out cache model.
    """

    def __init__(self, maxsize: int, logger=None):
        super().__init__(maxsize, logger)

        # implement a FIFO for the cache itself
        self._cache = []

    def lookup(self, requested: Obj) -> Optional[Obj]:
        # check if object already in cache
        stored = next((x for x in self._cache if x == requested), None)
        if stored is not None:
            # HIT
            return stored

        return None

    def admit(self, fetched: Obj) -> bool:
        return True

    def store(self, fetched: Obj):
        # trigger cache eviction if needed
        while fetched.size <= self.maxsize < sum(self._cache) + fetched.size:
            self._cache.pop(0)

        # put the new object at the end of the cache
        self._cache.append(fetched)


class ProtectedFIFOCache(FIFOCache):
    """
    Same as FIFOCache, but big (> 10% of total cache size) object are not allowed to enter the cache.
    """

    def admit(self, fetched: Obj) -> bool:
        # allow only small objects to enter the cache
        return fetched.size <= self.maxsize * 0.1


if __name__ == '__main__':

    # define objects
    x = Obj('x', 1000)
    a = Obj('a', 100)
    b = Obj('b', 100)
    c = Obj('c', 100)

    # create cache
    cache = NonCache(200)

    # place requests
    cache.recv(0, x)
    cache.recv(0, x)
    cache.recv(1, a)
    cache.recv(2, b)
    cache.recv(3, a)
    cache.recv(4, c)


    cache = FIFOCache(400)
    cache.recv(0, x)
    cache.recv(0, x)
    cache.recv(1, a)
    cache.recv(2, b)
    cache.recv(3, a)
    cache.recv(4, c)


    a = Obj('a', 100)
    b = Obj('b', 100)
    c = Obj('c', 30)
    cache = ProtectedFIFOCache(400)
    # too big request (>10%*400(
    cache.recv(1, a)
    cache.recv(2, b)
    cache.recv(3, a)
    # should be allowed to enter the cache
    cache.recv(4, c)
    cache.recv(4.1, c)
    cache.recv(4.2, c)
    # expired request
    cache.recv(1000, c)
