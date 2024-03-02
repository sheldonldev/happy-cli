import threading


# Based on tornado.ioloop.IOLoop.instance() approach.
# See https://github.com/facebook/tornado
class SingletonMixin(object):
    __singleton_lock = threading.Lock()
    __singleton_instance = None

    @classmethod
    def instance(cls):
        if not cls.__singleton_instance:
            with cls.__singleton_lock:
                if not cls.__singleton_instance:
                    cls.__singleton_instance = cls()
        return cls.__singleton_instance


if __name__ == '__main__':

    class A(SingletonMixin):
        pass

    class B(SingletonMixin):
        pass

    a = A.instance()
    a2 = A.instance()
    assert a is a2

    b = B.instance()
    b2 = B.instance()
    assert b is b2

    assert a is not b2
