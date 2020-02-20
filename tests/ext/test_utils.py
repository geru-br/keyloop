from keyloop.ext.utils.decorators import singleton, singletonmethod

def test_singleton_decorator():
    @singleton
    class A:
        pass

    a = A()
    b = A()
    assert a is b


def test_singletonmethod_decorator():
    @singleton
    class A:
        def __init__(self, x):
            self.x = x
        @singletonmethod
        def test(self):
            return self.x

    A(1234)
    assert A.test() == 1234
