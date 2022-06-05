from typing import Iterable

from tqdm import tqdm

from cachesim.cache import Request, Status
from example.cache import FIFOCache


class ProtectedFIFOCache(FIFOCache):
    """
    Same as FIFOCache, but big (> totalsize * limit) object are not allowed to enter the cache to avoid eviction of a
    large number of small objects.
    """

    def __init__(self, totalsize: int, limit: float = 0.1):
        super().__init__(totalsize)

        assert 0 < limit < 1, f"limit must be between 0 and 1, got: '{limit}'"
        self._limit = limit

    def _admit(self, fetched: Request) -> bool:
        # allow only small objects to enter the cache
        if fetched.size > self.totalsize * self._limit:
            return False

        return super()._admit(fetched)


if __name__ == "__main__":

    class PBarCache(ProtectedFIFOCache):
        """
        Integrates a progress bar to keep track of the simulation.
        """

        def map(self, requests: Iterable[Request], total=None):
            return map(self._recv, tqdm(requests, desc=self.__class__.__base__.__name__, total=total))


    class MyRequests:
        """
        Creates arbitrary client requests.
        """

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


    cache = PBarCache(totalsize=1000)

    total = 10000000
    client_requests = MyRequests(n=total)

    req, sta, cac = zip(*list(cache.map(client_requests, total=total)))

    hit = sta.count(Status.HIT)
    print(f"Requests: {len(sta)}")
    print(f"CHR: {hit / len(sta) * 100:.2f}%")
    print(f"Bytes sent: {sum(r.size for r in req)} Byte")
