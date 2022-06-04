import logging
from abc import ABC, abstractmethod
from multiprocessing import Process, Queue
from typing import Optional

from tqdm import tqdm

from cachesim.cache import Request, Status


class Cache(ABC, Process):
    """
    Abstract class to provide framework and basic functions. Inherit your model from this class.
    """

    def __init__(self, size: int, in_q: Queue, logger: logging.Logger = None):
        """
        Cache initialization. Overload the init method for custom implementation.

        :param size: Size of the cache.
        :param in_q: Queue to read to get chunks of requests to process.
        :param logger: Provide a logger, or use the default one.
        """
        super().__init__(name=self.__class__.__name__)

        # check cache size
        assert size > 0 and isinstance(size, int), f"Cache must have positive integer size: '{size}' received!"
        self.__size = size

        self.__in_q = in_q

        # setup logging
        if logger is None:
            self.__logger = logging.getLogger(name=self.__class__.__name__)
            # self._logger.setLevel(logging.DEBUG)  TODO: FIX this
        else:
            self.__logger = logger

        # KPIs
        self._hit = 0
        self._count = 0

    @property
    def size(self) -> int:
        """Total size of the cache."""
        return self.__size

    @property
    def queue(self):
        return self.__in_q

    @property
    def chr(self) -> float:
        return self._hit / self._count

    def run(self):
        try:
            # use a progress bar to keep track of the simulation
            with tqdm(desc=self.__class__.__name__, position=2) as pbar:

                # chunk of ingress metadata
                while chunk_in := self.__in_q.get():
                    # process requests in the queue, collect metadata
                    chunk_e = list(map(self.__recv, chunk_in))

                    # update KPIs
                    self._count += len(chunk_in)
                    self._hit += sum(map(lambda status: 1 if status == Status.HIT else 0))

                    # update progress bar
                    pbar.update(len(chunk_e))

        except KeyboardInterrupt:
            pass
        except Exception as e:
            self.__logger.exception(f"{e.__class__.__name__} occurred: {e}")
        finally:
            # close process
            self.close()

    def __recv(self, request: Request) -> Status:
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
                # HIT
                self.monitor(stored, Status.HIT)

                # "serv" object from cache
                return Status.HIT

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

            # MISS
            self.monitor(request, Status.MISS)

            # "serv" object from origin
            return Status.MISS

        else:
            # PASS
            self.monitor(request, Status.PASS)

            # "serv" object in passthrough mode
            return Status.PASS

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

    def monitor(self, fetched: Request, status: Status):
        """

        :return:
        """
        self.__log(fetched, status)

    def __log(self, request: Request, status: Status):
        """Basic logging"""
        self.__logger.warning(f"{request} {status}")
