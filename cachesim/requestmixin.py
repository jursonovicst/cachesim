from typing import Iterable

import cachetools

from cachesim import Request, Status


class RequestMixIn:

    def getsizeof(self: cachetools.Cache, request: Request) -> float:
        return request.size

    def map(self, requests: Iterable[Request]):
        """
        Use this method to process requests.
        """
        return map(self._recv, requests)

    def _recv(self: cachetools.Cache, request: Request) -> Request:
        """
        Send request objects through the cache.
        """

        try:
            # check object in cache (use getitem to allow internal counters to be updated)
            self[request.hash]

            request.retrieve(Status.HIT)
            return request

        except KeyError:
            # not in cache (or expired) --> simulate fetch!
            request.retrieve(Status.MISS)

            try:
                if not request.cacheable:
                    raise ValueError("Non cacheable")

                # store object
                self[request.hash] = request

                # "serv" object from origin
                return request

            except ValueError:
                # "serv" object in passthrough mode
                request.retrieve(Status.PASS)
                return request
