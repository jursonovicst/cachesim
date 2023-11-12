import random
from unittest import TestCase

from matplotlib import pyplot as plt

from cachesim import Request, Status
from readers.populationreader import PopulationReader
from caches import NonCache


class TestNonCache(TestCase):
    def test_noncache(self):
        cache = NonCache()
        content = 'abc'
        maxage = 300
        request = Request(0, content, len(content), maxage)

        self.assertEqual(0, cache.maxsize)
        self.assertNotIn(request.hash, cache)
        self.assertFalse(cache._admit(request))
        cache._store(request)
        self.assertFalse(cache._lookup(request))
        self.assertFalse(cache._treshold)

        cache = NonCache()
        ret = cache.map([request] * 100)
        requests, statuses, ages = zip(*list(ret))
        self.assertTrue(all(s == Status.PASS for s in statuses))
        self.assertTrue(all(r == request for r in requests))
        self.assertTrue(all(r.maxage == maxage for r in requests))
        self.assertTrue(all(r.size == len(content) for r in requests))
        self.assertTrue(all(r.retrieved for r in requests))
        self.assertTrue(all(r == request for r in requests))

    def test_chr(self):
        # create readers with 100, in avg. 300 Byte large random requests. Total content base is around 300kB
        totalcount = 10000
        count = int(totalcount / 10)
        mean = 300
        stddev = 20
        reader = PopulationReader(totalcount,
                                  population=[Request(0,
                                                      "%x" % random.getrandbits(8 * 8),
                                                      int(random.normalvariate(mean, stddev)),
                                                      int(3600))
                                              for x in range(0, count)],
                                  weights=[1] * count)
        #        plt.plot([r.time for r in readers], 'x')
        #        plt.show()
        # create a xxx, size limited to 10% of content base
        totalsize = int(totalcount * mean / 10)
        cache = NonCache()

        ret = cache.map(reader)

        requests, statuses, ages = zip(*list(ret))

        chr = sum(s == Status.HIT for s in statuses) / totalcount
        print(f"CHR: {chr * 100:.2f}%")
        self.assertEqual(0, chr)

        plt.plot([r.storedat for r in requests], range(0, totalcount), 'x')
        plt.ylabel("request no.")
        plt.xlabel('time')
        plt.show()
