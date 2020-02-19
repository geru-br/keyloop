
class singletonmethod:
    """
    Decorates a method that needs a class instance to be run
    but have to be called as if it where a classmethod.

    (For example a DB-assessing method that needs a sqlalchemy session created in __init__)
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
                instance = owner.single_instance = owner()
        return lambda *args, **kwargs: self.meth(instance, *args, **kwargs)
