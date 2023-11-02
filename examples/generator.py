import random
import time
from typing import Callable, Hashable

from cachesim import Reader, Request


class Generator(Reader):

    def __init__(self, count: int,
                 hashgen: Callable[[], Hashable] = random.randbytes(8),
                 sizegen: Callable[[], int] = random.randint(1, 100),
                 maxagegen: Callable[[], int] = random.randint(60, 300)):
        super().__init__(count)

        self._hashgen = hashgen
        self._sizegen = sizegen
        self._maxagegen = maxagegen
        self._k = 0
        self._timestamp = time.time()

    def __iter__(self):
        return super().__iter__()

    def __next__(self) -> Request:
        if self._k >= self._count:
            raise StopIteration

        self._k += 1
        return Request(self._timestamp + self._k, self._hashgen, self._sizegen, self._maxagegen)
