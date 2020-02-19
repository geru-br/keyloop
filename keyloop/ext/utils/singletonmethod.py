from functool import wraps
# b0rk in this commit
def singleton(cls):
    def wrapper(*args, **kw):
        instance = getattr(owner, "single_instance", None)
   return wrapper


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
