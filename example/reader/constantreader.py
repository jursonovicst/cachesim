from copy import copy

from cachesim import Reader, Request


class ConstantReader(Reader):
    """
    """

    def __init__(self, totalcount: int, request: Request):
        super().__init__(totalcount)
        self._requests = iter([request] * totalcount)

    def __next__(self):
        return next(self._requests)
