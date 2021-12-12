from cachesim import Cache, Obj
from typing import Optional


class NonCache(Cache):
    """
    Very basic example of a cache, which actually does not cache at all.
    """

    def lookup(self, requested: Obj) -> Optional[Obj]:
        return None

    def admit(self, fetched: Obj) -> bool:
        return True

    def store(self, fetched: Obj):
        pass
