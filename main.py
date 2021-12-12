from cachesim import Obj, NonCache, FIFOCache, ProtectedFIFOCache

if __name__ == '__main__':
    x = Obj('x', 1000)
    a = Obj('a', 100)
    b = Obj('b', 100)
    c = Obj('c', 100)
    cache = NonCache(200)
    cache.recv(0, x)
    cache.recv(0, x)
    cache.recv(1, a)
    cache.recv(2, b)
    cache.recv(3, a)
    cache.recv(4, c)

    cache = FIFOCache(400)
    cache.recv(0, x)
    cache.recv(0, x)
    cache.recv(1, a)
    cache.recv(2, b)
    cache.recv(3, a)
    cache.recv(4, c)

    a = Obj('a', 100)
    b = Obj('b', 100)
    c = Obj('c', 30)
    cache = ProtectedFIFOCache(400)
    # too big request (>10%*400(
    cache.recv(1, a)
    cache.recv(2, b)
    cache.recv(3, a)
    # should be allowed to enter the cache
    cache.recv(4, c)
    cache.recv(4.1, c)
    cache.recv(4.2, c)
    # expired request
    cache.recv(1000, c)
