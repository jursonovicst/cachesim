from cachesim import Obj

from examples import ProtectedFIFOCache

if __name__ == '__main__':
    # define objects
    x = Obj('x', 1000, 300)
    a = Obj('a', 100, 300)
    b = Obj('b', 100, 300)
    c = Obj('c', 100, 300)
    d = Obj('d', 30, 300)

    # create cache
    cache = ProtectedFIFOCache(400)

    # place requests
    cache.recv(0, a)
    cache.recv(1, b)
    cache.recv(2, a)
    cache.recv(3, d)
    cache.recv(3.1, d)
    cache.recv(3.2, d)
    cache.recv(1000, d)
