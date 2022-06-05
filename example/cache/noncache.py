from typing import Optional

from cachesim.cache import Cache, Request


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
