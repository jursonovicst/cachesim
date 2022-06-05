from typing import Iterable

from tqdm import tqdm

from cachesim.cache import Request, Status
from example.cache import NonCache


class PBarCache(NonCache):
    """
    Noncache variant to show, how to integrate a progress bar to keep track of the simulation.
    """

    def map(self, requests: Iterable[Request], total=None):
        return map(self._recv, tqdm(requests, desc=self.__class__.__name__, total=total))


if __name__ == "__main__":
    cache = PBarCache()


    class MyRequests:
        def __init__(self, n: int):
            self.n = n

        def __iter__(self):
            self.request = Request(0, 'a', 1, 30)
            return self

        def __next__(self):
            if self.n > 0:
                self.n -= 1
                return self.request
            else:
                raise StopIteration


    total = 10000000
    client_requests = MyRequests(n=total)
    req, sta = zip(*list(cache.map(client_requests, total=total)))

    hit = sta.count(Status.HIT)
    print(f"Requests: {len(sta)}")
    print(f"CHR: {hit / len(sta) * 100:.2f}%")
