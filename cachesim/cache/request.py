class Request:
    """
    Represents the metadata of the cache request
    """

    def __init__(self, time: float, hash: str, size: int, maxage: int, fetched: bool = False):
        """

        :param time: Timestamp (unix time) at the request was placed.
        :param hash: Uniq identifier of the requested object (hash).
        :param size: Size of the requested object.
        :param maxage: Maximum caching time. For non cacheable objects, use a non positive value.
        """
        # metadata to be known before fetch
        self._time = time
        self._hash = hash

        # metadata only known after fetch
        self._size = size
        self._maxage = maxage

        # misc
        self._fetched = fetched  # object fetched (retrieved from origin)

    @property
    def time(self) -> float:
        return self._time

    @time.setter
    def time(self, v: float):
        self._time = v

    @property
    def hash(self) -> str:
        return self._hash

    @property
    def size(self) -> int:
        assert self.fetched, f"size property cannot be known before object fetch!"
        return self._size

    @property
    def maxage(self) -> int:
        assert self.fetched, f"maxage property cannot be known before object fetch!"
        return self._maxage

    @property
    def cacheable(self) -> bool:
        assert self.fetched, f"cacheable cannot be known before object fetch!"
        return self.maxage > 0

    def isexpired(self, now: float) -> bool:
        assert self.fetched, f"Object must first enter the cache to determine if it is expired."
        return self.time + self.maxage < now

    @property
    def fetched(self) -> bool:
        return self._fetched

    @fetched.setter
    def fetched(self, val: bool):
        self._fetched = val

    def __add__(self, other):
        """For sum() function"""
        assert isinstance(other, Request), f"Operator add has been implemented only for {self.__class__.__name__} type."
        return self.size + other.size

    # def __radd__(self, other):
    #     """For sum() function"""
    #     assert isinstance(other, int), f"Operator radd has been implemented only for {self.__class__.__name__} type."
    #     return other + self.size

    def __str__(self):
        """For logging"""
        return f"{self._time} {self._hash} {self._size if self.fetched else '-'} {self._maxage if self.fetched else '-'}"

    def __copy__(self):
        return type(self)(self.time, self.hash, self.size, self.maxage, self._fetched)
