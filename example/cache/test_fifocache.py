from unittest import TestCase

from cachesim.cache import Request, Status
from example.cache import FIFOCache


class TestFIFOCache(TestCase):
    def test_fifocache(self):
        totalsize = 20
        cache = FIFOCache(totalsize)
        maxage = 300
        request = Request(0, 'small', 3, maxage)
        bigrequest = Request(0, 'big', 20, maxage)

        self.assertEqual(totalsize, cache.totalsize)
        self.assertEqual(0, cache.size)
        self.assertFalse(cache._lookup(request))
        request.fetched = True
        self.assertTrue(cache._admit(request))
        cache._store(request)
        self.assertEqual(request.size, cache.size)
        self.assertTrue(cache._lookup(request))
        self.assertFalse(cache.treshold)
        bigrequest.fetched = True
        self.assertFalse(cache._admit(bigrequest))
        self.assertEqual(request.size, cache.size)
        self.assertFalse(cache._lookup(bigrequest))

        cache = FIFOCache(totalsize)
        ret = cache.map([request] * 100)
        requests, statuses, sizes = zip(*list(ret))
        self.assertEqual(Status.MISS, statuses[0])
        self.assertTrue(all(s == Status.HIT for s in statuses[1:]))
        self.assertTrue(all(r == request for r in requests))
        self.assertTrue(all(r.maxage == maxage for r in requests))
        self.assertTrue(all(r.size == request.size for r in requests))
        self.assertTrue(all(r.fetched for r in requests))
        self.assertTrue(all(r == request for r in requests))
