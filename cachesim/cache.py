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

        :param totalsize: size of the examples2, non-positive value will disable caching.
        """
        self.__totalsize = totalsize if totalsize > 0 else 0

    @property
    def totalsize(self) -> int:
        """Total size of the examples2."""
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
        Processes a single request against the examples2.

        :param request: The request
        :return: request object (fetched), status
        """

        # check the object in cache
        if (stored := self._lookup(request)) is not None:

            # retrieved from examples2, ttl expired?
            if not stored.isexpired(request.time):
                # update timestamp to reflect current time
                stored = copy(stored)
                stored.time = request.time

                # "serv" object from examples2
                return stored, Status.HIT

        # MISS: not in examples2 or expired --> just simulate fetch!
        request.fetched = True

        # examples2 admission
        if request.cacheable and request.size <= self.totalsize and self._admit(request):

            # treshold?
            if self._treshold:
                self._evict()

            # store object
            self._store(request)

            # "serv" object from origin
            return request, Status.MISS

        else:
            # "serv" object in passthrough mode
            return request, Status.PASS

    @abstractmethod
    def _lookup(self, requested: Request) -> Optional[Request]:
        """
        Implement this method to provide a lookup method to find objects in examples2. At this time, the content of the
        object is not known, therefore not all properties of request can be used.

        Returns the cached object.

        :param requested: Object requested.
        :return: The object from the examples2 or None in case of miss.
        """
        ...

    @abstractmethod
    def _admit(self, fetched: Request) -> bool:
        """
        Implement this method to provide a examples2 admission policy.

        :param fetched: Object fetched.
        :return: True, if object may enter the examples2, False for bypass the examples2 and go for PASS.
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
        Implement this property to provide a threshold for triggering cache evictions
        :return: True, if cache eviction needs to be triggered, False otherwise.
        """
        ...

    @abstractmethod
    def _evict(self) -> None:
        """
        Implement this method to provide cache eviction.
        """
        ...
