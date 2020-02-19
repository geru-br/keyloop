from functools import wraps


def singleton(cls):
    @wraps(cls)
    def wrapper(*args, **kw):
        instance = getattr(cls, "single_instance", None)
        if instance:
            return instance
        instance = cls(*args, **kw)
        instance.single_instance = instance
        return instance

    return wrapper


class singletonmethod:
    """
    Decorates a method that needs a class instance to be run
    but have to be called as if it where a classmethod.
    (For example a DB-assessing method that needs a sqlalchemy session created in __init__)
    """

    def __init__(self, meth):
        self.meth = meth

    def __get__(self, instance, owner):
        if not instance:
            instance = getattr(owner, "single_instance", None)
            if not instance:
                raise RuntimeError("singletonmethod attempted on non-initialized class")
        return lambda *args, **kwargs: self.meth(instance, *args, **kwargs)
