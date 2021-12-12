from cachesim import Cache, Obj, Status
from typing import Optional
import unittest


class NonCache(Cache):
    """
    Very basic example of a cache, which actually does not cache at all.
    """

    def _lookup(self, requested: Obj) -> Optional[Obj]:
        return None

    def _admit(self, fetched: Obj) -> bool:
        return True

    def _store(self, fetched: Obj):
        pass


class FIFOCache(Cache):
    """
    First in First out cache model.
    """

    def __init__(self, maxsize: int, logger=None):
        super().__init__(maxsize, logger)

        # implement a FIFO for the cache itself
        self._cache = []

    def _lookup(self, requested: Obj) -> Optional[Obj]:
        # check if object already in cache
        return next((x for x in self._cache if x == requested), None)

    def _admit(self, fetched: Obj) -> bool:
        return True

    def _store(self, fetched: Obj):
        # trigger cache eviction if needed
        while fetched.size <= self.maxsize < sum(self._cache) + fetched.size:
            self._cache.pop(0)

        # put the new object at the end of the cache
        self._cache.append(fetched)


class ProtectedFIFOCache(FIFOCache):
    """
    Same as FIFOCache, but big (> 10% of total cache size) object are not allowed to enter the cache.
    """

    def _admit(self, fetched: Obj) -> bool:
        # allow only small objects to enter the cache
        return fetched.size <= self.maxsize * 0.1


class TestCaches(unittest.TestCase):
    def setUp(self):
        # define objects
        self.x = Obj('x', 1000, 300)
        self.a = Obj('a', 100, 300)
        self.b = Obj('b', 100, 300)
        self.c = Obj('c', 100, 300)
        self.d = Obj('d', 30, 300)

    def test_noncache(self):
        # create cache
        cache = NonCache(200)

        # place requests
        self.assertEqual(cache.recv(0, self.x), Status.PASS)  # way too big, must be PASS
        self.assertEqual(cache.recv(1, self.a), Status.MISS)  # NonCache does not cache
        self.assertEqual(cache.recv(2, self.b), Status.MISS)  # NonCache does not cache
        self.assertEqual(cache.recv(3, self.c), Status.MISS)  # NonCache does not cache

    def test_fifocache(self):
        # create cache
        cache = FIFOCache(400)

        # place requests
        self.assertEqual(cache.recv(0, self.x), Status.PASS)  # way too big, must be PASS
        self.assertEqual(cache.recv(1, self.a), Status.MISS)  # MISS
        self.assertEqual(cache.recv(2, self.b), Status.MISS)  # MISS
        self.assertEqual(cache.recv(3, self.a), Status.HIT)  # 2nd request on a, must be HIT
        self.assertEqual(cache.recv(4, self.c), Status.MISS)  # MISS

    def test_protectedfifocache(self):
        # create cache
        cache = ProtectedFIFOCache(400)

        # place requests
        self.assertEqual(cache.recv(0, self.a), Status.PASS)  # size limit at cache admission
        self.assertEqual(cache.recv(1, self.b), Status.PASS)  # size limit at cache admission
        self.assertEqual(cache.recv(2, self.a), Status.PASS)  # size limit at cache admission
        self.assertEqual(cache.recv(3, self.d), Status.MISS)  # MISS
        self.assertEqual(cache.recv(3.1, self.d), Status.HIT)  # 2nd request on a, must be HIT
        self.assertEqual(cache.recv(3.2, self.d), Status.HIT)  # 3rd request on a, must be HIT
        self.assertEqual(cache.recv(1000, self.d), Status.MISS)  # expired, must be MISS


if __name__ == '__main__':
    unittest.main()
