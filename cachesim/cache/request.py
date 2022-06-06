class Request:
    """
    Represents the metadata of the cache request
    """

    def __init__(self, time: float, hash: str, size: int, maxage: int):
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
        self._enter = None  # time at the object entered the cache (for TTL calculation)

        # misc
        self._fetched = False  # object fetched (retrieved from origin)

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

    @property
    def enter(self) -> float:
        assert self.fetched, f"enter cannot be known before object fetch!"
        return self._enter

    @enter.setter
    def enter(self, time: float):
        assert self.fetched, f"enter cannot be set before object fetch!"
        self._enter = time

    def isexpired(self, now: float) -> bool:
        assert self.enter is not None, f"Object must first enter the cache to determine if it is expired."
        return self.enter + self.maxage < now

    @property
    def fetched(self) -> bool:
        return self._fetched

    @fetched.setter
    def fetched(self, val: bool):
        self._fetched = val

    def __add__(self, other):
        """For sum() function"""
        assert isinstance(other, Request), f"Operator add has been implemented only for {self.__class__.__name__} type."
        return self.size + other

    def __radd__(self, other):
        """For sum() function"""
        assert isinstance(other, int), f"Operator radd has been implemented only for {self.__class__.__name__} type."
        return other + self.size

    def __eq__(self, other):
        """To implement in operator"""
        assert isinstance(other, Request), f"Operator EQ has been implemented only for {self.__class__.__name__} type."
        return self.hash == other.hash

    def __str__(self):
        """For logging"""
        return f"{self._time} {self.hash} {self.size if self.fetched else '-'} {self.maxage if self.fetched else '-'}"
