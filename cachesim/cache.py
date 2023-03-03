import logging
from abc import ABC, abstractmethod
from typing import Optional

from cachesim import Obj, Status


class Cache(ABC):
    """
    Abstract class to provide structure and basic functionalities for cache emulation. Inherit to implement your own
    cache model.
    """

    def __init__(self, maxsize: int, logger: logging.Logger = None):
        """
        Cache initialization. Overload the init method for custom settings.

        :param maxsize: maximum size of the cache.
        :param logger: logger to use instead of the own one.
        """

        # max cache size
        assert maxsize > 0 and isinstance(maxsize, int), f"Cache size must be positive integer : '{maxsize}' received!"
        self.__maxsize = maxsize

        # keep track of the time
        self.__clock = None

        # setup logging
        self.__logger = logging.getLogger(name=self.__class__.__name__) if logger is None else logger

    @property
    def maxsize(self) -> int:
        """Total size of the cache."""
        return self.__maxsize

    @property
    def clock(self) -> float:
        """Current time."""
        return self.__clock

    @clock.setter
    def clock(self, time: float):
        """Update current time."""
        assert self.__clock is None or time >= self.__clock, f"Time passes, you will never become younger!"
        self.__clock = time

    def recv(self, time: float, obj: Obj) -> Status:
        """
        Call this function to place a request towards the cache.

        :param time: Time (epoch) of the object request.
        :param obj: The object (Obj) requested.
        :return: Request status (Status).
        """

        # update the internal clock
        self.clock = time

        # try to get the object from cache

        if (stored := self._lookup(obj)) is not None:

            # retrieved from cache, check object expire
            if not stored.isexpired(self.clock):
                # HIT, "serv" object from cache
                self.__log(stored, Status.HIT)
                return Status.HIT

        # MISS: not in cache or expired --> just simulate fetch!
        obj.fetched = True

        # cache admission
        if obj.cacheable and obj.size <= self.maxsize and self._admit(obj):

            # store
            obj.enter = self.clock
            self._store(obj)

            self.__log(obj, Status.MISS)
            return Status.MISS

        else:
            # object not cacheable, log pass
            self.__log(obj, Status.PASS)
            return Status.PASS

    @abstractmethod
    def _admit(self, fetched: Obj) -> bool:
        """
        Implement this method to provide a cache admission policy.

        :param fetched: Object (Obj) fetched.
        :return: True, if object may enter the cache, False for bypass the cache and go for PASS.
        """
        pass

    @abstractmethod
    def _lookup(self, requested: Obj) -> Optional[Obj]:
        """
        Implement this method to provide a caching function. In this state, the content of the object is not known.
        Return the cached object.

        :param requested: Object (Obj) requested.
        :return: The object (Obj) from the cache.
        """
        pass

    @abstractmethod
    def _store(self, fetched: Obj):
        """
        Implement this method to store objects.

        :param fetched: Object (Obj) fetched from origin.
        """
        pass

    def __log(self, obj, status: Status):
        """Basic logging"""
        self.__logger.warning(f"{self.clock} {status} {obj}")
