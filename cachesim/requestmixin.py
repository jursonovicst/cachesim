import cachetools

from cachesim import Request, Status


class RequestMixIn:

    @staticmethod
    def getsizeof(value: Request) -> float:
        """
        Overload cachetools.Cache getsizeof method.
        """
        return value.size

    def request(self, req: Request):
        """

        """

    def __getitem__(self: cachetools.Cache, request: Request):
        """
        Send request objects through the cache.
        """

        try:
            # check object in cache (call getitem to allow internal counters to be updated)
            cachetools.Cache.__getitem__(self, request.hash)
            # self[request.hash]

            request.retrieve(Status.HIT)
            return request

        except KeyError:
            # not in cache (or expired) --> simulate fetch! TODO: check expired implementation!
            request.retrieve(Status.MISS)

            try:
                if not request.cacheable:
                    raise ValueError("Non cacheable")

                # store object
                cachetools.Cache.__setitem__(self, request.hash, request)
                # self[request.hash] = request

                # "serv" object from origin
                return request

            except ValueError:
                # "serv" object in passthrough mode
                request.retrieve(Status.PASS)
                return request

    def __setitem__(self, key, value):
        raise SyntaxError('Cannot call')
