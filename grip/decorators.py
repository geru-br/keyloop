import functools


def view_modifier(validators=(), schema=None):

    def wrapper(func):
        func.grip_validators = validators
        func.grip_schema = schema
        return func

    return wrapper
