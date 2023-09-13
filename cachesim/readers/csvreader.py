import csv
from os import access, R_OK
from os.path import isfile
from typing import Iterator

from cachesim import Reader, Request


class CSVReader(Reader):

    def __init__(self, totalcount: int, csvfile: str):
        super().__init__(totalcount=totalcount)

        assert isfile(csvfile) and access(csvfile, R_OK), f"File '{csvfile}' doesn't exist or isn't readable"
        self._csvfile = csvfile
        self._file = None
        self._reader = None
        self._counter = 0

    def __iter__(self) -> Iterator:
        if self._file is not None:
            self._file.close()

        self._file = open(self._csvfile, newline='')
        self._reader = csv.reader(self._file)
        self._counter = self.totalcount

        return super().__iter__()

    def __next__(self) -> Request:
        if self._counter == 0:
            raise StopIteration

        self._counter -= 1

        try:
            return Request.fromlist(next(self._reader))
        except StopIteration:
            self._file.seek(0)
            return Request.fromlist(next(self._reader))
