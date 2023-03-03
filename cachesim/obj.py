class Obj:
    """
    Represents an object only by his caching metadata (size, time accessed, cacheable, etc...), without the bytes of the
    object itself. Objects can be requested from or stored by a cache, therefore part of the metadata (like size, ...)
    can be accessed only after the object marked as fetched (see the .fetcher property). Any attempt accessing not to be
    known metadata parts will result an assertion!
    """

    def __init__(self, hash, size: int, maxage: int):
        """

        :param hash: Uniq identifier of the object (hash key).
        :param size: Size of the object.
        :param maxage: Maximum caching time. Any non-positive number represents not cacheable objects.
        """
        self._hash = hash
        self._size = size
        self._maxage = maxage

        self._enter = None  # time at the object entered the cache
        self._fetched = False  # object retrieved from origin

    @property
    def hash(self):
        return self._hash

    @property
    def size(self) -> int:
        assert self.fetched, f"This property should not be known before object fetch!"
        return self._size

    @property
    def maxage(self) -> int:
        assert self.fetched, f"This property should not be known before object fetch!"
        return self._maxage

    @property
    def cacheable(self) -> bool:
        return self.maxage > 0

    @property
    def enter(self) -> float:
        return self._enter

    @enter.setter
    def enter(self, time: float):
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
        assert isinstance(other, Obj), f"Operator add has been implemented only for Obj type."
        return self.size + other

    def __radd__(self, other):
        """For sum() function"""
        assert isinstance(other, int), f"Operator radd has been implemented only for Obj type."
        return other + self.size

    def __eq__(self, other):
        """To implement in operator"""
        assert isinstance(other, Obj), f"Operator EQ has been implemented only for Obj type."
        return self.hash == other.hash

    def __str__(self):
        return f"{self.hash} {self._size}"
