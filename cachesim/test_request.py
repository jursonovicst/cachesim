import random
import string
import time
from unittest import TestCase

from cachesim import Request


class TestRequest(TestCase):

    def test_request(self):
        for i in range(1000):

            ts = time.time() + random.random() * 2 * 60 * 60 * 24 * 365 + 60 * 60 * 24 * 365
            letters = string.ascii_lowercase
            hash = ''.join(random.choice(letters) for i in range(random.randint(5, 20)))
            size = random.randint(1024, 1024 * 1024 * 100)
            maxage = random.randint(0, 30)
            request = Request(time=ts, hash=hash, size=size, maxage=maxage)

            # before fetch
            self.assertEqual(ts, request.time)
            self.assertEqual(hash, request.hash)
            self.assertFalse(request.fetched)
            self.assertEqual(f"{ts} {hash} - -", str(request))

            with self.assertRaises(AssertionError):
                a = request.size
            with self.assertRaises(AssertionError):
                a = request.maxage
            with self.assertRaises(AssertionError):
                a = request.cacheable
            with self.assertRaises(AssertionError):
                a = request.isexpired(ts + random.randint(0, 35))

            # after fetch
            request.fetched = True
            self.assertEqual(ts, request.time)
            self.assertEqual(hash, request.hash)
            self.assertTrue(request.fetched)
            self.assertEqual(f"{ts} {hash} {size} {maxage}", str(request))

            self.assertEqual(size, request.size)
            self.assertEqual(maxage, request.maxage)
            if maxage == 0:
                self.assertFalse(request.cacheable)
            else:
                self.assertTrue(request.cacheable)

            # after caches enter
            request.enter = ts
            self.assertEqual(ts, request.time)
            self.assertEqual(hash, request.hash)
            self.assertTrue(request.fetched)

            self.assertEqual(size, request.size)
            self.assertEqual(maxage, request.maxage)
            if maxage == 0:
                self.assertFalse(request.cacheable)
            else:
                self.assertTrue(request.cacheable)
            self.assertEqual(ts, request.enter)
            delta = random.randint(0, 35)
            if delta > maxage:
                self.assertTrue(request.isexpired(ts + delta))
            else:
                self.assertFalse(request.isexpired(ts + delta))

    def test_add(self):
        for i in range(1000):
            letters = string.ascii_lowercase

            ts = time.time() + random.random() * 2 * 60 * 60 * 24 * 365 + 60 * 60 * 24 * 365
            index = ''.join(random.choice(letters) for i in range(random.randint(5, 20)))
            size_a = random.randint(1024, 1024 * 1024 * 100)
            maxage = random.randint(0, 30)
            request_a = Request(time=ts, hash=index, size=size_a, maxage=maxage)

            ts = time.time() + random.random() * 2 * 60 * 60 * 24 * 365 + 60 * 60 * 24 * 365
            index = ''.join(random.choice(letters) for i in range(random.randint(5, 20)))
            size_b = random.randint(1024, 1024 * 1024 * 100)
            maxage = random.randint(0, 30)
            request_b = Request(time=ts, hash=index, size=size_b, maxage=maxage)

            request_a.fetched = True
            request_b.fetched = True
            self.assertEqual(size_a + size_b, request_a + request_b)

    def test_eq(self):
        for i in range(1000):
            letters = string.ascii_lowercase
            index_a = ''.join(random.choice(letters) for i in range(random.randint(5, 20)))

            ts = time.time() + random.random() * 2 * 60 * 60 * 24 * 365 + 60 * 60 * 24 * 365
            size = random.randint(1024, 1024 * 1024 * 100)
            maxage = random.randint(0, 30)
            request_a1 = Request(time=ts, hash=index_a, size=size, maxage=maxage)

            ts = time.time() + random.random() * 2 * 60 * 60 * 24 * 365 + 60 * 60 * 24 * 365
            size = random.randint(1024, 1024 * 1024 * 100)
            maxage = random.randint(0, 30)
            request_a2 = Request(time=ts, hash=index_a, size=size, maxage=maxage)

            ts = time.time() + random.random() * 2 * 60 * 60 * 24 * 365 + 60 * 60 * 24 * 365
            index_b = ''.join(random.choice(letters) for i in range(random.randint(5, 20)))
            size = random.randint(1024, 1024 * 1024 * 100)
            maxage = random.randint(0, 30)
            request_b = Request(time=ts, hash=index_b, size=size, maxage=maxage)

            # self.assertEqual(request_a1, request_a2)
            # self.assertNotEqual(request_a1, request_b)
            # self.assertEqual(0, request_a1 + request_a2)

    def test_fromlist(self):
        a4 = [0, 'abc', 1, 60]
        request = Request.fromlist(a4)

        self.assertIsInstance(request, Request)
        self.assertEqual(request.time, 0)
        self.assertEqual(request.hash, 'abc')
        self.assertEqual(request._size, 1)
        self.assertEqual(request._maxage, 60)

        a5 = [0, 'abc', 1, 60, True]
        request = Request.fromlist(a5)

        self.assertIsInstance(request, Request)
        self.assertEqual(request.time, 0)
        self.assertEqual(request.hash, 'abc')
        self.assertEqual(request.size, 1)
        self.assertEqual(request.maxage, 60)
        self.assertTrue(request.fetched)
