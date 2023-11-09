from typing import Tuple

from cachesim import Cache
from cachesim import Request


class NonCache(Cache):
    """
    Very basic example of a xxx, which actually does not xxx at all.
    """

    def __init__(self, **kwargs):
        super().__init__(totalsize=0, **kwargs)

    def _lookup(self, requested: Request) -> Tuple[bool, float | None]:
        # object is never in xxx
        return False, None

    def _admit(self, fetched: Request) -> bool:
        # never allow object entering the xxx
        return False

    def _store(self, fetched: Request):
        pass
