from typing import Iterable

from tqdm import tqdm

from cachesim.cache import Request
from example.cache import NonCache


class PBarCache(NonCache):
    """
    Noncache variant to show, how to integrate a progress bar to keep track of the simulation.
    """

    def map(self, requests: Iterable[Request], total=None):
        return map(self._recv, tqdm(requests, desc=self.__class__.__name__, total=total))
