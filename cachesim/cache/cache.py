from abc import ABC, abstractmethod
from typing import Optional, Iterable, Tuple

from cachesim.cache import Request, Status


class Cache(ABC):
    """
    Abstract class to provide framework and basic functions. Inherit your model from this class.
    """

    def __init__(self, size: int):
        """
        Cache initialization. Overload the init method for custom implementation.

        :param size: Size of the cache.
        """
        # check cache size (we allow 0 size for theoretical plausibility)
        assert size >= 0 and isinstance(size, int), f"Cache must have non negative integer size: '{size}' received!"
        self.__size = size

    @property
    def size(self) -> int:
        """Total size of the cache."""
        return self.__size

    def map(self, requests: Iterable[Request]):
        return map(self.__recv, requests)

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

    def __recv(self, request: Request) -> Tuple[Request, Status]:
        """
        Processes a single request against the cache.

        :param request: The request
        :return: Request status (Status).
        """

        # check the object in the cache
        stored = self._lookup(request)

        # in cache?
        if stored is not None:

            # retrieved from cache, ttl expired?
            if not stored.isexpired(request.time):
                # "serv" object from cache
                return stored, Status.HIT

        # MISS: not in cache or expired --> just simulate fetch!
        request.fetched = True

        # cache admission
        if request.cacheable and request.size <= self.size and self._admit(request):

            # treshold?
            if self.treshold:
                self._evict()

            # store object, update cache enter time for TTL
            request.enter = request.time
            self._store(request)

            # "serv" object from origin
            return request, Status.MISS

        else:
            # "serv" object in passthrough mode
            return request, Status.PASS

    @abstractmethod
    def _lookup(self, requested: Request) -> Optional[Request]:
        """
        Implement this method to provide a lookup method to find objects in cache. At this time, the content of the
        object is not known, therefore not all properties of request can be used.

        Returns the cached object.

        :param requested: Object requested.
        :return: The object from the cache or None in case of miss.
        """
        pass

    @abstractmethod
    def _admit(self, fetched: Request) -> bool:
        """
        Implement this method to provide a cache admission policy.

        :param fetched: Object fetched.
        :return: True, if object may enter the cache, False for bypass the cache and go for PASS.
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
    def treshold(self) -> bool:
        """
        Implement this property to provide a treshold for triggering cache evictions
        :return:
        """
        pass

    @abstractmethod
    def _evict(self):
        """
        Implement this method to provide cache eviction.
        """
        pass
