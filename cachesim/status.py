from enum import Enum


class Status(Enum):
    """
    Cache status type.
    """
    HIT = 0     # object served from cache
    MISS = 1    # object not in cache, fetched from origins
    PASS = 2    # forced cache bypass (object too big or cache admission denied)
