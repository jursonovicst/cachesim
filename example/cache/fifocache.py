from typing import Optional, Iterable

from tqdm import tqdm

from cachesim.cache import Cache, Request, Status


class FIFOCache(Cache):
    """
    First in First out cache model.
    """

    def __init__(self, totalsize: int):
        super().__init__(totalsize)

        # store metadata indexed by hash
        self._cache = {}

        # keep track of indexes entering the cache
        self._index = []

        # actual size of the cache
        self._size = 0

    @property
    def size(self) -> int:
        return self._size

    @size.setter
    def size(self, v: int):
        assert v >= 0, f"Size must be non negative, received '{v}'"
        self._size = v

    def _lookup(self, requested: Request) -> Optional[Request]:
        if requested.hash not in self._cache:
            return None

        return self._cache[requested.hash]

    def _admit(self, fetched: Request) -> bool:
        # check if object fit into the cache (should not normally happen, eviction should be triggered first)
        return self.size + fetched.size <= self.totalsize

    def _store(self, fetched: Request):
        assert fetched.hash not in self._index, f"Object {fetched} already in cache: {self._cache[fetched.hash]}"
        self._cache[fetched.hash] = fetched
        self._index.append(fetched.hash)
        self.size += fetched.size

    @property
    def thlow(self):
        return .9

    @property
    def thhigh(self):
        return .95

    def _evict(self):
        """
        FIFO cache, evict oldest objects first
        """

        # evict till cache reaches 90%
        while self.size / self.totalsize > self.thlow:
            hash_to_delete = self._index.pop(0)
            evicted = self._cache.pop(hash_to_delete)
            self.size -= evicted.size

    @property
    def _treshold(self) -> bool:
        return self.size / self.totalsize > self.thhigh

    def _log(self, request: Request, status: Status):
        return super()._log(request, status) + (self.size,)


if __name__ == "__main__":

    class PBarCache(FIFOCache):
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
