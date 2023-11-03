from copy import copy

from cachesim import Reader, Request


class ConstantReader(Reader):
    """
    """

    def __init__(self, count: int, request: Request):
        super().__init__(count)
        self._request = request
        self._requests = None

    def __iter__(self):
        self._requests = iter([self._request] * self.totalcount)
        return super().__iter__()

    def __next__(self):
        return next(self._requests)
