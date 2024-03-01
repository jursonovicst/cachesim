import random
import time
from typing import List

from cachesim import Request
from cachesim.tools import Reader


class PopulationReader(Reader):

    def __init__(self, count: int, cbase: int, weights: List[float] = None):
        super().__init__(count)

        start_ts = time.time()
        self.__requests = [Request(start_ts + ts, chash, 1, 2 ** 64 - 1) for ts, chash in
                           zip(range(count), random.choices(range(cbase), weights=weights, k=count))]
        self._iter = None

    def __iter__(self):
        self._iter = iter(self.__requests)
        super().__iter__()

    def __next__(self):
        return next(self._iter)

    @property
    def future(self):
        return