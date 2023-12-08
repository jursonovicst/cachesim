import collections

import cachetools

from cachesim import RequestMixIn


class SimpleCache(cachetools.Cache, RequestMixIn):
    pass


class NonCache(cachetools.Cache, RequestMixIn):

    def __init__(self):
        super().__init__(maxsize=0)


class LFUCache(cachetools.LFUCache, RequestMixIn):
    pass


class BeladyCache(cachetools.Cache, RequestMixIn):

    def __init__(self, maxsize, future, getsizeof=None):
        super().__init__(maxsize, getsizeof)
        self.__fut = future
        self.__idx = -1

    def __setitem__(self, key, value, internal=False):
        if not internal:
            raise SyntaxError("Do not use setitem method.")
        super().__setitem__(key, value)

    def setitem(self, key, value, index):
        self.__idx = index
        self.__setitem__(key, value, internal=True)

    def popitem(self):
        """Remove and return the `(key, value)` pair not needed for the longest time."""
        key = max(self.keys(), key=lambda h: self.__pos(self.__fut, self.__idx, h))
        return key, self.pop(key)

    @staticmethod
    def __pos(array: list, start: int, value):
        try:
            return array.index(value, start)
        except ValueError:
            return len(array)  # if not in future (not requested anymore), use maximal position


class GLFUCache(cachetools.Cache, RequestMixIn):
    """Global Least Frequently Used (LFU) cache implementation."""

    # def __init__(self, maxsize, getsizeof=None):
    #     Cache.__init__(self, maxsize, getsizeof)
    #     self.__counter = collections.Counter()

    def __init__(self, maxsize, getsizeof=None, maxseen=None):
        cachetools.Cache.__init__(self, maxsize, getsizeof)
        self.__counter = collections.Counter()

        self.__seen = collections.Counter()
        self.__maxseen = maxseen

    def __getitem__(self, key, cache_getitem=cachetools.Cache.__getitem__):
        value = cache_getitem(self, key)
        if key in self:  # __missing__ may not store item
            self.__counter[key] -= 1
        return value

    # def __setitem__(self, key, value, cache_setitem=Cache.__setitem__):
    #     cache_setitem(self, key, value)
    #     self.__counter[key] -= 1

    def __setitem__(self, key, value, cache_setitem=cachetools.Cache.__setitem__):
        cache_setitem(self, key, value)
        self.__counter[key] -= 1 if key not in self.__seen else -self.__seen.pop(key)

    @property
    def counter(self):
        return self.__counter

    @property
    def seen(self):
        return self.__seen

    # def __delitem__(self, key, cache_delitem=Cache.__delitem__):
    #     cache_delitem(self, key)
    #     del self.__counter[key]

    def __delitem__(self, key, cache_delitem=cachetools.Cache.__delitem__):
        cache_delitem(self, key)
        self.__seen[key] = self.__counter[key]
        del self.__counter[key]

    def popitem(self):
        """Remove and return the `(key, value)` pair least frequently used."""
        try:
            ((key, _),) = self.__counter.most_common(1)
        except ValueError:
            raise KeyError("%s is empty" % type(self).__name__) from None
        else:
            return (key, self.pop(key))


class LRUCache(cachetools.LRUCache, RequestMixIn):
    pass
