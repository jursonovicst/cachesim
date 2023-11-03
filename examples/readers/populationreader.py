import random
import time
from typing import List

from cachesim import Request
from cachesim.tools import Reader


class PopulationReader(Reader):

    def __init__(self, count: int, population: List[Request], weights: List[int]):
        super().__init__(count)

        assert len(population) == len(
            weights), f"population size must match with weights len, got: '{len(population)}', '{len(weights)}'"
        assert all(isinstance(e, Request) for e in population), f"Population should have only Request elements"

        assert all(w >= 0 for w in weights), f"Weights should be non negative integers"

        self._population = population
        self._choices = iter(random.choices(range(len(population)), weights=weights, k=count))

    def __iter__(self):
        return self

    def __next__(self):
        choice = next(self._choices)
        return Request(time=time.time(),
                       chash=self._population[choice]._hash,
                       size=self._population[choice]._size,
                       maxage=self._population[choice]._maxage)
