from cachesim import Obj, Status
import logging
from abc import ABC, abstractmethod
from typing import Optional


class Cache(ABC):
    """
    Abstract class to provide structure and basic functionalities. Use this to implement your own cache model.
    """

    def __init__(self, maxsize: int, logger: logging.Logger = None):
        """
        Cache initialization. Overload the init method for custom initialization.

        :param maxsize: Maximum size of the cache.
        :param logger: If not None, use this logger, otherwise create one.
        """

        # max cache size
        assert maxsize > 0 and isinstance(maxsize, int), f"Cache must have positive integer size: '{maxsize}' received!"
        self._maxsize = maxsize

        # keep track of the time
        self._clock = None

        # setup logging
        if logger is None:
            self._logger = logging.getLogger(name=self.__class__.__name__)
            # self._logger.setLevel(logging.DEBUG)  TODO: FIX this
        else:
            self._logger = logger

    @property
    def maxsize(self) -> int:
        """Total size of the cache."""
        return self._maxsize

    @property
    def clock(self) -> float:
        """Current time."""
        return self._clock

    @clock.setter
    def clock(self, time: float):
        """Update current time."""
        assert self._clock is None or time >= self._clock, f"Time passes, you will never become younger!"
        self._clock = time

    def recv(self, time: float, obj: Obj) -> Status:
        """
        Call this function to place a request to the cache.

        :param time: Time (epoch) of the object request.
        :param obj: The object (Obj) requested.
        :return: Request status (Status).
        """

        # update the internal clock
        self.clock = time

        # try to get the object from cache
        stored = self.lookup(obj)
        if stored is not None:

            # retrieved from cache, check expires
            if not stored.isexpired(self.clock):
                # HIT, "serv" object from cache
                self.log(stored, Status.HIT)
                return Status.HIT

        # MISS: not in cache or expired --> just simulate fetch!
        obj.fetched = True

        # cache admission
        if self.admit(obj):

            # store
            obj.enter = self.clock
            self.store(obj)

            self.log(obj, Status.MISS)
            return Status.MISS

        else:
            self.log(obj, Status.PASS)
            return Status.PASS

    @abstractmethod
    def admit(self, fetched: Obj) -> bool:
        """
        Implement this method to provide a cache admission policy.

        :param fetched: Object fetched.
        :return: True, if object may enter the cache, False for bypass the cache and go for PASS.
        """
        pass

    @abstractmethod
    def lookup(self, requested: Obj) -> Optional[Obj]:
        """
        Implement this method to provide a caching function. In this state, the content of the object is not known.
        Return the cached object.

        :param requested: Object requested.
        :return: The object from the cache.
        """
        pass

    @abstractmethod
    def store(self, fetched: Obj):
        """
        Implement this method to store objects.

        :param fetched: Object fetched from origin.
        """
        pass

    def log(self, obj, status: Status):
        """Basic logging"""
        self._logger.warning(f"{self.clock} {status} {obj}")
