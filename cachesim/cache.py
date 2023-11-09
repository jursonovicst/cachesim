from abc import ABC, abstractmethod
from typing import Tuple, Iterable

from cachesim import Request
from cachesim import Status


class Cache(ABC):
    """
    Abstract class to provide framework and basic functions. Inherit your model from this class.
    """

    def __init__(self, totalsize: int, **kwargs):
        """
        Cache initialization. Overload the init method for custom implementation.

        :param totalsize: size of the cache, non-positive value will disable caching.
        """
        self.__totalsize = totalsize if totalsize > 0 else 0

    @property
    def totalsize(self) -> int:
        """Total size of the cache."""
        return self.__totalsize

    def map(self, requests: Iterable[Request]):
        """
        Use this method to process requests.
        """
        return map(self._recv, requests)

    def _recv(self, request: Request) -> Request:
        """
        Processes a single request against the cache.

        :param request: The request
        :return: requested object (fetched)
        """

        # check the object in cache
        found, time_stored = self._lookup(request)
        if found:
            # retrieved from cache, update status.
            request.retrieve(Status.HIT)

            return request

        # not in cache (or expired) --> simulate fetch!
        request.retrieve(Status.MISS)

        # cache admission
        if request.cacheable and request.size <= self.totalsize and self._admit(request):

            # store object
            self._store(request)

            # "serv" object from origin
            return request

        else:
            # "serv" object in passthrough mode
            request.retrieve(Status.PASS)
            return request

    @abstractmethod
    def _lookup(self, requested: Request) -> Tuple[bool, float | None]:
        """
        Implement this method to provide a lookup method to find objects in the cache. At this time, the content of the
        object is not known, therefore not all properties of request can be used.

        Returns a cache lookup result.

        :param requested: Object requested.
        :return: tuple of True if found in cache else False and the timestamp of storage time, None if not found.
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
