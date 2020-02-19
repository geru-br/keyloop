from functool import wraps

def singleton(cls):
    original_new = cls.__new__
    @wraps(cls.__new__)
    def wrapper(cls, *args, **kw):
        instance = getattr(cls, "single_instance", None)
        if instance:
            return instance
        instance = original_new(cls)
        instance.__init__(*args, **kw)
        cls.single_instance = instance
        return instance
    cls.__new__ = wrapper
    return cls


class singletonmethod:
    """
    Decorates a method that needs a class instance to be run
    but have to be called as if it where a classmethod.
    """

    def __init__(self, meth):
        if isinstance(singletonmethod, type):
            cls = singletonmethod
            def wrapper(*args, **kw):
                instance = cls(*args, **kw)
                instance.single_instance = cls

        self.meth = meth

    def __get__(self, instance, owner):
        if not instance:
            instance = getattr(owner, "single_instance", None)
            if not instance:
                raise RuntimeError("singletonmethod attempted on non-initialized class")
        return lambda *args, **kwargs: self.meth(instance, *args, **kwargs)
