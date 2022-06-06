import random
from unittest import TestCase

from cachesim import Request
from example.reader import PopulationReader


class TestPopulationReader(TestCase):
    def test_populationreader(self):
        # create reader with 100, in avg. 300 Byte large random requests. Total content base is around 300kB
        totalcount = 1000
        count = totalcount = 100
        smin = 200
        smax = 300
        mmin = 60
        mmax = 300
        reader = PopulationReader(totalcount,
                                  population=[Request(0,
                                                      "%x" % random.getrandbits(8 * 8),
                                                      random.randint(smin, smax),
                                                      random.randint(mmin, mmax))
                                              for x in range(0, count)],
                                  weights=[1] * count)

        n = 0
        lastts = 0
        uniq = {}
        for r in reader:
            n += 1

            self.assertIsInstance(r, Request)

            # self.assertAlmostEqual(time.time(), r.time, -1)
            # test monotonic
            self.assertGreater(r.time, lastts)
            lastts = r.time

            # test uniq
            uniq[r.hash] = r

            self.assertFalse(r.fetched)
            r.fetched = True

            self.assertGreaterEqual(r.size, smin)
            self.assertLessEqual(r.size, smax)
            self.assertGreaterEqual(r.maxage, mmin)
            self.assertLessEqual(r.maxage, mmax)

        self.assertEqual(totalcount, n)
        self.assertLessEqual(len(uniq), count)
