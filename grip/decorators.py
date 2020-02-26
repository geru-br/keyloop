import functools


def view_modifier(validator=None, schema=None):

    def wrapper(func):
        return func

    return wrapper
