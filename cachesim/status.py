from enum import Enum


class Status(Enum):
    """Cache status type."""
    HIT = 'hit'  # object returned from cache
    MISS = 'miss'  # object not in cache, fetched from origin
    PASS = 'pass'  # forced cache bypass (object too big or cache admission denied it)
