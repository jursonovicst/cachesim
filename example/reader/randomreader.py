import random
import time

from cachesim import Reader, Request


class RandomReader(Reader):

    def __init__(self, totalcount: int, hashlen: int = 8, sizegen: callable = random.randint(1, 100),
                 maxagegen: callable = random.randint(60, 300)):
        super().__init__(totalcount)

        assert hashlen > 0, f"I expect a positive hashlen, got '{hashlen}'"
        self._hashlen = int(hashlen)
        self._sizegen = sizegen
        self._maxagegen = maxagegen
        self._counter = 0

    @property
    def totalcount(self) -> int:
        return self._totalcount

    def __iter__(self):
        self._counter = self.totalcount
        return super().__iter__()

    def __next__(self) -> Request:
        if self._counter == 0:
            raise StopIteration

        self._counter -= 1
        return Request(time.time(), '%x' % random.getrandbits(self._hashlen * 8), int(self._sizegen),
                       int(self._maxagegen))
