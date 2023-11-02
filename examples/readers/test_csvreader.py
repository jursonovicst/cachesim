from unittest import TestCase

from cachesim import Request
from cachesim.readers import CSVReader


class TestCSVReader(TestCase):

    def test_csvreader(self):
        csvreader = CSVReader(totalcount=12, csvfile='cachesim/readers/sample.csv')

        count = 0
        for request in csvreader:
            count += 1
            self.assertIsInstance(request, Request)
            self.assertIn(request.hash, ['a', 'b', 'c', 'd', 'e'])

        self.assertEqual(count, 12)

        with self.assertRaises(StopIteration):
            self.assertIsNone(next(csvreader))

        with self.assertRaises(AssertionError):
            CSVReader(totalcount=5, csvfile='nonexistent.csv')
