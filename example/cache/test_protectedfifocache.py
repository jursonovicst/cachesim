from unittest import TestCase

from cachesim import Request
from example.cache import ProtectedFIFOCache


class TestProtectedFIFOCache(TestCase):
    def test_protectedfifocache(self):
        totalsize = 200
        limit = 0.2
        cache = ProtectedFIFOCache(totalsize, limit=limit)
        maxage = 300
        small = Request(0, 'small', int(totalsize * limit * 0.9), maxage)
        big = Request(0, 'big', int(totalsize * limit * 1.1), maxage)

        small.fetched = True
        self.assertTrue(cache._admit(small))
        big.fetched = True
        self.assertFalse(cache._admit(big))
