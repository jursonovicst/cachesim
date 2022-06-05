from unittest import TestCase

from cachesim.cache import Request, Status
from example.cache import NonCache


class TestNonCache(TestCase):
    def test_noncache(self):
        cache = NonCache()
        content = 'abc'
        maxage = 300
        request = Request(0, content, len(content), maxage)

        self.assertEqual(0, cache.totalsize)
        self.assertFalse(cache._lookup(request))
        self.assertFalse(cache._admit(request))
        cache._store(request)
        self.assertFalse(cache._lookup(request))
        self.assertFalse(cache.treshold)

        cache = NonCache()
        ret = cache.map([request] * 100)
        requests, statuses = zip(*list(ret))
        self.assertTrue(all(s == Status.PASS for s in statuses))
        self.assertTrue(all(r == request for r in requests))
        self.assertTrue(all(r.maxage == maxage for r in requests))
        self.assertTrue(all(r.size == len(content) for r in requests))
        self.assertTrue(all(r.fetched for r in requests))
        self.assertTrue(all(r == request for r in requests))
