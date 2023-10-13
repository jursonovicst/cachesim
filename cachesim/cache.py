from abc import ABC, abstractmethod
from copy import copy
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

        :param totalsize: size of the caches, non-positive value will disable caching.
        """
        self.__totalsize = totalsize if totalsize > 0 else 0

    @property
    def totalsize(self) -> int:
        """Total size of the caches."""
        return self.__totalsize

    def map(self, reader: Reader):
        return map(self._recv, reader)

    # def imap(self, requests: Iterable[Request], chunksize: int = 1):
    #     self.map(requests)
    #
    #         # return iterator for slices
    #         for chunk in islice(result_i, chunksize):
    #             print(chunk)
    #
    #     except KeyboardInterrupt:
    #         pass
    #     except Exception as e:
    #         self.__logger.exception(f"{e.__class__.__name__} occurred: {e}")

    # def run(self):
    #     try:
    #         # map the __recv function (in tqdm for progress bar) to create an iterator object
    #         result_i = map(self.__recv, tqdm(self.__requests, desc=self.__class__.__name__, position=2))
    #
    #         # start processing in chunks
    #         for chunk in islice(result_i, 10):
    #             print(chunk)
    #
    #     except KeyboardInterrupt:
    #         pass
    #     except Exception as e:
    #         self.__logger.exception(f"{e.__class__.__name__} occurred: {e}")
    #     finally:
    #         # close process
    #         self.close()

    def _recv(self, request: Request) -> Tuple[Request, Status]:
        """
        Processes a single request against the caches.

        :param request: The request
        :return: Request status (Status).
        """
        # check the object in the caches, make a copy to overwrite attributes.
        stored = self._lookup(request)

        # in caches?
        if stored is not None:

            # retrieved from caches, ttl expired?
            if not stored.isexpired(request.time):
                # update timestamp to reflect current time
                stored = copy(stored)
                stored.time = request.time

                # "serv" object from caches
                return self._log(stored, Status.HIT)

        # MISS: not in caches or expired --> just simulate fetch!
        request.fetched = True

        # caches admission
        if request.cacheable and request.size <= self.totalsize and self._admit(request):

            # treshold?
            if self._treshold:
                self._evict()

            # store object
            self._store(request)

            # "serv" object from origin
            return self._log(request, Status.MISS)

        else:
            # "serv" object in passthrough mode
            return self._log(request, Status.PASS)

    @abstractmethod
    def _lookup(self, requested: Request) -> Optional[Request]:
        """
        Implement this method to provide a lookup method to find objects in caches. At this time, the content of the
        object is not known, therefore not all properties of request can be used.

        Returns the cached object.

        :param requested: Object requested.
        :return: The object from the caches or None in case of miss.
        """
        pass

    @abstractmethod
    def _admit(self, fetched: Request) -> bool:
        """
        Implement this method to provide a caches admission policy.

        :param fetched: Object fetched.
        :return: True, if object may enter the caches, False for bypass the caches and go for PASS.
        """
        pass

    @abstractmethod
    def _store(self, fetched: Request):
        """
        Implement this method to store objects.

        :param fetched: Object fetched from origin.
        """
        pass

    @property
    @abstractmethod
    def _treshold(self) -> bool:
        """
        Implement this property to provide a treshold for triggering caches evictions
        :return:
        """
        pass

    @abstractmethod
    def _evict(self):
        """
        Implement this method to provide caches eviction.
        """
        pass

    def _log(self, request: Request, status: Status):
        return request, status
