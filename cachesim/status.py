from enum import Enum


class Status(Enum):
    """
    Cache status type.
    """
    HIT = 'hit'  # object returned from caches
    MISS = 'miss'  # object not in caches, fetched from origin
    PASS = 'pass'  # forced caches bypass (object too big or caches admission denied it)
