import functools


def view(validators=None, schema=None, response_schema=None, error_handler=None, factory=None):

    def wrapper(func):

        #TODO adjust for single entity containing all functions

        if schema:
            func.grip_schema = schema

        if response_schema:
            func.grip_response_schema = response_schema

        if error_handler:
            func.grip_error_handler = error_handler

        if validators:
            func.grip_validators = validators

        if factory:
            func.grip_factory = factory

        return func

    return wrapper
