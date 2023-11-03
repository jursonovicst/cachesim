from abc import ABC, abstractmethod
from typing import Optional, Tuple

from cachesim import Reader, Request
from cachesim import Status


class Cache(ABC):
    """
    Abstract class to provide framework and basic functions. Inherit your model from this class.
    """

    def __init__(self, totalsize: int):
        """
        Cache initialization. Overload the init method for custom implementation.

        :param totalsize: size of the cache, non-positive value will disable caching.
        """
        self.__totalsize = totalsize if totalsize > 0 else 0

    @property
    def totalsize(self) -> int:
        """Total size of the cache."""
        return self.__totalsize

    def map(self, reader: Reader):
        return map(self._recv, reader)

    def _recv(self, request: Request) -> Tuple[Request, Status, float]:
        """
        Processes a single request against the cache.

        :param request: The request
        :return: requested object (fetched), status, age
        """

        # check the object in cache
        if (stored := self._lookup(request)) is not None:

            # retrieved from cache, ttl expired?
            if not stored.isexpired(request.requestedat):
                # "serv" object from cache
                return stored, Status.HIT, request.requestedat - stored.storedat

        # MISS: not in cache or expired --> just simulate fetch!
        request.fetched = True

        # cache admission
        if request.cacheable and request.size <= self.totalsize and self._admit(request):

            # treshold?
            if self._treshold:
                self._evict()

            # store object
            self._store(request)

            # "serv" object from origin
            return request, Status.MISS, 0

        else:
            # "serv" object in passthrough mode
            return request, Status.PASS, 0

    @abstractmethod
    def _lookup(self, requested: Request) -> Optional[Request]:
        """
        Implement this method to provide a lookup method to find objects in the cache. At this time, the content of the
        object is not known, therefore not all properties of request can be used.

        Returns the cached object.

        :param requested: Object requested.
        :return: The object from the cache or None in case of miss.
        """
        ...

    @abstractmethod
    def _admit(self, fetched: Request) -> bool:
        """
        Implement this method to provide a cache admission policy.

        :param fetched: Object fetched.
        :return: True, if object may enter the cache, False for bypass and go for PASS.
        """
        ...

    @abstractmethod
    def _store(self, fetched: Request) -> None:
        """
        Implement this method to store objects.

        :param fetched: Object fetched from origin.
        """
        ...

    @property
    @abstractmethod
    def _treshold(self) -> bool:
        """
        Implement this property to provide a threshold for triggering cache eviction.
        :return: True, if cache eviction needs to be triggered, False otherwise.
        """
        ...

    @abstractmethod
    def _evict(self) -> None:
        """
        Implement this method to provide cache eviction.
        """
        ...