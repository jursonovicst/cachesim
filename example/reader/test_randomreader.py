import random
import time
from unittest import TestCase

from cachesim.cache import Request
from example.reader import RandomReader


class TestRandomReader(TestCase):
    def test_randomreader(self):
        totalsize = 100
        minsize = 20
        maxsize = 200
        maxagemin = 40
        maxagemax = 200
        reader = RandomReader(totalsize, sizegen=random.randint(minsize, maxsize),
                              maxagegen=random.randint(maxagemin, maxagemax))

        self.assertEqual(totalsize, reader.totalsize)

        count = 0
        for r in reader:
            count += 1

            self.assertIsInstance(r, Request)

            self.assertAlmostEqual(time.time(), r.time, -1)
            self.assertFalse(r.fetched)

            r.fetched = True

            self.assertGreater(r.size, minsize)
            self.assertLess(r.size, maxsize)
            self.assertGreater(r.maxage, maxagemin)
            self.assertLess(r.maxage, maxagemax)
            time.sleep(0.01)

        self.assertEqual(totalsize, count)
