import random
import time
from typing import List

from cachesim import Reader, Request


class PopulationReader(Reader):

    def __init__(self, totalcount: int, population: List[Request], weights: List[int]):
        super().__init__(totalcount)

        assert len(population) == len(
            weights), f"population size must match with weights len, got: '{len(population)}', '{len(weights)}'"
        assert all(isinstance(e, Request) for e in population), f"Population should have Request element"
        self._population = population

        assert all(w >= 0 for w in weights), f"Weights should be non negative integers"
        self._weights = weights

#        self._counter = 0
        self._requests = None

    def __iter__(self):
        self._requests = iter(random.choices(self._population, self._weights, k=self.totalcount))

        return super().__iter__()

#    def __iter__(self):
#        self._counter = self.totalcount
#        return super().__iter__()

    # def __next__(self) -> Request:
    #     if self._counter == 0:
    #         raise StopIteration
    #
    #     self._counter -= 1
    #     chosen = random.choices(self._population, self._weights, k=1)[0]
    #
    #     return Request(time=time.time(), hash=chosen._hash, size=chosen._size, maxage=chosen._maxage)

    def __next__(self):
        chosen = next(self._requests)
        return Request(time=time.time(), hash=chosen._hash, size=chosen._size, maxage=chosen._maxage)
