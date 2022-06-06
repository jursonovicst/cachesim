import random
import time
from unittest import TestCase

import matplotlib.pyplot as plt

from cachesim.cache import Request, Status
from example.cache import FIFOCache
from example.reader import PopulationReader


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
        self.assertFalse(cache._treshold)
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

    def test_chr(self):
        # create reader with 100, in avg. 300 Byte large random requests. Total content base is around 300kB
        count = 10000
        popcount = int(count / 10)
        mean = 300
        stddev = 20
        reader = PopulationReader(count,
                                  population=[Request(time.time(),
                                                      "%x" % random.getrandbits(128),
                                                      int(random.normalvariate(mean, stddev)),
                                                      int(3600))
                                              for x in range(0, popcount)],
                                  weights=[1] * popcount)

        # create a cache, size limited to 10% of content base
        totalsize = int(count * mean / 10)
        cache = FIFOCache(totalsize=totalsize)

        ret = cache.map(reader)
        requests, statuses, sizes = zip(*list(ret))
        chr = sum(s == Status.HIT for s in statuses) / count
        print(f"CHR: {chr * 100:.2f}%")

        plt.plot([r.time for r in requests], sizes)
        plt.ylim(0, totalsize)
        plt.ylabel("cache size (B)")
        plt.ylabel('time')
        plt.show()
