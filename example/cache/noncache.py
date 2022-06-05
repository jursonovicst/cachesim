from typing import Optional, Iterable

from tqdm import tqdm

from cachesim.cache import Cache, Request, Status


class NonCache(Cache):
    """
    Very basic example of a cache, which actually does not cache at all.
    """

    def __init__(self):
        super().__init__(totalsize=0)

    def _lookup(self, requested: Request) -> Optional[Request]:
        # object is never in cache
        return None

    def _admit(self, fetched: Request) -> bool:
        # never allow object entering the cache
        return False

    def _store(self, fetched: Request):
        pass

    def _evict(self):
        pass

    @property
    def _treshold(self) -> bool:
        # no need to eviction
        return False


if __name__ == "__main__":

    class PBarCache(NonCache):
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


    cache = PBarCache()

    total = 10000000
    client_requests = MyRequests(n=total)

    req, sta = zip(*list(cache.map(client_requests, total=total)))

    hit = sta.count(Status.HIT)
    print(f"Requests: {len(sta)}")
    print(f"CHR: {hit / len(sta) * 100:.2f}%")
    print(f"Bytes sent: {sum(r.size for r in req)} Byte")
