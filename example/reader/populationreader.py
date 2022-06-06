import random
import time
from typing import List

from cachesim import Reader
from cachesim.cache import Request


class PopulationReader(Reader):

    def __init__(self, totalsize: int, population: List[Request], weights: List[int]):
        assert totalsize >= 0, f"I expect a non negative totalsize, got '{totalsize}'"
        self._totalsize = int(totalsize)

        assert len(population) == len(
            weights), f"population size must match with weights len, got: '{len(population)}', '{len(weights)}'"
        assert all(isinstance(e, Request) for e in population), f"Population should have Request element"
        self._population = population

        assert all(w >= 0 for w in weights), f"Weights should be non negative integers"
        self._weights = weights

        self._counter = 0

    @property
    def totalsize(self) -> int:
        return self._totalsize

    def __iter__(self):
        self._counter = self.totalsize
        return super().__iter__()

    def __next__(self) -> Request:
        if self._counter == 0:
            raise StopIteration

        self._counter -= 1
        request = random.choices(self._population, self._weights, k=1)[0]
        request.time = time.time()
        return request
