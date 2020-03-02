import functools


def grip_view(validators=None, schema=None, response_schema=None, error_handler=None):

    def wrapper(func):

        if schema:
            func.grip_schema = schema

        if response_schema:
            func.grip_response_schema = response_schema

        if error_handler:
            func.grip_error_handler = error_handler

        if validators:
            func.grip_validators = validators
        return func

    return wrapper
