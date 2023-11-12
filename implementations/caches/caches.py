import cachetools

from cachesim import RequestMixIn


class SimpleCache(cachetools.Cache, RequestMixIn):
    pass


class NonCache(cachetools.Cache, RequestMixIn):

    def __init__(self):
        super().__init__(maxsize=0)


class LFUCache(cachetools.LFUCache, RequestMixIn):
    pass


class LRUCache(cachetools.LRUCache, RequestMixIn):
    pass
